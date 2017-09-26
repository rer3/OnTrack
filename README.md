# OnTrack: Nutrition and Fitness Tracker

The repository contains the OnTrack nutrition and fitness tracking application.

## Table of Contents

- [Overview](#overview)
- [Development](#development)
- [Installation](#installation)
- [Using OnTrack](#using-ontrack)
  - [Getting Started](#getting-started)
  - [Managing Your Profile](#managing-your-profile)
  - [Recording Your Routines](#recording-your-routines)

## Overview

OnTrack is an open-source desktop application for tracking nutrition and fitness routines. It was written in Python 2.7.11. Its user interface was built with the PyQt4 bindings for Qt v4 under a GPLv3 license. The OnTrack application folder (containing the application and all dependencies), as well as the OnTrack Installer executable file, were created with PyInstaller. OnTrack is tested for the Windows OS and is not yet available for macOS or Linux. The user interface has been optimized for 1920x1080 screen resolution.

## Development

#### Application

* ReferenceSource_MASTER
  - apple.ico
  - ExerciseDetails.json
  - FoodDetails.json
  - FoodNutrients.json
* __init__.py
* album.py
* body.py
* brain.py
* dna.py
* ears.py
* eyes.py
* face.py
* face.spec
* organs.py

#### Installer

* __init__.py
* apple.ico
* icons.py
* installer.py
* installer.spec
* OnTrack_zipped.zip (must be created by PyInstaller)

The .spec files used to create the application folder and Installer executable file are included in this repository. The pathex and icon parameters in each file must be changed to the path to all application files and the path to the apple icon, respectively. Open the command prompt and activate your virtual environment. Navigate to your application code directory and execute:
```
pyinstaller face.spec
```

Zip the OnTrack folder in the resulting dist folder and move it to the installer code directory. Activate the installer's virtual environment (if applicable), navigate to the installer code directory, and execute:
```
pyinstaller installer.spec
```

The OnTrack_Installer.exe file is in the resulting dist folder.

## Installation

You can download the OnTrack installer by clicking the link below.
* [Click here to download the installer](https://dl.dropbox.com/s/x4cdfy4k7sxl0af/OnTrack_Installer.exe?dl=0 "Download OnTrack_Installer.exe")

The installer contains the zipped OnTrack application folder. To "install" OnTrack, it simply unzips this folder into your selected directory and creates a desktop shortcut to the app's executable file 'OnT.exe'. The installer size is 60 MB. The OnTrack app initially requres 100 MB of free space. Each OnTrack user typically generates between 5-10 MB of additional data. Your antivirus software might flag the installer since it is an unknown executable file without a digital signature. If you prefer, you can download the zipped application folder by clicking the link below. Remember that the file 'OnT.exe' launches the application.

* [Click here to download the zipped app folder](https://dl.dropbox.com/s/i8rxwsm4dgcfxi9/OnTrack_zipped.zip?dl=0 "Download OnTrack_zipped.zip")

## Using OnTrack

### Getting Started

Once OnTrack is installed on your computer, click the shortcut on your desktop to open the application. On the Home page, you will find the Main Menu at the top, a Login Menu at the center, and a Settings button beneath the Login Menu. Create your username, select it from the drop-down list of active users, and log in.

[![Home][Home]][Home]

Click the 'Guide' button in the Main Menu to access OnTrack's user guide and glossary. You can give each resource a thorough read, or just dive right into tinkering with the tools on the Profile and Builder pages.

[![Guide][Guide]][Guide]

Change application behavior by clicking the Settings button.

[![Settings][Settings]][Settings]

### Managing Your Profile

Click the Profile button in the Main Menu to go to the Profile page. Profile tools are the Health Diary, Nutrient Guide, and Data Plotter. Use the Health Diary to record daily health metric measurements (e.g. weight). Use the Nutrient Guide to designate daily nutrient targets. Use the Data Plotter to create graphs of your nutrition and fitness data.

[![Profile][Profile]][Profile]
[![Plot][Plot]][Plot]

### Recording Your Routines

[Home]: https://i.imgur.com/dIcIZhi.png "Home Page"
[Settings]: https://i.imgur.com/jEaxGZw.png "Change App Settings"
[Profile]: https://i.imgur.com/z35D7cm.png "Manage Profile Data"
[Plot]: https://i.imgur.com/7Z1OKKk.png "View Data Plots"
[Inventory]: https://i.imgur.com/QoOtg7Q.png "Load Inventories"
[Create]: https://i.imgur.com/GgaWMAl.png "Create Your Build"
[Builder]: https://i.imgur.com/4mbyyQt.png "Modify Your Build"
[View]: https://i.imgur.com/4JP4xm9.png "View Inventory Items"
[Meal]: https://i.imgur.com/AYEANom.png "Add Meals to Your Build"
[Quantities]: https://i.imgur.com/jhZdptE.png "Add Ingredient Quantities to Your Build"
[Sessions]: https://i.imgur.com/Vbhgc9I.png "Add Activity Sessions to Your Build"
[Workout]: https://i.imgur.com/Mw2kJov.png "Add Workouts to Your Build"
[Food]: https://i.imgur.com/keMF7bK.png "Add Food Reference Items"
[Exercise]: https://i.imgur.com/JLFEVn9.png "Add Exercise Reference Items"
[Guide]: https://i.imgur.com/6kdyQRF.png "Read the User Guide"