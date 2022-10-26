#PASSWORD MANAGER
#BY: Matthew Lew
#Contact: matthew.lew008@gmail.com
#The purpose of this project is to store and encrypt user passwords into an sqlite database
#and allow users to add and delete entries using the GUI
#The code is primarily split into the backend.py file and the GUI.py file that handle the back and front end respectively

#Impoting other py files
import backend
import GUI

#Future planned updates
#TODO:
# 1. Confirm Password Screen
# 2. Text to * for passwords
# 3. Add delete and change password buttons in each row
# 4. Update the table upon changing data

#Main function that checks if it is the user's first time using the application
if __name__ == '__main__':

    if backend.isFirstTime():
        GUI.callWindow(GUI.FirstTimeWindow)
    else:
        GUI.callWindow(GUI.MainWindow)