#Backend.py
#This file handles the encryption and storage of the sqlite database
#Functions from this file are used in both PasswordManager.py and GUI.py

#Imports
from cryptography.fernet import Fernet
import os
import sqlite3

#Setup constants and make sure data folder exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
MASTER_PASSWORD_PATH = os.path.join(DATA_DIR, 'masterPassword.txt')
MANAGER_KEY_PATH = os.path.join(DATA_DIR, 'managerKey.key')
MASTER_KEY_PATH = os.path.join(DATA_DIR, 'masterKey.key')
PASSWORDS_DB_PATH = os.path.join(DATA_DIR, 'passwords.db')

#This file checks if there are any missing files and creates them if theyre missing
#Returns True if the user has a master password set, else returns False
def isFirstTime():
    #Checking each necessary file, if it does not exist create it
    if not os.path.exists(MASTER_PASSWORD_PATH):
        if not os.path.exists(MANAGER_KEY_PATH):
            generateKey(MANAGER_KEY_PATH)
        if not os.path.exists(MASTER_KEY_PATH):
            generateKey(MASTER_KEY_PATH)
        if not os.path.exists(PASSWORDS_DB_PATH):
            connection = sqlite3.connect(PASSWORDS_DB_PATH)
            connection.execute('''CREATE TABLE MANAGER
                                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    PLATFORM        TEXT,
                                    PASSWORD        TEXT);''')
            storeDatabase(connection)
        return True
    else:
        return False

#Functions to handle keys for encryption
def generateKey(fileName):
    newKey = Fernet.generate_key()
    with open(fileName, 'wb') as myKey:
        myKey.write(newKey)
#Next 2 functions can be compiled into one, just need to implement proper passing of parameters
def loadPassKey():
    with open(MASTER_KEY_PATH,"rb") as myKey:
        return myKey.read()
def loadKey():
    with open(MANAGER_KEY_PATH,'rb') as myKey:
        return myKey.read()

#These next two functions are solely for encrypting and decrypting the user's master password, it's existence is redundant however
#and will be replaced by store and load database once the proper formatting for passing parameters is implemented
def encryptPassword(password):
    #Casts the password to byte format
    b= str.encode(password)
    fernet = Fernet(loadPassKey())
    with open(MASTER_PASSWORD_PATH,'wb') as myFile:
        temp = fernet.encrypt(b)
        myFile.write(temp)
def decryptPassword():
    #Decrypting password
    fernet = Fernet(loadPassKey())
    with open(MASTER_PASSWORD_PATH,'rb') as myFile:
        encryptedPassword = myFile.read()
        decryptedPassword = fernet.decrypt(encryptedPassword)
        decryptedPassword = decryptedPassword.decode('utf-8')
        return decryptedPassword

#Function that checks if the given password entered by the user is correct
def passwordCheck(password):
    return decryptPassword() == password

#Next two functions encrypt and decrypt the passwords.db file
def encryptDatabase(database):
    fernet = Fernet(loadKey())
    return fernet.encrypt(database)
def decryptDatabase(encryptedDataBase):
    fernet = Fernet(loadKey())
    return fernet.decrypt(encryptedDataBase)

#Loads database from the encrypted file into an actual sqlite database, it is loaded into memory
#to ensure that no temp files can be accessed for the decrypted passwords
def loadDatabase():
    #Opening file
    with open(PASSWORDS_DB_PATH,'rb') as myFile:
        encryptedFile = myFile.read()
    #Decrypting it from byte form
    decryptedFile = decryptDatabase(encryptedFile)
    decryptedFile = decryptedFile.decode('utf-8')
    database = sqlite3.connect(':memory:')
    database.executescript(decryptedFile)
    return database

#Stores and encrypts database
def storeDatabase(database):
    #Converts to byte form
    b=b''
    #properly formatting each line of the database
    for line in database.iterdump():
        b += bytes('%s\n','utf8') % bytes(line,'utf8')
    #Encrypting and writing the file
    with open(PASSWORDS_DB_PATH,'wb') as myFile:
        temp = encryptDatabase(b)
        myFile.write(temp)

# Function to check if an item with the given platform and password exists in the given database
def inDatabase(database, platform, password):
    # Creating a cursor to loop through the database and creating the query to give to SQLite
    cursor = database.cursor()
    cursor.execute("SELECT id, platform, password from MANAGER")
    # Looping through database and comparing it to given values
    for row in cursor:
        if platform == row[1] and password == row[2]:
            return True
    # If item is not found, return False
    return False

def addToDatabase(database, platform, password):
    # Function to add an item to the table, the query is given to SQLite as:
    # "INSERT INTO MANAGER (PLATFORM, PASSWORD) VALUES (platform, password)"
    if not inDatabase(database, platform, password):
        database.execute("INSERT INTO MANAGER (PLATFORM, PASSWORD) VALUES (\'" + platform + "\', \'"  + password + "\')")

def delFromDatabase(database, platform, password):
    # Function to delete an item from the table, the query is given to SQLite as:
    # "DELETE FROM MANAGER WHERE PLATFORM = platform AND PASSWORD = password"
    if inDatabase(database, platform, password):
        database.execute("DELETE FROM MANAGER WHERE PLATFORM = \'" + platform + "\' AND PASSWORD = \'" + password + "\';")

#Prints database, never used in main but used for testing reasons
def printDatabase(database):
    cursor = database.cursor()
    cursor.execute("SELECT id, platform, password from MANAGER")
    for row in cursor:
        print("ID = ", row[0])
        print("PLATFORM = ", row[1])
        print("PASSWORD = ", row[2])
