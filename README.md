# 🔐 Password Manager
This Password Manager application securely stores and encrypts user passwords in an SQLite database. Users can easily add and delete password entries through a graphical user interface (GUI).

---

## 📋 Overview
The project is split into two main components:

- `backend.py`: Handles encryption, decryption, and database management.
- `GUI.py`: Implements the PyQt6-based graphical interface.

The main executable script is `PasswordManager.py`, which manages the application flow.

---

## ✨ Features

- Secure encryption of stored passwords using the `cryptography` library (Fernet symmetric encryption).
- Password storage in an encrypted SQLite database.
- GUI for easy password entry and deletion.
- Automatic creation of necessary keys and encrypted files on first run.

---

## 🛠️ Technologies Used

- Python 3
- SQLite3
- [cryptography](https://cryptography.io/en/latest/)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)

---

## 🚀 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
---

## ▶️ Usage

Run the application:
    ```bash
    python PasswordManager.py
    ```
- On first launch you'll be prompted to set a master password.
- On subsequent launches, enter your master password to access the stored passwords.
- Use the GUI to add or delete password entries.

---

## 🛠️ Future Enhancements

- Confirm password screen when setting a new master password.
- Mask passwords with asteriks (*) in the GUI and a reveal password button.
- Add buttons to delete or change passwords directly within the table.
- Automatically update the password table when changes are made.

---

## 📄 License
This project is released under the MIT License.



