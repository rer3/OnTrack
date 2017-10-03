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
  - [Managing References](#managing-references)
- [Contact Info](#contact-info)

## Overview

OnTrack is an open-source desktop application for tracking nutrition and fitness routines. It is tested for the Windows OS and is not yet available for macOS or Linux. The user interface has been optimized for 1920x1080 screen resolution. The OnTrack installer is available below under *Installation*. Screenshots and a brief tutorial are available below under **Using OnTrack**, and a thorough user guide is provided within the application.

## Development

OnTrack was written in Python 2.7.11. Its user interface uses PyQt4 bindings for Qt 4.8.7 under a GPLv3 license. The OnTrack application folder (containing the application and all dependencies), as well as the OnTrack installer executable file, were created with PyInstaller 3.2.1. Application dependencies are PyQt4 4.11.4, matplotlib 2.0.0, openpyxl 2.4.8, and ujson 1.35. Installer dependencies are PyQt4 4.11.4 and winshell 0.6.

### Application

Application code consists of nine modules, the PyInstaller specification file, and the ReferenceSource_MASTER folder which contains the app's executable file icon and initial food and exercise reference data. PyInstaller was used to bundle these OnTrack application files and create a one-folder app.

File | Description
--- | ---
*\_\_init\_\_.py* | Blank init file
*album.py* | Resource data for app icons sourced from Google Material Icons and used under an Apache License v2.0
*body.py* | Classes to manage and analyze nutrition and fitness data entered by the user
*brain.py* | Classes to manage local data files created and modified by the application
*dna.py* | Constants referenced by application modules
*ears.py* | Classes to prompt the user for data inputs
*eyes.py* | Functions to analyze and clean user data and classes to plot graphs of the cleaned data
*face.py* | Application user interface and the main function
*organs.py* | Custom PyQt4 class wrappers and helper functions used by application modules
*face.spec* | PyInstaller specification file for the application
*apple.ico* | OnT.exe icon sourced from freeiconshop.com and used under a free use license
*ExerciseDetails.json* | Initial exercise reference data, original for this application, includes exercise details
*FoodDetails.json* | Initial food reference data, sourced from the USDA National Nutrient Database for Standard Reference (NDSR) Release 28, includes food details
*FoodNutrients.json* | Initial food reference data, sourced from the USDA NDSR, includes food nutrient content

### Installer

Installer code consists of three modules, the PyInstaller specification file, the installer's executable file icon, and the zipped OnTrack application folder, created by PyInstaller, which contains the application and all dependencies. The zipped OnTrack application folder is not included in this repository, but it can be downloaded at the applicable link below under **Installation**. PyInstaller was used to bundle these OnTrack installer files and create a one-file app.

File | Description
--- | ---
*\_\_init\_\_.py* | Blank init file
*icons.py* | Resource data for installer icon *apple.ico*
*installer.py* | Installer user interface and the main function
*installer.spec* | PyInstaller specification file for the installer
*apple.ico* | OnTrack_Installer.exe icon sourced from freeiconshop.com and used under a free use license
*OnTrack_zipped.zip* | Zipped OnTrack application folder created by PyInstaller -- **not included in this repository**

### Replicating OnTrack

The OnTrack application can be replicated by following the directions below.
1. Save all application files to the same folder on your hard drive.
2. Create a folder in this directory called 'ReferenceSource_MASTER' and save the four applicable files to it.
3. Change the ```pathex``` and ```icon``` parameters in *face.spec* to the correct paths on your hard drive.
4. Install all dependencies into a virtual environment.
5. Open the command prompt, activate your virtual environment, and navigate to your application code directory.
6. Execute ```pyinstaller face.spec``` to create the application distribution folder.
7. Zip the OnTrack folder located in the dist folder. Alternately, save the zipped OnTrack application folder from the link found below under **Installation**. The folder must be called 'OnTrack_zipped', otherwise the ```datas``` parameter in *installer.spec* must be changed.
8. Save all installer files to the same folder on your hard drive and move the zipped OnTrack folder into that directory.
10. Change the ```pathex``` and ```icon``` parameters in *installer.spec* to the correct paths on your hard drive.
11. Change virtual environments if applicable and install all dependencies.
12. Navigate to your installer code directory.
13. Execute ```pyinstaller installer.spec``` to create the installer distribution folder.
14. Open the 'OnTrack_Installer.exe' file in the dist folder.

## Installation

You can download the OnTrack installer by clicking the link below.
* [Click here to download the installer](https://dl.dropbox.com/s/myqikw8q66iz5ar/OnTrack_Installer.exe?dl=0 "Download OnTrack_Installer.exe")

The installer contains the zipped OnTrack application folder. To "install" OnTrack, it simply unzips this folder into your selected directory and creates a desktop shortcut to the app's executable file 'OnT.exe'. The installer size is 60 MB. The OnTrack app initially requires 100 MB of free space. Each OnTrack user typically generates between 5-10 MB of additional data. Your antivirus software might flag the installer since it is an unknown executable file without a digital signature.

If you prefer, you can download the zipped application folder by clicking the link below. Unzip it into your directory of choice and open the file 'OnT.exe' to launch the application.
* [Click here to download the zipped app folder](https://dl.dropbox.com/s/ia10lmxix924qto/OnTrack_zipped.zip?dl=0 "Download OnTrack_zipped.zip")

## Using OnTrack

### Getting Started

OnTrack's user interface implements responsive menus which actively enable and disable buttons based on whether or not the button actions may be executed at that time. This feature facilitates a smoother UI experience. Move your mouse cursor over any menu button to show a description of its action in the status bar at the bottom of the window. All actions are permanent as this app does not utilize PyQt's Undo/Redo framework. As such, your local data files are irreversibly changed each time you execute any type of save action. Also, when you move your mouse cursor over icon-only buttons, a tooltip will pop up with the button's name.

Once OnTrack is installed on your computer, click the shortcut on your desktop to open the application. On the Home page, you will find the Main Menu at the top, a Login Menu at the center, and a *Settings* button. Enter your username under **New User** and click *Create User*. Then select your username from the drop-down list under **Active Users** and click *Login User*. All app users start out with the same food and exercise reference inventories. You must log in to navigate to the Profile and Builder pages.

[![Home][Home]][Home]

Click the *Guide* button in the Main Menu to access OnTrack's user guide and glossary. Give each resource a thorough read, or just dive right into tinkering with the tools on the Profile and Builder pages. Change application behavior by clicking *Settings* under the Login Menu.

[![Guide][Guide]][Guide]
[![Settings][Settings]][Settings]

### Managing Your Profile

Click the *Profile* button in the Main Menu to go to the Profile page. Profile tools are the Health Diary, Nutrient Guide, and Data Plotter. Use the **Health Diary** to record daily health metric measurements (e.g. weight). Use the **Nutrient Guide** to set daily nutrient targets. Use the **Data Plotter** to create graphs of your nutrition and fitness data. An example of a Health Metrics graph is shown below.

[![Profile][Profile]][Profile]
[![Plot][Plot]][Plot]

### Recording Your Routines

Click the *Builder* button in the Main Menu to go to the Builder page. Builder tools are the Build Manager and the Inventory Manager. Use the **Build Manager** to create and edit nutrition and fitness routines and save them as templates or records. Use the **Inventory Manager** to create references and view, edit, and delete references, templates, and records.

The Build Manager lets you create a data representation of your nutrition or fitness routine, called a *build*. Each build is made up of one or more *build elements*. These elements are just the different components of your routine. Build elements and their relative differences will become clear as you begin using OnTrack.

To start creating your routine, click the *Create New Build* button at the top of the Build Menu and select the type of build that you want to create. Nutrition build types are Diets, Meals, and Recipes. Fitness build types are Programs, Cycles, and Workouts. Your new build will show up in the Build Viewer. Now you can add, edit, or remove its build elements.

[![Create][Create]][Create]
[![Builder][Builder]][Builder]

You can also edit a build template or record by loading the applicable inventory, selecting the item matching one of the build types mentioned above, and clicking the *Send Item To Build* button at the top of the Inventory Menu. To load the inventory, just select it from the Inventory Manager's inventory drop-down list and it will automatically show up in the Inventory Viewer. You can view the properties of an inventory item at any time by double-clicking it, or by selecting it and clicking the *View Item* button in the Inventory Menu.

[![Inventory][Inventory]][Inventory]
[![View][View]][View]

You can add new elements to your build by selecting one of its build elements and clicking the *Add New Element* button in the Build Menu. A dialog will appear prompting you to edit this new element's properties. Click 'OK' to save changes and add the new element as a child to the selected build element. This parent-child relationship is shown in the Build Viewer by indentations. It is important to track because it stores information like which Meals (children) were eaten throughout a day's Diet (parent), or which Workouts (children) were completed during a week's Cycle (parent).

[![Meal][Meal]][Meal]
[![Workout][Workout]][Workout]

You can also add Food or Exercise reference items as elements to your build. They appear in your build as Ingredients and Activities, respectively. To add a reference item to your build, select an applicable build element (Meal, Recipe, or Workout) in the Build Viewer, select the reference item in the Inventory Viewer, then click the 'Add Inventory Item' button in the Build Menu. A dialog will appear prompting you to add Quantities to the new Ingredient or Sessions to the new Activity. Click 'OK' to save changes and add the element to your build.

[![Quantities][Quantities]][Quantities]
[![Sessions][Sessions]][Sessions]

Below is a handy table to remember each routine's elements, their properties, and elements that may be added to them as children.

Routine | Name | Properties | Child Element(s)
--- | --- | --- | ---
Nutrition | Diet | description, date | Meal
Nutrition | Meal | description, date | Recipe, Ingredient
Nutrition | Recipe | description, portion | Recipe, Ingredient
Nutrition | Ingredient | NA | Quantity
Nutrition | Quantity | amount, unit | NA
Fitness | Program | description, start | Cycle
Fitness | Cycle | description | Workout
Fitness | Workout | description, period | Activity
Fitness | Activity | NA | Session
Fitness | Session | effort, intensity, note | NA

## Managing References

Although OnTrack comes with pre-loaded Food and Exercise reference items, you can create new Foods and Exercises to fill in any gaps. Load the applicable inventory and click the *Create New Reference* button in the Inventory Menu. A dialog will appear prompting you to edit this new reference item's properties. Click 'OK' to save changes and add the new item to the inventory.

[![Food][Food]][Food]
[![Exercise][Exercise]][Exercise]

If you know other OnTrack users, you can share your custom reference items with each other. Select a Food or Exercise and click the *Save Data Capsule* button in the Inventory Menu. Your reference item will be saved to your hard drive as a "Data Capsule" file with a .json extension. This file stores all of the item's properties in a recognizable format. Now you or anyone else that uses OnTrack can create that same reference item without having to reenter all of those same properties. Simply load the applicable inventory, click the *Load Data Capsules* button in the Inventory Menu, and select one or more Data Capsules on your hard drive. OnTrack will attempt to create a reference item for each one.

## Contact Info

If you have any questions or comments, feel free to email me at roberterager3@gmail.com.

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