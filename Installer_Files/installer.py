#!/usr/bin/env python2.7
"""
This module contains the OnTrack Installer user interface and main function.
----------
The OnTrack distribution folder, created using PyInstaller, is stored in the
zipped file OnTrack_zipped.zip. An installer dialog lets the user select the
install folder into which the OnTrack distribution folder is unzipped. A
shortcut is made for the PATH/TO/FOLDER/OnTrack/OnT.exe file that launches the
application and it is moved to the user's desktop. The Qt framework is used for
both the installer and for OnTrack's user interface.
----------
Module Components
    TITLE_FONT: QFont object for the title font
    MSG_FONT: QFont object for the message font
    TAG_FONT: QFont object for the installation directory tag
    DIR_FONT: QFont object for the installation directory path
    BUTTON_FONT: QFont object for INSTALL button text
    BUTTON_STYLE: CSS for INSTALL button
    FRAME_STYLE: CSS for window frames
    resource_path: function to return the path to a resource file
    delete_conf: deletes the qt.conf file that is created by the installer
    InstallerDialog: QMainWindow subclass to display an installer window
    main: function to run the installer
"""


import os
import sys
import winshell
import zipfile

from PyQt4 import QtCore
from PyQt4 import QtGui

import icons

TITLE_FONT = QtGui.QFont()
TITLE_FONT.setFamily("Tahoma")
TITLE_FONT.setPointSize(18)
TITLE_FONT.setWeight(75)

MSG_FONT = QtGui.QFont()
MSG_FONT.setFamily("Tahoma")
MSG_FONT.setPointSize(10)

TAG_FONT = QtGui.QFont()
TAG_FONT.setFamily("Tahoma")
TAG_FONT.setPointSize(10)
TAG_FONT.setWeight(75)

DIR_FONT = QtGui.QFont()
DIR_FONT.setFamily("Tahoma")
DIR_FONT.setPointSize(9)

BUTTON_FONT = QtGui.QFont()
BUTTON_FONT.setFamily("Arial")
BUTTON_FONT.setPointSize(16)

BUTTON_STYLE = "".join([
    "QToolButton {\nbackground-color: qlineargradient(spread:pad, ",
    "x1:0.522, y1:0, x2:0.527, y2:1, stop:0 rgba(215, 255, 249, 255), ",
    "stop:1 rgba(187, 246, 248, 255));\nborder: 1px solid black;\n}\n\n",
    "",
    "QToolButton:hover {\nbackground-color: qlineargradient(spread:reflect, ",
    "x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(173, 255, 119, 255), ",
    "stop:1 rgba(217, 255, 169, 255));\nborder: 2px solid rgb(60, 127, 177)",
    "\n}\n\n",
    "",
    "QToolButton:pressed:hover {\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.508, y1:0, x2:0.512, ",
    "y2:1, stop:0 rgba(48, 215, 243, 255), stop:1 rgba(86, 255, ",
    "231, 255));\n}\n\n",
    "",
    "QToolButton:disabled {\nbackground-color: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 ",
    "rgba(109, 148, 161, 255), stop:1 rgba(171, 196, 207, 255));\n}"])

FRAME_STYLE = "".join([
    "QFrame#bg {\nbackground-color:white;\n}\n\n",
    "",
    "QFrame#title {\nbackground-color: rgb(155, 255, 5);\n",
    "border: 1px solid black;\n}"])


