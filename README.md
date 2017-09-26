# OnTrack: Nutrition and Fitness Tracker

The repository contains the OnTrack nutrition and fitness tracking application.

## Table of Contents

- [Overview](#overview)
- [Development](#development)
  - [Application](#application)
  - [Installer](#installer)
  - [Replicating OnTrack](#replicating-ontrack)
- [Installation](#installation)
- [Using OnTrack](#using-ontrack)
  - [Getting Started](#getting-started)
  - [Managing Your Profile](#managing-your-profile)
  - [Recording Your Routines](#recording-your-routines)

## Overview

OnTrack is an open-source desktop application for tracking nutrition and fitness routines. It is tested for the Windows OS and is not yet available for macOS or Linux. The user interface has been optimized for 1920x1080 screen resolution. The OnTrack installer is available below under *Installation*. Screenshots and a brief tutorial are available below under *Using OnTrack*, and a thorough user guide is provided within the application.

## Development

OnTrack was written in Python 2.7.11. Its user interface was built with PyQt4 bindings for Qt 4.8.7 under a GPLv3 license. The OnTrack application folder (containing the application and all dependencies), as well as the OnTrack installer executable file, were created with PyInstaller 3.2.1. Application dependencies are: PyQt4 4.11.4, matplotlib 2.0.0, openpyxl 2.4.8, and ujson 1.35. Installer dependencies are: PyQt4 4.11.4 and winshell 0.6.

### Application

Application code consists of nine modules, the PyInstaller specification file, and the ReferenceSource_MASTER folder which contains the app's executable file icon and initial food and exercise reference data. PyInstaller was used to bundle these files and create a one-folder app.

File | Description
--- | ---
*\_\_init\_\_.py* | Blank init file
*album.py* | Resource data for app icons sourced from Google Material Icons under Apache License v2.0
*body.py* | Classes to manage and analyze nutrition and fitness data entered by the user
*brain.py* | Classes to manage local data files created and modify by the application
*dna.py* | Constants referenced by application modules
*ears.py* | Classes to prompt the user for data inputs
*eyes.py* | Functions to analyze and clean user data and classes to plot graphs of the cleaned data
*face.py* | Application user interface and the main function
*organs.py* | Custom PyQt4 class wrappers and helper functions used by application modules
*face.spec* | PyInstaller specification file for the application
*apple.ico* | Apple icon for OnT.exe, sourced from freeiconshop.com under a free use license
*ExerciseDetails.json* | Initial exercise reference data, original for this application, includes exercise details
*FoodDetails.json* | Initial food reference data, sourced from the USDA National Nutrient Database for Standard Reference (NDSR) Release 28, includes food details
*FoodNutrients.json* | Initial food reference data, sourced from the USDA NDSR, includes food nutrient content

### Installer

Installer code consists of three modules, the PyInstaller specification file, the installer's executable file icon, and the zipped OnTrack application folder created by PyInstaller which contains the application and all dependencies. The zipped OnTrack application folder is not included in this repository, but it can be downloaded at the applicable link below under *Installation*. PyInstaller was used to bundle these files and create a one-file app.

File | Description
--- | ---
*\_\_init\_\_.py* | Blank init file
*icons.py* | Resource data for installer taskbar icon apple.ico
*installer.py* | Installer user interface and the main function
*installer.spec* | PyInstaller specification file for the installer
*apple.ico* | Apple icon for OnTrack_Installer.exe, sourced from freeiconshop.con under a free use license
*OnTrack_zipped.zip* | Zipped OnTrack application folder created by PyInstaller -- **not included in this repository**

### Replicating OnTrack

The OnTrack application can be replicated by following the directions below.
1. Save all application files and move them to the same folder.
2. Create a folder in this directory called 'ReferenceSource_MASTER' and save the four applicable files to it.
3. Change the pathex and icon parameters in face.spec to the correct paths on your hard drive.
4. Install all dependencies (and their dependencies) into a virtual environment.
5. Open the command prompt, activate your virtual environment, and navigate to your application code directory.
6. Execute ```pyinstaller face.spec``` to create the application distribution folder.
7. Zip the OnTrack folder located in the dist folder. Alternately, save the zipped OnTrack application folder from the link found below under *Installation*
8. Save all installer files and move them to the same folder.
9. Move the zipped OnTrack application folder into that directory.
10. Change the pathex and icon parameters in installer.spec to the correct paths on your hard drive.
11. Change virtual environments if applicable and install all dependencies.
12. Navigate to your installer code directory.
13. Execute ```pyinstaller installer.spec``` to create the installer distribution folder.
14. Open the OnTrack_Installer.exe file in the dist folder.

## Installation

You can download the OnTrack installer by clicking the link below.
* [Click here to download the installer](https://dl.dropbox.com/s/x4cdfy4k7sxl0af/OnTrack_Installer.exe?dl=0 "Download OnTrack_Installer.exe")

The installer contains the zipped OnTrack application folder. To "install" OnTrack, it simply unzips this folder into your selected directory and creates a desktop shortcut to the app's executable file 'OnT.exe'. The installer size is 60 MB. The OnTrack app initially requres 100 MB of free space. Each OnTrack user typically generates between 5-10 MB of additional data. Your antivirus software might flag the installer since it is an unknown executable file without a digital signature.

If you prefer, you can download the zipped application folder by clicking the link below. Remember that the file 'OnT.exe' launches the application.
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