# Substitution-scheduler
Basically A GUI program that takes in a excel file and tells what teacher is free in a specific period of specific day but Does MUCH more than that


##

## Features :
1. Real time updates based on what options you selected.
2. Customizable theme and scaling.
3. All data saved in excel format 
4. Set unavailable classes.
5. status bar with number of free period display
6. check time table of a teacher
7. filter needed teachers by department
8. very user-friendly
##

## First start & intro :
When you start the program for the first time It will ask for a data file to read from :![enter image description here](https://i.ibb.co/1qynKs0/image.png)
Here you can select the excel file with the containing all the teacher data by either clicking the 'browse' button or entering a path. The excel file should be in in a proper format to be read by the software.
once the file is opened it  is copied into the program's directory named 'Teacher_data.xlsx' for convenience


After Selecting a valid data file a window like this will open up :

![enter image description here](https://i.ibb.co/2FsS78F/Screenshot-2023-05-21-005236.png)

This window consists of many things:

(1) : The department filter  : use this to show teachers of only a certain department
(2) : Day & Period selector : Select a day and period to show the status of faculty at
(3) : Available Faculty : list of all the teachers free at the selected day and period
(4) : Engaged Faculty : list of all the teachers Busy and with whom at the selected day and period
(5) : Status bar : Click on any teacher to view number of free periods for that teacher here
 
 these are all the things that you see when you open up the window
 when do some interaction,there are some more sub-windows that show up :
 

## 1. Right click menu :

![right click menu](https://i.ibb.co/Xy1SN1k/image.png)

## 1.1. Check Time Table :

 Check the teacher's time Table for the selected day or any other day of the week
 
![Time Table window](https://i.ibb.co/xhWcRwy/image.png)

## 1.2. Edit Data :

Opens up the excel file in any installed office software to edit

## 1.3 Select unavailable classes :

![unavailable classes window](https://i.ibb.co/vYV58bh/image.png)

Using this feature you can select a number of classes and give them the status of 'unavailable' - teachers teaching these classes will show up as free and when viewing the time table(1.1) these classes will be crossed out these classes will also count in the free period that are shown in the status bar(5)

## 1.4 Preferences :
![prefrences window](https://i.ibb.co/J2DW8Zy/image.png)

Here you can scaling of the program and choose from 150+themes available

# the ⓘ icons
these icon have information regarding the window they are on because most people are not gonna read this documentation lol

# and that's all for now! :)
Made with <3 by Parth Sahni Using PySimpleGUI
