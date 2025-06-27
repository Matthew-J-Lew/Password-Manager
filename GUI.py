#GUI.py
#This file creates the entire front end of the project
#Most of the future optimizations for the project can be made here
import sys
import backend
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

#This window is only created if the user needs to set a master password
class FirstTimeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nextWindow = MainWindow()
        #First Window
        self.setWindowTitle("Password Manager")
        self.setFixedSize(300,125)
        #First text box
        self.message = QLabel()
        self.message.setText("Please set your master password")
        font = self.message.font()
        font.setPointSize(15)
        self.setFont(font)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Input field
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Enter button
        self.button = QPushButton()
        self.button.setText("Enter")
        self.button.clicked.connect(self.button_click)
        #setting up window
        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.input)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    #Button click function
    def button_click(self):
        #Takes whatever is in the input field, encrypts it, and sets it as the master password and displays the next window
        password = self.input.text()
        backend.encryptPassword(password)
        self.nextWindow.show()
        self.close()

#The first window that users will see when they launch the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nextWindow = PasswordDisplayWindow()
        #First Window
        self.setWindowTitle("Password Manager")
        self.setFixedSize(300,125)
        #First text box
        self.message = QLabel()
        self.message.setText("Please input master password")
        font = self.message.font()
        font.setPointSize(15)
        self.setFont(font)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Input field
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Enter button
        self.button = QPushButton()
        self.button.setText("Enter")
        self.button.clicked.connect(self.button_click)
        #setting up window
        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.input)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    #Button click function
    def button_click(self):
        #Checks what is in the input field and checks if it is correct
        password = self.input.text()
        self.input.setText("")
        #If it is correct show the next window
        if backend.passwordCheck(password):
            self.nextWindow.show()
            self.close()
        #Else show an error message
        else:
            self.wrongPassword()
    #Creating error message
    def wrongPassword(self):
        popUp = QMessageBox.critical(self,"Error", "Wrong Password",
                                     buttons=QMessageBox.StandardButton.Ok,
                                     defaultButton=QMessageBox.StandardButton.Ok)

#This is the window that displays the actual database for users
class PasswordDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Database")
        self.setFixedSize(600,400)
        #top label
        self.message = QLabel()
        self.message.setText("Your Passwords")
        font = self.message.font()
        font.setPointSize(15)
        self.message.setFont(font)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Table - need to find a way to add editable and selectable flags
        self.table = QTableWidget(self.getNumRows(),3)
        self.table.setMinimumSize(580,250)
        self.table.setColumnWidth(0,0)
        self.table.setColumnWidth(1,200)
        self.table.setColumnWidth(2,340)
        self.table.hideColumn(0)
        self.table.setHorizontalHeaderLabels(["ID","Platform","Password"])
        self.loadTableData()
        #Making contents of layout 2
        self.addingButton = QPushButton()
        self.addingButton.setText("Add Entry")
        self.addingButton.clicked.connect(self.addButtonIsPressed)
        self.message2 = QLabel()
        self.message2.setText("Enter Platform ")
        self.message2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Making contents of layout 3
        self.deletingButton = QPushButton()
        self.deletingButton.setText("Delete Entry")
        self.deletingButton.clicked.connect(self.deleteButtonIsPressed)
        self.input2 = QLineEdit()
        self.input2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message3 = QLabel()
        self.message3.setText("Enter Password")
        self.message3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Adding all the layouts together
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.message)
        mainLayout.addWidget(self.table)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.addingButton)
        layout2.addWidget(self.message2)
        layout2.addWidget(self.input)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.deletingButton)
        layout3.addWidget(self.message3)
        layout3.addWidget(self.input2)
        #Creating full window
        mainLayout.addLayout(layout2)
        mainLayout.addLayout(layout3)
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    #Converting from an sqlite database and then adding each element to the rows of the table
    def loadTableData(self):
        database = backend.loadDatabase()
        #Creating an sql query to select the correct items in the database
        cursor = database.cursor()
        cursor.execute("SELECT * from MANAGER")
        tableRow = 0
        for row in cursor:
            self.table.setItem(tableRow, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(tableRow, 1, QTableWidgetItem(row[1]))
            self.table.setItem(tableRow, 2, QTableWidgetItem(row[2]))
            tableRow += 1
    #Returns number of rows in the database through an sql query, used to create the table in the GUI
    def getNumRows(self):
        database = backend.loadDatabase()
        cursor = database.cursor()
        cursor.execute("SELECT COUNT(*) FROM MANAGER")
        numRows = list(cursor)[0][0]
        cursor.close()
        database.close()
        return numRows
    #Add button function
    def addButtonIsPressed(self):
        database = backend.loadDatabase()
        platform = self.input.text()
        password = self.input2.text()
        if not backend.inDatabase(database, platform, password):
            backend.addToDatabase(database, platform, password)
            backend.storeDatabase(database)
            self.input.setText("")
            self.input2.setText("")
        else:
            self.errorMessage("Item is already in database")
    #Delete button function
    def deleteButtonIsPressed(self):
        database = backend.loadDatabase()
        platform = self.input.text()
        password = self.input2.text()
        if backend.inDatabase(database, platform, password):
            backend.delFromDatabase(database, platform, password)
            backend.storeDatabase(database)
            self.input.setText("")
            self.input2.setText("")
        else:
            self.errorMessage("Item already not in database")
    #defining error message
    def errorMessage(self, Message):
        popUp = QMessageBox.critical(self, "Error", Message,
                                     buttons=QMessageBox.StandardButton.Ok,
                                     defaultButton=QMessageBox.StandardButton.Ok)
#Calling window function to start each new window
def callWindow(window):
    GUI = QApplication(sys.argv)
    myWindow = window()
    myWindow.show()
    #starts main loop
    GUI.exec()
