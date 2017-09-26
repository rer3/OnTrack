#!/usr/bin/env python2.7
"""
This module contains classes to manage local app and user data.
----------
These classes read and write local file data. All data files created by the
OnTrack runtime environment are saved in JSON format. The OnTrack parent
directory contains the following files and folders:

OnTrack
|-ReferenceSource
  |-apple.ico
  |-AppState.json
  |-ExerciseDetails.json
  |-FoodDetails.json
  |-FoodNutrients.json
|-Users
  |-<USERNAME> (specific user directory)
    |-ExerciseDetails.json
    |-FoodDetails.json
    |-FoodNutrients.json
    |-Profile.json
    |-Records.json
    |-Settings.json
    |-Templates.json
|... (All other files and folders built by PyInstaller)

The files and folders built by PyInstaller are all dependencies packaged with
the original 9 Ontrack modules: __init__, album, dna, organs, body, brain,
ears, eyes, and face. The file apple.ico is the application icon. The
application state contains a dictionary with the following data:

    'created': <datetime.date string>
    'default': <default username string>
    'users': <list of active username strings>
    'version': <version number string>

When a new active user is created by the application, a <USERNAME> directory is
created in the Users directory. All files shown above under <USERNAME> are
created in their default state. The files containing Exercise Details, Food
Details, and Food Nutrients are copied from the ReferenceSource directory so
that all new users begin with the same reference data. The files containing
the user's profile, records, and templates are created with empty data
containers. Settings.json is created with default application settings.

The ReferenceFileCreator class is a QThread subclass written for a future
version of OnTrack that will implement a feature to recreate reference files if
they are deleted or source data is updated. Components from this class's run
method were used to create the initial Exercise Details, Food Details, and Food
Nutrients reference files. These files are packaged with the OnTrack executable
in the zipped distribution folder. Both the executable and distribution folder
were created with PyInstaller.
----------
Local Data Management: classes to manage local data files.
    AppState: class to manage the application state file
    User: class to manage user data files

Source Data Creator: class to build reference data files found in the
ReferenceSource directory.
    ReferenceFileCreator: QThread subclass to build initial reference files
"""


import contextlib
import datetime
import json
import os
import shutil
import sys
import urllib2

from PyQt4 import QtCore
from PyQt4 import QtGui
import ujson

import dna
import body
import organs


# -----------------------------------------------------------------------------
# Local Data Management -------------------------------------------------------

class AppState:
    """
    Class to access and modify the the app state file AppState.json.

    AppState reads the local app state file, AppState.json, stores its
    properties in the _state attribute, modifies the properties when directed
    to do so by the application, and writes over the app state file with the
    modified data. Additional attributes are implemented to store the
    QMainWindow parent (the GUI) and the AppState.json file path. Methods are
    implemented to load the current app state data into the _state attribute,
    check the app state for inconsistencies or an invalid state when AppState
    is instantiated, change app state properties, and overwrite AppState.json
    when changes are made.
    """
    def __init__(self, parent):
        """
        Initialize an AppState object.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        """
        self._parent = parent
        self._path = os.path.join(sys.path[0], dna.REF_DIR, "AppState.json")
        self._state = {}
        self.load_state()
        self.check_state()

    def load_state(self):
        """
        Load the app state data into the _state attribute.

        Assigns the AppState.json file data to the _state attribute. If the
        file is not found, an app state file is created with the default state.
        If a state file is not found and cannot be created, the application is
        closed.
        """
        try:
            with open(self._path, "r") as state_file:
                self._state = json.load(state_file)
        except IOError:
            try:
                # If the app state is missing, try to create the default
                # file and assign the default state dict to _state attribute.
                default_state = {
                    "created": False, "default": None, "users": [],
                    "version": dna.__version__}
                with open(self._path, "w") as state_file:
                    ujson.dump(default_state, state_file)
                self._state = default_state
            except IOError:
                QtGui.QMessageBox.warning(
                    self._parent, "Critical Error",
                    "The app state file cannot be found in the source " +
                    "folder and it cannot be created! OnTrack is exiting...")
                sys.exit(1)

    def check_state(self):
        """
        Check that the app state is valid and handle inconsistencies.

        Verifies that the 'Users' directory exists in the OnTrack application
        folder, all usernames listed in _state['users'] have directories, and
        all necessary files are located in each username directory. If a user
        directory is found that has not been programmatically added to the
        AppState.json file, it is checked for valid user files. This allows a
        valid user folder to be moved to the 'Users' directory without breaking
        the application. All user directories without the necessary files are
        removed. If a critical error is encountered, the application is closed.

        Attempts to create a Users directory by default each time the state is
        checked. This allows the directory to be deleted without causing a
        critical error when the application is first opened. This step also
        makes it optional, but not required, for the OnTrack installer to
        create a Users directory after it unzips the OnTrack distribution
        folder into the chosen directory.
        """
        userspath = os.path.join(sys.path[0], "Users")
        try:
            os.mkdir(userspath)
        except OSError:
            pass
        try:
            # Check if OnTrack has been 'created' (run for the first time since
            # the AppState.json file was created). If not, set created date.
            if not self._state["created"]:
                today = datetime.datetime.now().date().isoformat()
                self._state["created"] = today
                self.save_state()
            # Determine which user folders are in the Users directory. Point
            # out new and missing users.
            previous_users = self._state["users"]
            current_users = []
            for fname in os.listdir(userspath):
                if os.path.isdir(os.path.join(userspath, fname)):
                    current_users.append(fname)
            new_users = set(current_users) - set(previous_users)
            missing_users = set(previous_users) - set(current_users)
            if new_users:
                new_names = ", ".join([name for name in new_users])
                QtGui.QMessageBox.warning(
                    self._parent, "New User Folders",
                    "New user folders were found. The files in these " +
                    "folders will be validated. New active users are:\n\n" +
                    new_names)
            if missing_users:
                missing = ", ".join([name for name in missing_users])
                QtGui.QMessageBox.warning(
                    self._parent, "Missing User Folders",
                    "Folders for one or more previously active users cannot " +
                    "be found. These active user will be removed:\n\n" +
                    missing)
            # Check for all required files in all current user dirs.
            bad_users = []
            all_fnames = dna.ALL_FILES.values()
            for username in current_users:
                userpath = os.path.join(userspath, username)
                user_filepaths = [
                    os.path.join(userpath, fname) for fname in all_fnames]
                for filepath in user_filepaths:
                    if not os.path.isfile(filepath):
                        bad_users.append(username)
                        break
            # Remove all user dirs without all required files.
            if bad_users:
                bad = ", ".join([name for name in bad_users])
                QtGui.QMessageBox.warning(
                    self._parent, "Invalid User Folders",
                    "One or more files are missing from the following user " +
                    "folders. These user folders will be deleted:\n\n" + bad)
                for username in bad_users:
                    userpath = os.path.join(userspath, username)
                    shutil.rmtree(userpath, ignore_errors=True)
            # Check for all source reference files.
            ref_fnames = dna.REF_FILES.values()
            for fname in ref_fnames:
                refpath = os.path.join(sys.path[0], dna.REF_DIR, fname)
                if not os.path.isfile(refpath):
                    QtGui.QMessageBox.warning(
                        self._parent, "Critical Error",
                        "A reference file has been removed from the source " +
                        "folder! OnTrack is exiting...")
                    sys.exit(1)
            # Update AppState.json users and default user, if necessary.
            good_users = list(set(current_users) - set(bad_users))
            self._state["users"] = sorted(good_users)
            if self._state["default"] not in good_users + [None]:
                    self._state["default"] = None
            self.save_state()
        except (IOError, KeyError, OSError):
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "Something very bad occurred while checking the app state! " +
                "OnTrack is exiting...")
            sys.exit(1)

    def save_state(self):
        """Overwrite the app state file with the current app state data."""
        try:
            with open(self._path, "w") as state_file:
                ujson.dump(self._state, state_file)
        except IOError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file cannot be saved! OnTrack is exiting...")
            sys.exit(1)

    def default_user(self):
        """
        Return the username that is automatically logged in on app start.

        :return: The default username
        :rtype: str
        """
        try:
            return self._state["default"]
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)

    def set_default_user(self, new_default_username=None):
        """
        Set the default username that is logged in when the app is opened.

        :param new_default_username: The new default username to log in or None
        :type new_default_username: str, None
        """
        try:
            if new_default_username is None:
                self._state["default"] = None
            else:
                self._state["default"] = new_default_username
            self.save_state()
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)

    def users(self):
        """
        Return the usernames of all active app users.

        :return: A list of active username strings
        :rtype: list
        """
        try:
            return self._state["users"]
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)

    def add_user(self, new_username):
        """
        Add a new username to the list of active app users.

        The GUI parent manages the validation of new usernames and the creation
        of new User objects (i.e. user folder and files). Users are not added
        to the app state using this method unless validation is successful.

        :param new_username: The username of a new app user
        :type new_username: str
        """
        try:
            self._state["users"].append(new_username)
            self.save_state()
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)

    def remove_user(self, username):
        """
        Remove a username from the list of active app users.

        :param username: The username of an active app user
        :type username: str
        """
        # If user is not found in active users list, the parent QMainWindow
        # will still remove the username from the drop-down and attempt to
        # delete the user directory.
        try:
            self._state["users"].remove(username)
            self.save_state()
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)
        except ValueError:
            QtGui.QMessageBox.warning(
                self._parent, "Missing App User",
                "A problem occurred when attempting to remove this user " +
                "from the app state file! Future application issues may " +
                "occur.")

    def created(self):
        """
        Return the created date.

        :return: The created datetime.date isoformat string
        :rtype: str
        """
        try:
            return self._state["created"]
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)

    def version(self):
        """
        Return the version number.

        :return: The version number string
        :rtype: str
        """
        try:
            return self._state["version"]
        except KeyError:
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "The app state file has been corrupted! OnTrack is exiting...")
            sys.exit(1)


