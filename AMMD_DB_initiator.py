import sys
import os
import time
import subprocess
# PyQt5 Libraries

from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox

import mysql.connector as sql
from mysql.connector.locales.eng import client_error


class main_form(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # Setting the position and size of the UI
        self.ui = uic.loadUi(os.path.abspath('source/main_form.ui'), self)
        # Error dialog
        self.error_dialog = QtWidgets.QErrorMessage()

        # Connection info
        self.stackedWidget.setCurrentIndex(0)

        self.ui.show()

    def env_file_generation(self):
        self.mysql_port = self.mysql_port_edit.text()
        self.sftp_port = self.sftp_port_edit.text()
        self.mysql_password = self.mysql_password_edit.text()

        file_path = os.path.abspath('.env')
        content = "MYSQL_PORT=" + self.mysql_port + "\n"
        content += "SFTP_PORT=" + self.sftp_port + "\n"
        content += "MYSQL_PASSWORD=" + self.mysql_password

        with open(file_path, 'w') as open_file:
            open_file.write(content)


    def server_initiation(self):
        self.initiate_server.setDisabled(True)
        try:
            # replacement strings
            WINDOWS_LINE_ENDING = b'\r\n'
            UNIX_LINE_ENDING = b'\n'

            self.env_file_generation()

            # relative or absolute file path, e.g.:
            file_path = os.path.abspath("sftp/system_config/users.conf")

            with open(file_path, 'rb') as open_file:
                content = open_file.read()

            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

            with open(file_path, 'wb') as open_file:
                open_file.write(content)

            subprocess.run(["Docker", "compose", "down"])
            subprocess.run(["Docker", "compose", "up", "-d"])
            # ("docker exec -it ammd_db_mysql /bin/bash /home/backup/backup.sh " + self.mysql_password)

            self.showDialog("Server initiated")
        except:
            self.error_dialog.showMessage(str(sys.exc_info()))
            subprocess.run(["Docker", "compose", "down"])



    def showDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Message Box")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            return True
        else:
            return False
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = main_form()

    sys.exit(app.exec())
