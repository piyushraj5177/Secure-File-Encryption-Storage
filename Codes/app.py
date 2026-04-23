from flask import Flask, render_template, request, redirect, session, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        mobile TEXT UNIQUE,
        dob TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        user TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- ENCRYPTION ----------
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as f:
            f.write(key)
    return open("secret.key", "rb").read()

cipher = Fernet(load_key())

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('index.html', dashboard=('user' in session))


# ---------- REGISTER ----------
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip()
    password = generate_password_hash(request.form['password'])
    mobile = request.form['mobile'].strip()
    dob = request.form['dob']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? OR mobile=?", (username, mobile))
    if cursor.fetchone():
        conn.close()
        return render_template('index.html', error="Username or Mobile already exists!")

    cursor.execute("INSERT INTO users (username,password,mobile,dob) VALUES (?,?,?,?)",
                   (username, password, mobile, dob))
    conn.commit()
    conn.close()

    return render_template('index.html', success="Account created successfully!")


# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    data = cursor.fetchone()
    conn.close()

    if not data:
        return render_template('index.html', error="Username not found!")

    if check_password_hash(data[0], password):
        session['user'] = username
        return redirect('/')

    return render_template('index.html', error="Wrong password!")


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------- UPLOAD ----------
@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect('/')

    file = request.files['file']
    if file.filename == '':
        return redirect('/')

    os.makedirs("encrypted_files", exist_ok=True)

    path = os.path.join("encrypted_files", file.filename)
    data = file.read()
    encrypted = cipher.encrypt(data)

    with open(path, 'wb') as f:
        f.write(encrypted)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (filename,user) VALUES (?,?)",
                   (file.filename, session['user']))
    conn.commit()
    conn.close()

    return redirect('/')


# ---------- FILE LIST ----------
@app.route('/get_files')
def get_files():
    if 'user' not in session:
        return jsonify([])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM files WHERE user=?", (session['user'],))
    data = cursor.fetchall()
    conn.close()

    return jsonify([f[0] for f in data])


# ---------- VERIFY PASSWORD ----------
@app.route('/verify_password', methods=['POST'])
def verify_password():
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (session['user'],))
    data = cursor.fetchone()
    conn.close()

    if check_password_hash(data[0], password):
        return "OK", 200
    return "Wrong", 401


# ---------- DOWNLOAD ----------
@app.route('/download/encrypted/<filename>')
def download_encrypted(filename):
    return send_file(os.path.join("encrypted_files", filename), as_attachment=True)


@app.route('/download/decrypted/<filename>')
def download_decrypted(filename):
    path = os.path.join("encrypted_files", filename)
    data = open(path, 'rb').read()
    decrypted = cipher.decrypt(data)

    temp = "temp_" + filename
    open(temp, 'wb').write(decrypted)

    return send_file(temp, as_attachment=True)


# ---------- DELETE FILE ----------
@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join("encrypted_files", filename))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE filename=?", (filename,))
    conn.commit()
    conn.close()

    return redirect('/')


# ---------- USERS ----------
@app.route('/get_users')
def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    data = cursor.fetchall()
    conn.close()
    return jsonify([u[0] for u in data])


@app.route('/delete_user', methods=['POST'])
def delete_user():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    data = cursor.fetchone()

    if data and check_password_hash(data[0], password):

        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        cursor.execute("DELETE FROM files WHERE user=?", (username,))
        conn.commit()

        conn.close()
        return "OK", 200

    conn.close()
    return "Wrong", 401


# ---------- RESET PASSWORD ----------
@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form['username']
    mobile = request.form['mobile']
    dob = request.form['dob']
    new_password = generate_password_hash(request.form['new_password'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND mobile=? AND dob=?",
                   (username, mobile, dob))

    if not cursor.fetchone():
        conn.close()
        return render_template('index.html', error="Details not matched!")

    cursor.execute("UPDATE users SET password=? WHERE username=?",
                   (new_password, username))
    conn.commit()
    conn.close()

    return render_template('index.html', success="Password updated successfully!")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)