def resource_path(relative):
    """
    Return the resource path for a file packaged with the installer.

    This code was found in multiple online sources, used by other programmers
    using PyInstaller. This function returns the path of a file that has been
    packaged in a one-file executable.

    :param relative: File name
    :type relative: str
    :return: Path to the file
    :rtype: str
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def delete_conf():
    """Delete the qt.conf file that is mysteriously created."""
    try:
        os.remove(os.path.join(os.getcwd(), "qt.conf"))
    except OSError:
        pass


class Installer(QtGui.QMainWindow):
    """
    Class to display an OnTrack Installer window.

    Installer creates a QMainWindow which lets the user select an installation
    directory and install OnTrack onto their hard drive. The OnTrack_zipped
    file packaged with this one-file installer is unzipped into the selected
    directory. The zippath attribute stores the resource path to this zipped
    distribution folder. The install_dir attribute stores the installation
    directory--default is the Windows user profile folder. Methods are
    implemented to change the selected directory, unzip the distribution folder
    into the directory, and create a shortcut to the OnTrack executable file
    on the user's desktop.
    """

    def __init__(self):
        """
        Initialize an InstallDialog object.

        Assigns the 'OnTrack_zipped.zip' resource path to the zippath
        attribute and the user's Windows user profile directory to the
        install_dir attribute. Calls setup_ui to build user interface
        components and connect signals to slots.
        """
        QtGui.QMainWindow.__init__(self)
        self.zippath = resource_path("OnTrack_zipped.zip")
        self.install_dir = os.path.join(os.environ["USERPROFILE"])
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Window properties.
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        width, height = 800, 400
        self.setFixedSize(width, height)
        self.setWindowTitle("RER3 Software")
        apple_icon = QtGui.QIcon()
        apple_icon.addPixmap(
            QtGui.QPixmap(":/icons/apple.ico"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.setWindowIcon(apple_icon)
        central = QtGui.QWidget(self)
        self.setCentralWidget(central)
        bg_frame = QtGui.QFrame(central)
        bg_frame.setGeometry(0, 0, width, height)
        bg_frame.setStyleSheet(FRAME_STYLE)
        bg_frame.setObjectName("bg")
        # Title and message.
        title_frame = QtGui.QFrame(bg_frame)
        title_frame.setGeometry(0, 0, width, 66)
        title_frame.setObjectName("title")
        title_tag = QtGui.QLabel(title_frame)
        title_tag.setGeometry(10, 8, width - 20, 50)
        title_tag.setAlignment(QtCore.Qt.AlignCenter)
        title_tag.setFont(TITLE_FONT)
        title_tag.setText("OnTrack Installer")
        message = QtGui.QLabel(bg_frame)
        message.setGeometry(10, 86, width - 20, 26)
        message.setAlignment(QtCore.Qt.AlignCenter)
        message.setFont(MSG_FONT)
        message.setText(
            "The OnTrack app requires 100 MB of space. Select an " +
            "installation directory and click INSTALL.")
        # Installation directory components.
        dir_frame = QtGui.QFrame(self)
        dir_frame.setGeometry(10, 140, width - 20, 80)
        dir_frame.setFrameShape(QtGui.QFrame.Box)
        dir_tag = QtGui.QLabel(self)
        dir_tag.setGeometry(20, 126, 190, 26)
        dir_tag.setAlignment(QtCore.Qt.AlignCenter)
        dir_tag.setFont(TAG_FONT)
        dir_tag.setStyleSheet("QLabel { background-color: white; }")
        dir_tag.setText("Installation Directory")
        self.dir_text = QtGui.QPlainTextEdit(self)
        self.dir_text.setGeometry(20, 166, 600, 30)
        self.dir_text.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.dir_text.insertPlainText(self.install_dir)
        self.dir_text.moveCursor(QtGui.QTextCursor.Start)
        self.dir_text.setFont(DIR_FONT)
        self.dir_text.setStyleSheet(
            "QPlainTextEdit { border: 0px solid black; }")
        self.dir_text.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        if len(self.dir_text.toPlainText()) > 70:
            self.update_text_geom()
        self.browse_bn = QtGui.QToolButton(self)
        self.browse_bn.setGeometry(670, 160, 110, 40)
        self.browse_bn.setText("Browse...")
        # Install button.
        self.install_bn = QtGui.QToolButton(self)
        self.install_bn.setGeometry(310, 300, 180, 60)
        self.install_bn.setFont(BUTTON_FONT)
        self.install_bn.setStyleSheet(BUTTON_STYLE)
        self.install_bn.setText("INSTALL")
        # Installing and Complete messages.
        self.installing_msg = QtGui.QLabel(self)
        self.installing_msg.setGeometry(10, 312, 780, 30)
        self.installing_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.installing_msg.setFont(BUTTON_FONT)
        self.installing_msg.setText(
            "Decompressing files into your installation directory...")
        self.installing_msg.hide()
        self.complete_msg = QtGui.QLabel(self)
        self.complete_msg.setGeometry(10, 312, 780, 30)
        self.complete_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.complete_msg.setFont(BUTTON_FONT)
        self.complete_msg.setText("Installation Complete!")
        self.complete_msg.hide()
        # Connect signals to slots.
        self.browse_bn.clicked.connect(self.change_directory)
        self.install_bn.clicked.connect(self.install_application)
        # Delete qt.conf.
        delete_conf()

    def update_text_geom(self):
        """Update the dir_text attribute's geometry based on its text."""
        if self.dir_text.horizontalScrollBar().maximum() > 0:
            self.dir_text.setGeometry(20, 156, 600, 50)
        else:
            self.dir_text.setGeometry(20, 166, 600, 30)

    def change_directory(self):
        """Change the installation directory."""
        new_dir = str(
            QtGui.QFileDialog.getExistingDirectory(
                self, "Select Installation Directory", self.install_dir,
                QtGui.QFileDialog.ShowDirsOnly |
                QtGui.QFileDialog.DontResolveSymlinks))
        if new_dir != "":
            self.install_dir = new_dir
            self.dir_text.clear()
            self.dir_text.insertPlainText(self.install_dir)
            self.dir_text.moveCursor(QtGui.QTextCursor.Start)
            self.update_text_geom()

    def install_application(self):
        """Unzip the OnTrack distribution folder into the installation dir."""
        try:
            # Check for install verification.
            choice = QtGui.QMessageBox.question(
                self, "Confirm Install OnTrack",
                "Install OnTrack into the selected directory?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.No:
                return
            # Check for OnTrack folder.
            if os.path.isdir(os.path.join(self.install_dir, "OnTrack")):
                QtGui.QMessageBox.warning(
                    self, "OnTrack Folder Exists",
                    "There is already an 'OnTrack' folder in this directory!")
                return
            # Show processing message (process events to show it).
            self.install_bn.hide()
            self.installing_msg.setVisible(True)
            QtGui.QApplication.processEvents()
            # Unzip file.
            with zipfile.ZipFile(self.zippath, "r") as zip_temp:
                zip_temp.extractall(self.install_dir)
            # Process events to make sure files are unzipped, create Users dir,
            # hide Installing Message and create shortcut.
            QtGui.QApplication.processEvents()
            try:
                userspath = os.path.join(self.install_dir, "OnTrack", "Users")
                os.mkdir(userspath)
            except OSError:
                pass
            self.installing_msg.hide()
            self.create_shortcut()
        except (OSError, WindowsError):
            QtGui.QMessageBox.warning(
                self, "Unauthorized Directory",
                "You do not have permission to install here!")
            self.installing_msg.hide()
            self.install_bn.setVisible(True)

    def create_shortcut(self):
        """Create a shortcut to the OnT executable file and exit installer."""
        self.complete_msg.setVisible(True)
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        shortcut_path = os.path.join(desktop_path, "OnTrack.lnk")
        file_path = os.path.join(self.install_dir, "OnTrack", "OnT.exe")
        icon_path = os.path.join(
            self.install_dir, "OnTrack", "ReferenceSource", "apple.ico")
        winshell.CreateShortcut(
            Path=shortcut_path, Target=file_path, Icon=(icon_path, 0))
        # Display success message and exit the installer dialog.
        QtGui.QMessageBox.information(
            self, "OnTrack Installed",
            "OnTrack has been successfully installed and a shortcut " +
            "has been added to your desktop!")
        sys.exit(0)


def main():
    """Run the OnTrack Installer."""
    app = QtGui.QApplication(sys.argv)
    gui = Installer()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
