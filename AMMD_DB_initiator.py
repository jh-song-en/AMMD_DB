import sys
import os
import time
import json
import subprocess
import copy

# PyQt5 Libraries
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import re
import mysql.connector as sql
from mysql.connector.locales.eng import client_error

import docker


class main_form(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # Setting the position and size of the UI
        self.ui = uic.loadUi(os.path.abspath('source/main_form.ui'), self)
        # Error dialog
        self.error_dialog = QtWidgets.QErrorMessage()

        self.group = QButtonGroup()

        self.group.addButton(self.radio_manager)
        self.group.addButton(self.radio_researcher)
        self.group.addButton(self.radio_visitor)
        self.user_modification_mode = 0

        # Connection info
        self.docker_running_check()

        self.ui.show()

    def docker_running_check(self):
        client = docker.from_env()
        container_list = client.containers.list()
        current_server = [container.attrs["Name"] for container in container_list]
        client.close
        ammd_db_server_list = ['/ammd_db_mysql', '/ammd_db_sftp']
        current_page = 1
        for server in ammd_db_server_list:
            if server not in current_server:
                self.stackedWidget.setCurrentIndex(0)
                current_page = 0

        if current_page == 1:
            self.stackedWidget.setCurrentIndex(1)

            server_status_dict = {}
            for container in container_list:
                attr = container.attrs
                name = attr["Name"]
                try:
                    port = list(attr["HostConfig"]["PortBindings"].values())[0][0]["HostPort"]
                except:
                    port = 0

                server_status_dict[name] = port
            self.mysql_port_label.setText(str(server_status_dict["/ammd_db_mysql"]))
            self.sftp_port_label.setText(str(server_status_dict["/ammd_db_sftp"]))

    def env_file_generation(self):
        self.mysql_port = self.mysql_port_edit.text()
        self.sftp_port = self.sftp_port_edit.text()

        file_path = os.path.abspath('.env')
        content = "MYSQL_PORT=" + self.mysql_port + "\n"
        content += "SFTP_PORT=" + self.sftp_port + "\n"

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

            content = content.replace(b'\r\n', b'\n')
            with open(file_path, 'wb') as open_file:
                open_file.write(content)

            subprocess.run(["Docker", "compose", "down"])
            subprocess.run(["Docker", "compose", "up", "-d"])
            subprocess.run(["Docker", "exec", "-it", "ammd_db_mysql", "python3", "/home/system_config/initialfunc.py"])
            # ("docker exec -it ammd_db_mysql /bin/bash /home/backup/backup.sh " + self.mysql_password)

            self.docker_running_check()

            self.showDialog("Server initiated")
        except:
            self.error_dialog.showMessage(str(sys.exc_info()))
            subprocess.run(["Docker", "compose", "down"])

    """
    ####################################################################################################################
    server_check_page 
    ####################################################################################################################
    """

    def user_button_clicked(self):
        self.stackedWidget.setCurrentIndex(2)
        self.get_user_list()

    """
    ####################################################################################################################
    user 
    ####################################################################################################################
    """
    def user_cancel_button_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
        del self.user_dict
        del self.user_dict_change

    def get_user_list(self):
        with open(os.path.abspath('sftp/system_config/users.conf'), "r") as f:
            user_file_read = f.read().split('\n')
            user_list = [user.split(":") for user in user_file_read if user]

            anom_dict = {}
            for user in user_list:
                anom_dict[user[0]] = {"encrypted_password": user[1], "temp_password": user[2], "user_number": user[3],
                                      "user_permission": user[4]}
            self.user_dict = anom_dict
            self.user_dict_change = copy.deepcopy(anom_dict)

            self.browse_user_list()

    def browse_user_list(self):
        user_name_list = self.user_dict_change.keys()
        model = QtGui.QStandardItemModel()
        self.user_list_view.setModel(model)
        for i in user_name_list:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)

    def delete_user_button_click(self):
        try:
            index = self.user_list_view.selectionModel().selectedIndexes()
            user_name = self.user_list_view.model().itemData(index[0])[0]
            del self.user_dict_change[user_name]
            self.browse_user_list()
        except IndexError:
            pass

    def add_user_button_click(self):
        self.user_modification_mode = 2
        self.reset_user_config_setting_edits()
        self.user_config_setting_edits_set_enabled(True)

    def user_list_view_double_clicked(self):
        self.user_modification_mode = 1
        self.reset_user_config_setting_edits()
        self.user_config_setting_edits_set_enabled(True)
        self.user_id_edit.setEnabled(False)
        try:
            index = self.user_list_view.selectionModel().selectedIndexes()
            user_name = self.user_list_view.model().itemData(index[0])[0]
            self.user_id_edit.setText(user_name)
            user_permission = self.user_dict_change[user_name]["user_permission"]
            if user_permission == "0":
                self.radio_manager.setChecked(True)
            if user_permission == "50":
                self.radio_researcher.setChecked(True)
            if user_permission == "100":
                self.radio_visitor.setChecked(True)
        except IndexError:
            pass

    def user_config_setting_edits_set_enabled(self, boolean):

        self.user_id_edit.setEnabled(boolean)
        self.new_password_edit.setEnabled(boolean)
        self.password_confirm_edit.setEnabled(boolean)
        self.radio_manager.setEnabled(boolean)
        self.radio_researcher.setEnabled(boolean)
        self.radio_visitor.setEnabled(boolean)
        self.user_confirm_button.setEnabled(boolean)

    def reset_user_config_setting_edits(self):
        self.user_id_edit.setText("")
        self.new_password_edit.setText("")
        self.password_confirm_edit.setText("")
        self.group.setExclusive(False)
        self.radio_manager.setChecked(False)
        self.radio_researcher.setChecked(False)
        self.radio_visitor.setChecked(False)
        self.group.setExclusive(True)

    def user_confirm_button_clicked(self):
        if self.user_modification_mode == 0:
            return 0
        else:
            user_id = self.user_id_edit.text()
            new_password = self.new_password_edit.text()
            confirmed_password = self.password_confirm_edit.text()
            if self.user_modification_mode == 1:
                if not (new_password == "" and confirmed_password == ""):
                    ver = self.password_verify(new_password, confirmed_password)
                    if not ver:
                        return 0
            if self.user_modification_mode == 2:  # Add mode

                if user_id in self.user_dict_change.keys():
                    self.showDialog("The user already exists")
                    return 0
                else:
                    if not (re.match("^[a-z0-9]*$", user_id) and len(user_id) >= 5):
                        self.showDialog("The user id must be longer than 5 letters, "
                                        "and include lowercase and numbers only")
                        return 0
                    ver = self.password_verify(new_password, confirmed_password)
                    if not ver:
                        return 0

            if self.radio_manager.isChecked():
                user_permission = "0"  # manager code
            elif self.radio_researcher.isChecked():
                user_permission = "50"  # researcher code
            elif self.radio_visitor.isChecked():
                user_permission = "100"  # visitor code
            else:
                self.showDialog("Select the user permission")
                return 0
        self.add_user_to_user_dict_change(user_id, new_password, user_permission)
        self.reset_user_config_setting_edits()
        self.user_config_setting_edits_set_enabled(False)
        self.browse_user_list()
        print(self.user_dict_change)
        self.user_modification_mode = 0

    def add_user_to_user_dict_change(self, user_id, new_password, user_permission):
        client = docker.from_env()
        byte_string = client.containers.run("python:alpine",
                                            "python -c \"import crypt; print(crypt.crypt('" + new_password + "'))\"",
                                            auto_remove=True)
        encrypted_password = byte_string.decode("utf-8").strip("\n")
        if user_id not in self.user_dict_change.keys():
            self.user_dict_change[user_id] = {}
        if new_password == "":
            pass
        else:
            self.user_dict_change[user_id]["encrypted_password"] = encrypted_password
            self.user_dict_change[user_id]["temp_password"] = new_password

        self.user_dict_change[user_id]["user_permission"] = user_permission
    def user_save_button_clicked(self):
        if self.user_dict == self.user_dict_change:
            return 0
        self.user_save_button.setEnabled(False)
        user_list = list(self.user_dict.keys())
        print(user_list)
        user_list_change = list(self.user_dict_change.keys())
        print(user_list_change)
        delete_user_list = [user for user in user_list if user not in user_list_change]
        new_user_list = [user for user in user_list_change if user not in user_list]
        existing_user_list = [user for user in user_list_change if user in user_list]

        user_dict_altered_password = {user: self.user_dict_change[user] for user in existing_user_list if
                                      self.user_dict_change[user]["temp_password"] != "e"}
        user_dict_altered_permission = {user: self.user_dict_change[user] for user in existing_user_list if
                                        self.user_dict_change[user]["user_permission"] != self.user_dict[user][
                                            "user_permission"]}

        new_user_dict = {user: self.user_dict_change[user] for user in new_user_list}

        user_update = {"del_user": delete_user_list, "user_password": user_dict_altered_password,
                       "user_permission": user_dict_altered_permission, "new_user": new_user_dict}

        user_info_sftp_list = []
        for i in range(len(user_list_change)):
            user = user_list_change[i]
            user_info = self.user_dict_change[user]
            user_number = 1001 + i
            user_info_string = ":".join([user, user_info["encrypted_password"], "e", str(user_number), user_info["user_permission"]])
            user_info_sftp_list.append(user_info_string)

        user_info_sftp_string = "\n".join(user_info_sftp_list)
        content = str.encode(user_info_sftp_string)

        content = content.replace(b'\r\n', b'\n')


        with open(os.path.abspath('mysql/system_config/mysql_user_update.json'), "w") as f:
            json.dump(user_update, f)
        with open(os.path.abspath("sftp/system_config/users.conf"), "wb") as f:
            f.write(content)

        subprocess.run(["Docker", "compose", "down"])
        subprocess.run(["Docker", "compose", "up", "-d"])
        subprocess.run(["Docker", "exec", "-it", "ammd_db_mysql", "python3", "/home/system_config/initialfunc.py"])
        self.get_user_list()

        self.user_save_button.setEnabled(True)


    def server_restart_button_clicked(self):
        subprocess.run(["Docker", "compose", "down"])
        subprocess.run(["Docker", "compose", "up", "-d"])
        subprocess.run(["Docker", "exec", "-it", "ammd_db_mysql", "python3", "/home/system_config/initialfunc.py"])
        self.docker_running_check()

    def password_verify(self, new_password, confirmed_password):
        if new_password != confirmed_password:
            self.showDialog("The password confirmation does not match")
            return False
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, new_password)
        if not mat:
            password_message = """Your password must be have at least:  
        8 to 20 characters long
        1 uppercase & 1 lowercase character
        1 number
        1 Symbolic character (@$!#%*?&)
        """
            self.showDialog(password_message)
            return False
        else:
            return True

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
