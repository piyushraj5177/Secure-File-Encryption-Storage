# 🔐 Secure File Storage System

## 📌 Project Overview
The Secure File Storage System is a web-based application developed using Python that ensures safe and secure storage of user files. The system uses encryption techniques (Fernet) to protect files from unauthorized access and provides a user-friendly interface for file management.

---

## 🚀 Features
- User Authentication (Login & Registration)
- Secure Password Hashing
- File Upload & Storage
- File Encryption & Decryption
- Download Files (Encrypted / Decrypted)
- File Deletion
- Password Reset System
- User Management

---

## 🛠️ Tech Stack
- Backend: Python
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Encryption: Cryptography (Fernet)
- Security: Werkzeug (Password Hashing)

---

## ⚙️ System Requirements

### Hardware
- Minimum 4GB RAM
- Intel i3 or above
- 500GB Storage

### Software
- Python 3.x
- SQLite
- VS Code / PyCharm
- Web Browser (Chrome / Edge / Firefox)

---

## 🧠 Working Principle
- User registers and logs into the system.
- Files uploaded by the user are encrypted before storage.
- Stored files remain unreadable without decryption.
- On download, user can choose encrypted or decrypted file (after password verification).

---

## 🏗️ System Architecture
The system follows a 3-layer architecture:
1. Presentation Layer: Frontend (HTML, CSS, JavaScript)
2. Application Layer: Backend (Python)
3. Data Layer: Database + File Storage

---

## 📂 Project Structure
Secure-File-Storage/
│
├── app.py
├── database.db
├── secret.key
├── encrypted_files/
├── templates/
│   └── index.html
└── static/

---

## ▶️ How to Run the Project

1. Clone the repository:
git clone https://github.com/your-username/secure-file-storage.git

2. Navigate to the folder:
cd secure-file-storage

3. Install dependencies:
pip install cryptography werkzeug

4. Run the application:
python app.py

5. Open in browser:
http://127.0.0.1:5000/

---

## 🔍 Key Functionalities

### Authentication
- Secure login using hashed passwords
- Session management for users

### File Handling
- Upload files → automatically encrypted
- Download files → encrypted or decrypted
- Delete files securely

### Encryption
- Uses Fernet symmetric encryption
- Secret key stored locally

---

## 📊 Results
- Successfully implemented secure file storage system
- Prevents unauthorized access
- Ensures data confidentiality and integrity
- Smooth and efficient performance

---

## ✅ Advantages
- Strong data security
- Easy to use interface
- Lightweight system
- Efficient performance

---

## ⚠️ Limitations
- Local storage only (no cloud)
- Limited scalability
- No multi-factor authentication

---

## 🔮 Future Scope
- Cloud integration (AWS / Google Drive)
- Multi-user file sharing
- Advanced authentication
- Mobile application version
- Improved UI/UX

---

## 🏁 Conclusion
This project demonstrates a practical implementation of a secure file storage system using encryption techniques. It ensures data protection through authentication and encryption mechanisms and serves as a strong foundation for future applications.

---

## 📚 References
- Python Cryptography Library
- SQLite Documentation
- Online Tutorials
## 👨‍💻 Author
Piyush Raj  
Electronics & Computer Science Engineering Student