class User:
    """
    Class to access, modify, and update user data files.

    User is used to read local user data files, store and modify data, write
    updates to local user data files, and return specialized data sets that
    are used by the GUI. The user's data is saved to local files Profile.json,
    Records.json, Settings.json, and Templates.json. The user's _data attribute
    references these files, and its default structure is stored in the class
    attribute default_userdata, a dictionary with the format:

        {
            'uprof': {'diary': {}, 'guide': {}},
            'ureco': {'D': {}, 'P': {}},
            'usett': {
                'askdelete': True,
                'askexit': True,
                'buildonly': True,
                'favorites': {
                    'F': [], 'E': [], 'TR': [], 'TM': [], 'TD': [], 'TW': [],
                    'TC': [], 'TP': [], 'RD': [], 'RP': []
                },
                'muscles': dna.MUSCLES,
                'nutrients': dna.GUI_NUTRIENTS,
                'sortid': True,
                'sortup': True
            },
            'utemp': {_id: {} for _id in ['R', 'M', 'D', 'W', 'C', 'P']}
        }

    The default_userdata keys are the same as the analogous file IDs from the
    dna.ALL_FILES dictionary. Profile data include the user's Health Diary and
    Nutrient Guide. Records data include Diet and Program record inventories.
    Settings data include application settings. Templates data include Recipe,
    Meal, Diet, Workout, Cycle, and Program template inventories.

    Attributes are implemented to store the GUI (QMainWindow) parent, username
    string, user path string, a dictionary of file paths mapped to file IDs,
    a dictionary of user data mapped to file IDs, the BuildCenter object which
    allows all build element class objects to access reference inventories,
    build element objects created for each template item, and build element
    objects created for each Diet and Program record. Methods are implemented
    to create, modify, and delete the user's <USERNAME> directory and all files
    contained within. Additional methods return file data, modify profile,
    reference, record, and template data, and overwrite user files.
    """

    default_userdata = {
        "uprof": {"diary": {}, "guide": {}},
        "ureco": {"D": {}, "P": {}},
        "usett": {
            "askdelete": True,
            "askexit": True,
            "buildonly": True,
            "favorites": {
                "F": [], "E": [], "TR": [], "TM": [], "TD": [], "TW": [],
                "TC": [], "TP": [], "RD": [], "RP": []
            },
            "muscles": dna.MUSCLES,
            "nutrients": dna.GUI_NUTRIENTS,
            "sortid": True,
            "sortup": True
        },
        "utemp": {_id: {} for _id in ["R", "M", "D", "W", "C", "P"]}
    }

    def __init__(self, parent, username, new_user=False):
        """
        Initialize a User object.

        Assigns the parent and username args to the _parent and _username
        attributes. Assigns the user's <USERNAME> folder path to the _userpath
        attribute. Assigns empty dicts to the _filepaths, _data,
        _templateobjects, and _recordobjects attributes. Assigns a new
        BuildCenter object to the _buildcenter attribute. Assigns True to the
        _created attribute. This value is checked by the GUI when a new
        username is created before the current app state and Active Username
        Field are updated. If exceptions are raised at any point during user
        creation, False is assigned to the _created attribute and the app state
        and Active Username Field are not updated with a new active user.

        Calls methods to add user file paths to the _filepaths dict. If the
        parameter new_user is assigned True, methods are called to create the
        user directory, copy to it reference files, and create in it the
        remaining user files. Methods are called to load data from the existing
        user files into the _data attribute, as well as to update the
        _buildcenter attribute with the loaded reference inventory data.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param username: The user's username
        :type username: str
        :param new_user: True to create the directory and files for a new user,
            otherwise False
        :type new_user: bool
        """
        self._parent = parent
        self._username = username
        self._userpath = os.path.join(sys.path[0], "Users", self._username)
        self._filepaths = {}
        self._data = {}
        self._templateobjects = {}
        self._recordobjects = {}
        self._buildcenter = body.BuildCenter()
        self._created = True
        # Add file paths before attempting to create new user files.
        self.add_file_paths()
        if new_user:
            self.create_user_directory()
            self.copy_reference_files()
            self.create_user_files()
        # If the user was not created, do not attempt to update data.
        if not self._created:
            return
        # Add user data and update BuildCenter references.
        self.load_file_data()
        self._buildcenter.update_references(
            **{fileid: self._data[fileid] for fileid in dna.REF_FILES})
        # Build template and record objects.
        self.create_template_objects()
        self.create_record_objects()

    def username(self):
        """
        Return the username.

        :return: The username
        :rtype: str
        """
        return self._username

    def was_created(self):
        """Return True if the user was created otherwise return False."""
        return self._created

    # ------------------- DATA MANAGEMENT METHODS -------------------

    def add_file_paths(self):
        """
        Add user file paths to the _filepaths attribute.

        The full path to each user data file is in the format:

            PATH/TO/APP/FOLDER/.../OnTrack/Users/<USERNAME>/<FILENAME>.json

        The _userpath attribute is joined to each file name in dna.ALL_FILES
        and this full path is mapped to its corresponding file ID in the
        _filepaths attribute. File IDs and associated file names are:

            'edref': ExerciseDetails.json
            'fdref': FoodDetails.json
            'fnref': FoodNutrients.json
            'uprof': Profile.json
            'ureco': Records.json
            'usett': Settings.json
            'utemp': Templates.json
        """
        for fileid in dna.ALL_FILES:
            filepath = os.path.join(self._userpath, dna.ALL_FILES[fileid])
            self._filepaths[fileid] = filepath

    def create_user_directory(self):
        """
        Create the user directory.

        Creates a folder at _userpath attribute if the user is new.
        """
        try:
            os.mkdir(self._userpath)
        except OSError:
            self._created = False
            QtGui.QMessageBox.warning(
                self._parent, "Cannot Create User",
                "A folder cannot be created for this user. You may continue " +
                "using this application to modify existing users.")

    def copy_reference_files(self):
        """
        Creates reference files in the user directory.

        Copies reference files ExerciseDetails.json, FoodDetails.json,
        and FoodNutrients.json from the reference source directory to the
        user directory specified by the _userpath attribute. If the user
        directory was not created, i.e. the _created attribute is False, this
        method does not attempt to copy reference files.
        """
        try:
            if not self._created:
                return
            refdir_path = os.path.join(sys.path[0], dna.REF_DIR)
            for fileid in dna.REF_FILES:
                refpath = os.path.join(refdir_path, dna.REF_FILES[fileid])
                with open(refpath, "r") as open_file:
                    refdata = json.load(open_file)
                    self.overwrite_file(fileid, refdata)
        except IOError:
            self._created = False
            QtGui.QMessageBox.warning(
                self._parent, "Cannot Create User",
                "A reference file cannot be copied to the user's folder! " +
                "You may continue using this application to modify " +
                "existing users.")

    def create_user_files(self):
        """
        Create new user files in the user directory.

        Creates empty user files Profile.json, Records.json, Settings.json, and
        Templates.json in the user directory specified by the _userpath
        attribute. The User.default_userdata attribute sets the structure of
        default user files. If the user directory was not created or reference
        files were not copied to the user directory, i.e. the _created
        attribute is False, this method does not attempt to create user files.
        """
        try:
            if not self._created:
                return
            for fileid in dna.USER_FILES:
                empty_data = User.default_userdata[fileid]
                filepath = self._filepaths[fileid]
                with open(filepath, "w") as open_file:
                    ujson.dump(empty_data, open_file)
        except (IOError, KeyError):
            self._created = False
            QtGui.QMessageBox.warning(
                self._parent, "Cannot Create User",
                "A data file cannot be created in this user's folder! You " +
                "may continue using this application to modify existing " +
                "users.")

    def get_data(self, file_id):
        """Return user data for the file ID."""
        try:
            return self._data[file_id]
        except KeyError:
            # Do not automatically log in any user the next time the app opens.
            self._parent.appstate.set_default_user(None)
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "Data has been corrupted for this user. You must delete " +
                "this user the next time you open OnTrack. OnTrack is " +
                "exiting...")
            sys.exit(1)

    def load_file_data(self):
        """
        Load user file data and add them to the _data attribute.

        The full path to each user data file is in the format:

            PATH/TO/APP/FOLDER/.../OnTrack/Users/<USERNAME>/<FILENAME>.json

        The data in each JSON file is read and loaded into a dict object which
        is mapped to the corresponding file ID in the _data attribute. File IDs
        and associated file names are:

            'edref': ExerciseDetails.json
            'fdref': FoodDetails.json
            'fnref': FoodNutrients.json
            'uprof': Profile.json
            'ureco': Records.json
            'usett': Settings.json
            'utemp': Templates.json

        If a new user was not successfully created, this method does not
        attempt to add file data to the _data attribute.
        """
        if not self._created:
            return
        for fileid in self._filepaths:
            self._data[fileid] = self.load_data(fileid)

    def load_data(self, file_id):
        """
        Load the file data into the _data attribute for a file ID.

        The file specified by the file_id arg is opened and the data is read
        into a dict object and returned. All reference and user files are in
        the JSON format. If an exception is raised, one of the user's files has
        likely been corrupted. The GUI's appstate's set_default_user method is
        called to remove reset the default user. This prevents a corrupted
        default username from causing the app to get stuck on this warning
        each time it is opened.

        :param file_id: A reference or user file ID
        :type file_id: str
        :return: File data for the specified file ID
        :rtype: dict
        """
        try:
            filepath = self._filepaths[file_id]
            with open(filepath, "r") as open_file:
                return json.load(open_file)
        except (IOError, KeyError):
            # Do not automatically log in any user the next time the app opens.
            self._parent.appstate.set_default_user(None)
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "A data file has been corrupted for this user. You must " +
                "delete this user the next time you open OnTrack. OnTrack " +
                "is exiting...")
            sys.exit(1)

    def overwrite_file(self, file_id, new_data):
        """
        Overwrite the specified file with new data.

        The file specified by the file_id arg is overwritten with the dict
        object passed as the new_data arg. If the file does not exist, it is
        created. If an exception is raised, one of the user's files has likely
        been corrupted. The GUI's appstate's set_default_user method is called
        to remove reset the default user. This prevents a corrupted default
        username from causing the app to get stuck on this warning each time it
        is opened.

        :param file_id: A reference or user file ID
        :type file_id: str
        :param new_data: New data with which to overwrite the specified file
        :type new_data: dict
        """
        try:
            filepath = self._filepaths[file_id]
            with open(filepath, "w") as open_file:
                ujson.dump(new_data, open_file)
        except (IOError, KeyError):
            # Do not automatically log in any user the next time the app opens.
            self._parent.appstate.set_default_user(None)
            QtGui.QMessageBox.warning(
                self._parent, "Critical Error",
                "A data file has been corrupted for this user. You must " +
                "delete this user the next time you open OnTrack. OnTrack " +
                "is exiting...")
            sys.exit(1)

    def delete_user_directory(self):
        """
        Delete the user directory.

        Deletes the folder at the _userpath attribute and all files within it.
        """
        try:
            shutil.rmtree(self._userpath, ignore_errors=True)
        except (IOError, OSError):
            userpath = os.path.join(sys.path[0], "Users")
            QtGui.QMessageBox.warning(
                self._parent, "Deletion Error",
                "The data for this user cannot be deleted. You must " +
                "manually delete the user folder found here:\n\n" + userpath +
                "\n\nUntil it is deleted, this user folder may cause " +
                "unforeseen issues with this application.")

    # ----------------------- SETTINGS METHODS ----------------------

    def settings(self):
        """
        Return the user's settings.

        :return: The user's settings
        :rtype: dict
        """
        return self._data["usett"]

    def update_settings(self, new_settings):
        """
        Update the user's settings.

        Overwrites the user's settings with new settings with the format:

            {setting name: setting value, ...}

        The different settings and their names are:

            'askdelete': bool to ask the user to confirm item deletion
            'askexit': bool to ask the user to confirm application exit
            'buildonly': bool to update Build Info for the entire build
            'favorites': dict of favorite IDs mapped to favorite lists
            'muscles': list of focus muscles to display
            'nutrients': list of nutrients to display
            'sortid': bool to sort inventories by item ID
            'sortup': bool to sort inventories in ascending order

        The Settings.json file is overwritten with the new data.

        :param new_settings: A dictionary of settings keys, either a partial
            or complete set of all settings keys, mapped to new settings values
        :type new_settings: dict
        """
        self._data["usett"].update(new_settings)
        self.overwrite_file("usett", self._data["usett"])

    def update_favorites(
            self, fave_id, item_id, is_favorite, delete_template=False):
        """
        Update the user's 'favorites' setting for an item ID.

        Searches the list mapped to the fave_id arg key in the 'favorites'
        sub-dict for the item_id arg. Based on the is_favorite arg and whether
        or not the item_id is found, the list is either updated to add or
        remove the item_id, or it remains unchanged. The favorites IDs and
        their corresponding inventory items are:

            'F': Food references
            'E': Exercise references
            'TR': Recipe templates
            'TM': Meal templates
            'TD': Diet templates
            'TW': Workout templates
            'TC': Cycle templates
            'TP': Program templates
            'RD': Diet records
            'RP': Program records

        If the delete_template arg is True, a template item has been deleted
        and the template item IDs have been reassigned to consecutive numbers
        starting with 10001. Since templates now have new item IDs, the IDs in
        the favorites list are inaccurate and need to be decremented by 1 if
        they are greater than the item_id arg.

        :param fave_id: An inventory's favorites ID
        :type fave_id: str
        :param item_id: A reference, template, or record item ID
        :type item_id: str
        :param is_favorite: True if the item is a favorite, otherwise False
        :type is_favorite: bool
        :param delete_template: True if a template is being deleted, else False
        :type delete_template: bool
        """
        faves = self._data["usett"]["favorites"][fave_id]
        if is_favorite:
            if item_id not in faves:
                faves.append(item_id)
        else:
            if item_id in faves:
                faves.remove(item_id)
        if delete_template:
            old_tids = []
            new_tids = []
            for tid in faves:
                if int(tid) > int(item_id):
                    old_tids.append(tid)
                    new_tids.append(str(int(tid) - 1))
            for tid in old_tids:
                faves.remove(tid)
            faves += new_tids
        self.overwrite_file("usett", self._data["usett"])

    # ----------------------- PROFILE METHODS -----------------------

    def health_diary(self):
        """
        Return the Health Diary.

        :return: The user's Health Diary
        :rtype: dict
        """
        return self._data["uprof"]["diary"]

    def add_entry(self, entry):
        """
        Add an entry to the Health Diary.

        Updates the user's Health Diary with a new entry with the format:

            {entry date: {health metric: measurement value, ...}}

        The Profile.json file is overwritten with the new data.

        :param entry: A dictionary with an entry date mapped to a dictionary of
            health metric measurements (metrics mapped to their values)
        :type entry: dict
        """
        self.health_diary().update(entry)
        self.overwrite_file("uprof", self._data["uprof"])

    def remove_entry(self, entry_date):
        """
        Remove an entry from the Health Diary.

        Removes the entry date and its measurements from the user's Health
        Diary. The Profile.json file is overwritten with the new data.

        :param entry_date: An existing Health Diary entry date
        :type entry_date: str
        """
        self._data["uprof"]["diary"].pop(entry_date)
        self.overwrite_file("uprof", self._data["uprof"])

    def remove_health_metric(self, health_metric):
        """
        Remove a health metric from the Health Diary.

        Removes the health_metric arg from each Health Diary entry in which a
        measurement for it exists. Any entry dates with no measurements
        remaining after removal of this metric are themselves removed from the
        Health Diary. The Profile.json file is overwritten with the new data.

        :param health_metric: An existing health metric in the Health Diary
        :type health_metric: str
        """
        empty_dates = []
        for entry_date in self._data["uprof"]["diary"]:
            if health_metric in self._data["uprof"]["diary"][entry_date]:
                self._data["uprof"]["diary"][entry_date].pop(health_metric)
            if not self._data["uprof"]["diary"][entry_date]:
                empty_dates.append(entry_date)
        for entry_date in empty_dates:
            self._data["uprof"]["diary"].pop(entry_date)
        self.overwrite_file("uprof", self._data["uprof"])

    def nutrient_guide(self):
        """
        Return the Nutrient Guide.

        :return: The user's Nutrient Guide
        :rtype: dict
        """
        return self._data["uprof"]["guide"]

    def add_targets(self, targets):
        """
        Add targets to the Nutrient Guide.

        Updates the user's Nutrient Guide with new targets with the format:

            {effective date: {nutrient ID: target value, ...}}

        The Profile.json file is overwritten with the new data.

        :param targets: A dictionary with an effective date mapped to a
            dictionary of nutrient IDs mapped to target values
        :type targets: dict
        """
        self._data["uprof"]["guide"].update(targets)
        self.overwrite_file("uprof", self._data["uprof"])

    def remove_targets(self, effective_date):
        """
        Remove nutrient targets from the Nutrient Guide.

        Removes the effective date and its target nutrient values from the
        Nutrient Guide. The Profile.json file is overwritten with the new data.

        :param effective_date: An existing Nutrient Guide effective date
        :type effective_date: str
        """
        self._data["uprof"]["guide"].pop(effective_date)
        self.overwrite_file("uprof", self._data["uprof"])

    # ---------------------- REFERENCE METHODS ----------------------

    def food_details(self, item_id=None):
        """
        Return the Food Details dictionary or a specific Food item's details.

        If the optional item_id parameter is assigned a Food reference item ID,
        the details list for that Food is returned, otherwise the entire Food
        Details reference dictionary is returned. A Food item's details are
        returned in a list with the format:

            [description, food group ID, [unit sequences]]

        :param item_id: A Food item ID or None
        :type item_id: str, None
        :return: A Food reference item's details list or the entire Food
            Details reference dictionary
        :rtype: dict, list
        """
        if item_id is None:
            return self._data["fdref"]
        else:
            return self._data["fdref"][item_id]

    def food_nutrients(self, item_id=None):
        """
        Return the Food Nutrients dict or a specific Food item's nutrients.

        If the optional item_id parameter is assigned a Food reference item ID,
        the nutrient content dictionary for that Food is returned, otherwise
        the entire Food Nutrients reference dictionary is returned. A Food
        item's nutrient content is returned in a dict with the format:

            {nutrient ID: value for 100 grams of Food, ... <per nutrient>}

        :param item_id: A Food item ID or None
        :type item_id: str, None
        :return: A Food reference item's nutrient content dict or the entire
            Food Nutrients reference dictionary
        :rtype: dict, list
        """
        if item_id is None:
            return self._data["fnref"]
        else:
            return self._data["fnref"][item_id]

    def exercise_details(self, item_id=None):
        """
        Return the Exercise Details dict or a specific Exercise item's details.

        If the optional item_id parameter is assigned an Exercise reference
        item ID, the details list for that Exercise is returned, otherwise the
        entire Exercise Details reference dictionary is returned. An Exercise
        item's details are returned in a list with the format:

            [description, focus muscle, [effort unit, intensity unit], [tags]]

        :param item_id: An Exercise item ID or None
        :type item_id: str, None
        :return: An Exercise reference item's details list or the entire
            Exercise Details reference dictionary
        """
        if item_id is None:
            return self._data["edref"]
        else:
            return self._data["edref"][item_id]

    def add_reference(self, ref_object):
        """
        Add a reference item to the Food or Exercise reference inventory.

        Updates the user's Food Details and Food Nutrients reference dicts if
        ref_object is a Reference object for a Food item, otherwise the object
        is for an Exercise item and the user's Exercise Details reference dict
        is updated. The ref_object arg stores all relevant properties of a
        new or existing reference item, accessed by passing the property name
        to the ref_object's info method. The property names and values relevant
        to this method are:

        --Food Reference Item--
            'reftype': 'Food'
            'itemid': reference item ID string
            'isfavorite': bool indicating if item is a favorite
            'nutrientcontent': nutrient content dictionary
        --Exercise Reference Item--
            'reftype': 'Exercise'
            'itemid': reference item ID string
            'isfavorite': bool indicating if item is a favorite

        The ref_object's details method is used to return the reference item's
        details list. If a new reference item is represented, its 'itemid' will
        be an empty string. In this case, the next available item ID for which
        to save reference item data in its applicable inventory will be
        determined. Valid Food item IDs range from '200001' to '299999', and
        valid Exercise item IDs range from '10001' to '19999'. When the maximum
        number of reference items is reached, this method returns False so that
        the GUI can identify and handle this event. Reference dictionaries are
        updated with ref_object data in the formats:

        --Food Details--
            {itemid: ['description', 'groupid', 'unitsequences']}
        --Food Nutrients--
            {itemid: 'nutrientcontent'}
        --Exercise Details--
            {itemid: ['description', 'focusmuscle', 'units', 'tags']}

        The applicable user files are overwritten with the new data, and the
        relevant user favorites list is updated. Returns the item ID if the
        reference was added, or False if the maximum number of references has
        been reached.

        :param ref_object: A Reference object containing properties of a new or
            existing Food or Exercise reference item
        :type ref_object: Reference
        """
        reftype = ref_object.info("reftype")
        itemid = ref_object.info("itemid")
        if reftype == "Food":
            if itemid == "":
                max_id = organs.max_key(
                    self.food_details(), floor="200000", ceiling="210000")
                rid = "200001" if max_id is None else str(int(max_id) + 1)
                if rid == "210001":
                    return False
            else:
                rid = itemid
            self._data["fdref"].update({rid: ref_object.details()})
            self._data["fnref"].update(
                {rid: ref_object.info("nutrientcontent")})
            self.overwrite_file("fdref", self._data["fdref"])
            self.overwrite_file("fnref", self._data["fnref"])
        else:
            if itemid == "":
                max_id = organs.max_key(
                    self.exercise_details(), floor="10000", ceiling="20000")
                rid = "10001" if max_id is None else str(int(max_id) + 1)
                if rid == "20001":
                    return False
            else:
                rid = itemid
            self._data["edref"].update({rid: ref_object.details()})
            self.overwrite_file("edref", self._data["edref"])
        self.update_favorites(reftype[0], rid, ref_object.info("isfavorite"))
        return rid

    def remove_reference(self, ref_object):
        """
        Remove a reference item from the Food or Exercise reference inventory.

        Updates the user's Food Details and Food Nutrients reference dicts if
        ref_object is a Reference object for a Food item, otherwise the object
        is for an Exercise item and the user's Exercise Details reference dict
        is updated. The ref_object arg stores all relevant properties of an
        existing reference item, accessed by passing the property name to the
        ref_object's info method. The property names and values relevant to
        this method are:

        --Food Reference Item--
            'reftype': 'Food'
            'itemid': reference item ID string
        --Exercise Reference Item--
            'reftype': 'Exercise'
            'itemid': reference item ID string

        Pops the 'itemid' property value from the relevant reference dict(s).
        The applicable user files are overwritten with the new data, and the
        favorites list is updated if necessary.

        :param ref_object: A Reference object containing properties of an
            existing Food or Exercise reference item
        :type ref_object: Reference
        """
        reftype = ref_object.info("reftype")
        itemid = ref_object.info("itemid")
        if reftype == "Food":
            self._data["fdref"].pop(itemid)
            self._data["fnref"].pop(itemid)
            self.overwrite_file("fdref", self._data["fdref"])
            self.overwrite_file("fnref", self._data["fnref"])
        else:
            self._data["edref"].pop(itemid)
            self.overwrite_file("edref", self._data["edref"])
        self.update_favorites(reftype[0], itemid, False)

    # ----------------------- TEMPLATE METHODS ----------------------

    def templates(self, cid):
        """
        Return the template inventory for a build element class ID.

        :param cid: The build element class ID of a template inventory
        :type cid: str
        """
        return self._data["utemp"][cid]

    def template_state(self, cid, item_id):
        """
        Return the state of a template inventory item.

        Searches the template inventory specified by the cid arg and returns
        the state of the template item specified by the item_id arg.

        :param cid: The build element class ID of a template inventory
        :type cid: str
        :param item_id: An existing template inventory item ID
        :type item_id: str
        :return: The state of the template inventory item
        :rtype: list
        """
        return self._data["utemp"][cid][item_id]

    def add_template(self, template_state, is_favorite=False, item_id=None):
        """
        Add a template item to the corresponding inventory.

        Updates the user's applicable template dictionary with a template state
        dict, with the item_id arg mapped to the template_state arg. If the
        template_state arg represents a new template, then an item_id arg is
        not passed to this method. In this case, the next available template
        item ID for which to save template state data is determined. Valid
        template item IDs range from '10001' to '99999'. When the maximum
        number of template items is reached, this method returns False so that
        the GUI can identify and handle this event. After the template dict is
        updated, the Templates.json file is overwritten with the new data, the
        _templateobjects attribute is updated with an object whose state is set
        to that of the template_state and mapped to the item ID, and the
        favorites list is updated according to the is_favorite arg. Returns
        the item ID if the template was added, or False if the maximum number
        of templates has been reached.

        :param template_state: The state of a new or existing template item
        :type template_state: list
        :param is_favorite: True if the template is a favorite, otherwise False
        :type is_favorite: bool
        :param item_id: An existing template inventory item ID
        :type item_id: str
        :return: The template's item ID string or False if the maximum number
            of template IDs has been reached
        :rtype: str, False
        """
        cid = template_state[0]
        if item_id is None:
            max_id = organs.max_key(
                self._data["utemp"][cid], floor="101", ceiling="600")
            tid = "101" if max_id is None else str(int(max_id) + 1)
            if tid == "601":
                return False
        else:
            tid = item_id
        self._data["utemp"][cid].update({tid: template_state})
        self.overwrite_file("utemp", self._data["utemp"])
        tem_object = body.build_element(cid)
        tem_object.set_state(template_state)
        self._templateobjects[cid].update({tid: tem_object})
        self.update_favorites("T" + cid, tid, is_favorite)
        return tid

    def remove_template(self, cid, item_id):
        """
        Remove a template item from the corresponding inventory.

        Removes the template state mapped to the item_id arg key from the
        template inventory dict specified by the cid arg. The remaining item
        IDs in the template inventory are reassigned to remove the gap in
        otherwise consecutive item IDs. The Templates.json file is overwritten
        with the new data, the relevant template object is removed from the
        _templateobjects attribute, and the favorites list is updated.

        :param cid: The build element class ID of a template inventory
        :type cid: str
        :param item_id: An existing template inventory item ID
        :type item_id: str
        """
        self._data["utemp"][cid].pop(item_id)
        self._data["utemp"][cid] = organs.consecutive_dict(
            self._data["utemp"][cid], "101", "600")
        self.overwrite_file("utemp", self._data["utemp"])
        self._templateobjects[cid].pop(item_id)
        self._templateobjects[cid] = organs.consecutive_dict(
            self._templateobjects[cid], "101", "600")
        self.update_favorites("T" + cid, item_id, False, True)

    def create_template_objects(self):
        """
        Create template objects for all template inventory items.

        Creates Recipe, Meal, Diet, Workout, Cycle, and Program objects for all
        existing templates and maps each object to the corresponding item ID.
        These template objects allow the application to call build element
        class methods to analyze template data and return specialized data sets
        as required.
        """
        self._templateobjects = {
            "R": {}, "M": {}, "D": {}, "W": {}, "C": {}, "P": {}}
        for cid in self._templateobjects:
            for item_id in self._data["utemp"][cid]:
                tem_object = body.build_element(cid)
                tem_object.set_state(self._data["utemp"][cid][item_id])
                self._templateobjects[cid][item_id] = tem_object

    def template_objects(self, cid, item_id=None):
        """
        Return template objects for the specified class ID.

        Returns the dictionary of template objects for the cid arg. If the
        item_id arg is passed a template item ID, that object is returned.

        :param cid: The build element class ID of template objects to return
        :type cid: str
        :param item_id: An existing template inventory item ID
        :type item_id: str, None
        :return: A dictionary of template objects mapped to their item IDs, or
            the specified template object
        :rtype: dict, Recipe, Meal, Diet, Workout, Cycle, Program
        """
        if item_id is None:
            return self._templateobjects[cid]
        else:
            return self._templateobjects[cid][item_id]

    # ------------------------ RECORD METHODS -----------------------

    def records(self, cid):
        """
        Return the record inventory for a build element class ID.

        :param cid: The build element class ID of a record inventory
        :type cid: str
        """
        return self._data["ureco"][cid]

    def record_exists(self, record_state):
        """
        Return True if a record item ID exists, otherwise return False.

        Determines whether the record_state arg is a Diet or Program object and
        checks if its item ID--the Diet date or Program start date--exists in
        the corresponding record inventory dict.

        :param record_state: The state of a new or existing record item
        :type record_state: list
        :return: True if the record date exists, otherwise False
        :rtype: bool
        """
        cid = record_state[0]
        item_id = record_state[3]
        if item_id in self._data["ureco"][cid]:
            return True
        return False

    def record_state(self, cid, item_id):
        """
        Return the state of a record inventory item.

        Searches the record inventory specified by the cid arg and returns the
        state of the record item specified by the item_id arg.

        :param cid: The build element class ID of a record inventory
        :type cid: str
        :param item_id: An existing record inventory item ID
        :type item_id: str
        :return: The state of the record inventory item
        :rtype: list
        """
        return self._data["ureco"][cid][item_id]

    def add_record(self, record_state, is_favorite=False, old_state=None):
        """
        Add a record item to the corresponding record inventory.

        Updates the user's applicable record inventory dictionary with a record
        state dict, with the record_state arg's Diet date or Program start date
        as the item ID mapped to the record_state arg. If record_state is the
        state of an existing, potentially edited record, the record's previous
        state is passed as the old_state arg. In this case, the date (item ID)
        of record_state is compared to that of old_state. If the two dates are
        different, after record_state has been added to the record inventory,
        the old_state record date is then removed from it. This prevents the
        same record from being saved twice, but under two different dates. This
        condition is unique to record items, since no other inventory item type
        allows the user to change its item ID.

        After the record inventory dict is updated, the Records.json file is
        overwritten with the new data, the _recordobjects attribute is updated
        with an object whose state is set to that of record_state and mapped to
        record_state's date/item ID, and the favorites list is updated. If
        record_state's date has been changed, remove_record is called to handle
        the removal of the previous state from the record inventory dict. If a
        new record overwrites an existing record, the update_favorites method
        automatically removes the record date from the favorites list.

        :param record_state: The state of a new or existing record item
        :type record_state: list
        :param is_favorite: True if the record is a favorite, otherwise False
        :type is_favorite: bool
        :param old_state: The previous state of the existing record item
            assigned to the record_state parameter, or None
        :type old_state: list, None
        """
        cid = record_state[0]
        item_id = record_state[3]
        self._data["ureco"][cid].update({item_id: record_state})
        self.overwrite_file("ureco", self._data["ureco"])
        rec_object = body.build_element(cid)
        rec_object.set_state(record_state)
        self._recordobjects[cid].update({item_id: rec_object})
        self.update_favorites("R" + cid, item_id, is_favorite)
        if old_state is not None and item_id != old_state[3]:
            self.remove_record(old_state)

    def remove_record(self, record_state):
        """
        Remove a record item from the corresponding inventory.

        Removes the record state mapped to the record_state arg's date/item ID
        key from the applicable record inventory. The Records.json file is
        overwritten with the new data, the relevant record object is removed
        from the _recordobjects attribute, and the favorites list is updated.

        :param record_state: The state of an existing record item
        :type record_state: list
        """
        cid = record_state[0]
        item_id = record_state[3]
        self._data["ureco"][cid].pop(item_id)
        self.overwrite_file("ureco", self._data["ureco"])
        self._recordobjects[cid].pop(item_id)
        self.update_favorites("R" + cid, item_id, False)

    def create_record_objects(self):
        """
        Create record objects for all record inventory items.

        Creates Diet and Program objects for all Diet and Program records and
        maps each object to the corresponding item ID--which is the Diet date
        or Program start date of that record. These record objects allow the
        application to call build element class methods to analyze record data
        and return specialized data sets as required.
        """
        self._recordobjects = {"D": {}, "P": {}}
        for cid in self._recordobjects:
            for item_id in self._data["ureco"][cid]:
                rec_object = body.build_element(cid)
                rec_object.set_state(self._data["ureco"][cid][item_id])
                self._recordobjects[cid][item_id] = rec_object

    def record_objects(self, cid, item_id=None):
        """
        Return record objects for the specified class ID.

        Returns the dictionary of record objects for the cid arg. If the
        item_id arg is passed a record item ID, that object is returned.

        :param cid: The build element class ID of record objects to return
        :type cid: str
        :param item_id: An existing record inventory item ID
        :type item_id: str, None
        :return: A dictionary of record objects mapped to their item IDs
        :rtype: dict, Diet, Program
        """
        if item_id is None:
            return self._recordobjects[cid]
        else:
            return self._recordobjects[cid][item_id]


# -----------------------------------------------------------------------------
# Source Data Creator ---------------------------------------------------------

class ReferenceFileCreator(QtCore.QThread):
    """
    QThread subclass to create Food and Exercise reference item source data.

    ReferenceFileCreator is used to create the initial ExerciseDetails.json,
    FoodDetails.json, and FoodNutrients.json reference files. The Exercise
    reference data is sourced from the dna.EXERCISES tuple of Exercise
    reference item details. The Food reference data is sourced from the website
    for the USDA National Nutrient Database for Standard Reference. This class
    scrapes Food reference item data from USDA source files and reshapes it to
    fit the purposes of this application. Class attributes are implemented to
    return signals indicating which reference file is being created, what the
    current progress is, and if an error is encountered. The run method
    inherited from the QThread superclass is overridden to execute file
    creation until all 3 reference files are saved.

    This class was used to create the aforementioned reference files for this
    application. It is not used by the application at any point during runtime.
    Future versions of OnTrack will use this class to allow the user to
    recreate missing, modified, or outdated reference source files.
    """

    # Implement three signals as class attributes to emit the focus reference
    # file (that which is being created currently), the progress status, and
    # errors (if an exception is raised at any time).
    focus_update = QtCore.pyqtSignal(str)
    progress_update = QtCore.pyqtSignal(float)
    error_update = QtCore.pyqtSignal()

    def __init__(self, parent):
        """
        Initialize a ReferenceFileCreator object.

        Assigns False to the completed attribute.

        :param parent: Parent QWidget
        :type parent: QWidget
        """
        QtCore.QThread.__init__(self, parent)
        self.completed = False

    def run(self):
        """Run the thread to create the reference source files."""
        try:
            # Run the thread until all 3 reference source files are created.
            while not self.completed:

                # Find the total length of the characters in the USDA source
                # data files FOOD_DES.txt, WEIGHT.txt, and NUT_DATA.txt.
                total_chars = 0.0
                with contextlib.closing(
                        urllib2.urlopen(dna.URL_FOOD_DES)) as temp:
                    total_chars += int(temp.info().getheader("Content-Length"))
                with contextlib.closing(
                        urllib2.urlopen(dna.URL_WEIGHT)) as temp:
                    total_chars += int(temp.info().getheader("Content-Length"))
                with contextlib.closing(
                        urllib2.urlopen(dna.URL_NUT_DATA)) as temp:
                    total_chars += int(temp.info().getheader("Content-Length"))
                # Increment characters by an arbitrary amount for the EDREF
                # source data in the dna module. Initialize a variable to track
                # the number of characters that are read so that the progress
                # can be emitted. Create the output reference directory.
                total_chars += len(dna.EXERCISES) * 10
                chars_read = 0
                os.mkdir(dna.REF_DIR)

                # -------- Process Exercise Details (EDREF) ---------

                # Emit signal with EDREF focus, sleep for 1 second to allow
                # focus message to be displayed (EDREF is processed quickly).
                self.focus_update.emit("Creating Exercise Details Reference")
                self.sleep(1)
                # Initialize the EDREF dict and its path.
                edref = {}
                edref_path = os.path.join(
                    sys.path[0], dna.REF_DIR, dna.REF_FILES["edref"])
                # Exercise IDs range from 10001 to 19999.
                first_id = "10001"
                for exercise_details in dna.EXERCISES:
                    edref[first_id] = exercise_details
                    first_id = str(int(first_id) + 1)
                    # Increment chars read and emit signal with progress value.
                    chars_read += 10
                    self.progress_update.emit((chars_read / total_chars) * 100)
                # Write edref to edref file path.
                with open(edref_path, "w") as edref_file:
                    ujson.dump(edref, edref_file)

                # ----------- Process Food Details (FDREF) ----------

                # Emit signal with FDREF focus.
                self.focus_update.emit("Creating Food Details Reference")
                # Initialize the FDREF dict and its path.
                fdref = {}
                fdref_path = os.path.join(
                    dna.REF_DIR, dna.REF_FILES["fdref"])
                # Open USDA food description URL and read data into fdref.
                with contextlib.closing(
                        urllib2.urlopen(dna.URL_FOOD_DES)) as food_des:
                    for line in food_des:
                        # Prepend '1' to the USDA food ID to make it easier to
                        # add Food reference items beyond 99999.
                        foodid = "1" + line[1:6]
                        # Add food ID key to fdref if it does not exist and map
                        # it to an empty list.
                        if foodid not in fdref:
                            fdref[foodid] = []
                        # Append food description to food ID list in fdref.
                        food_des = line[16:442].replace("~", "").split("^")[0]
                        fdref[foodid].append(food_des)
                        # Append food group ID to food ID list in fdref.
                        groupid = line[9:13]
                        fdref[foodid].append(groupid)
                        # Increment chars read and emit signal with progress
                        # value.
                        chars_read += len(line)
                        self.progress_update.emit(
                            (chars_read / total_chars) * 100)
                # Append empty list to food ID list in fdref for storage of
                # unit sequences.
                for foodid in fdref:
                    fdref[foodid].append([])

                # Open USDA food weight URL and read data into fdref.
                with contextlib.closing(
                        urllib2.urlopen(dna.URL_WEIGHT)) as food_wgt:
                    for line in food_wgt:
                        # Don't forget to prepend '1' to the USDA food ID.
                        foodid = "1" + line[1:6]
                        # Parse unit sequence. Numbers are converted to floats
                        # if they have a decimal value, otherwise ints.
                        sequence = line[8:].replace("~", "").split("^")
                        if organs.is_decimal(sequence[1]):
                            amount = float(sequence[1])
                        else:
                            amount = int(float(sequence[1]))
                        unit = sequence[2]
                        if organs.is_decimal(sequence[3]):
                            weight = float(sequence[3])
                        else:
                            weight = int(float(sequence[3]))
                        # Replace this single unicode character with a string.
                        # Yes, this is the only one. Forgoing this step will
                        # break everything.
                        if unit == "Entr\xe9e":
                            unit = "Entree"
                        # Append unit sequence to food ID list index 2.
                        fdref[foodid][2].append([amount, unit, weight])
                        # Increment chars read and emit signal with progress
                        # value.
                        chars_read += len(line)
                        self.progress_update.emit(
                            (chars_read / total_chars) * 100)
                # Remove all foods with no unit sequences. These are useless.
                foodids_to_remove = []
                for foodid in fdref:
                    if not fdref[foodid][2]:
                        foodids_to_remove.append(foodid)
                for foodid in foodids_to_remove:
                    fdref.pop(foodid)
                # Write fdref to fdref file path.
                with open(fdref_path, "w") as fdref_file:
                    ujson.dump(fdref, fdref_file)

                # ---------- Process Food Nutrients (FNREF) ---------

                # Emit signal with FNREF focus.
                self.focus_update.emit("Creating Food Nutrients Reference")
                # Initialize the FNREF dict and its path.
                fnref = {}
                fnref_path = os.path.join(
                    dna.REF_DIR, dna.REF_FILES["fnref"])
                # Open USDA food nutrient data URL and read data into fnref.
                with contextlib.closing(
                        urllib2.urlopen(dna.URL_NUT_DATA)) as nut_data:
                    for line in nut_data:
                        # Prepend '1' to food ID once more.
                        foodid = "1" + line[1:6]
                        # Add food ID key to fnref if it does not exist and map
                        # it to an empty dict.
                        if foodid not in fnref:
                            fnref[foodid] = {}
                        # Parse nutrient ID and nutrient value. Skip over any
                        # nutrient IDs not used by this application.
                        nutrientid = line[9:12]
                        if nutrientid not in dna.NUTRIENTS:
                            continue
                        value = line[14:24].split("^")[0]
                        if organs.is_decimal(value):
                            value = float(value)
                        else:
                            value = int(float(value))
                        # Append nutrient ID and value if value > 0. If a food
                        # ID does not have a nutrient ID listed for it in FNREF
                        # then it is assumed the value of that nutrient is 0.
                        if value > 0:
                            fnref[foodid][nutrientid] = value
                        # Increment chars read and emit signal with progress
                        # value.
                        chars_read += len(line)
                        self.progress_update.emit(
                            (chars_read / total_chars) * 100)
                # Write fnref to fnref file path.
                with open(fnref_path, "w") as fnref_file:
                    ujson.dump(fnref, fnref_file)

                # ---------------------------------------------------

                # Emit signal with final focus and set completed attribute to
                # True to finish the thread.
                self.focus_update.emit("All References Completed")
                self.completed = True

        except (IndexError, TypeError, urllib2.URLError, ValueError):
            # Emit error signal.
            self.error_update.emit()
