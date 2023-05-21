
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

### (1) : The department filter  : use this to show teachers of only a certain department
### (2) : Day & Period selector : Select a day and period to show the status of faculty at
### (3) : Available Faculty : list of all the teachers free at the selected day and period
### (4) : Engaged Faculty : list of all the teachers Busy and with whom at the selected day and period
### (5) : Status bar : Click on any teacher to view number of free periods for that teacher here
 
 ### these are all the things that you see when you open up the window. When do some interaction, there are some more sub-windows that show up :
 

## 1. Right click menu :

![enter image description here](https://i.ibb.co/Xy1SN1k/image.png)

## 1.1. Check Time Table :

Check the teacher's time Table for the selected day or any other day of the week

![enter image description here](https://i.ibb.co/xhWcRwy/image.png)

## 1.2. Edit Data :

Opens up the excel file in any installed office software to edit

## 1.3 Select unavailable classes :

![enter image description here](https://i.ibb.co/vYV58bh/image.png)
Using this feature you can select a number of classes and give them the status of 'unavailable' - teachers teaching these classes will show up as free and when viewing the time table(1.1) these classes will be crossed out these classes will also count in the free period that are shown in the status bar(5)

## 1.4 Preferences :
![enter image description here](https://i.ibb.co/J2DW8Zy/image.png)

Here you can scaling of the program and choose from 150+themes available

# the ⓘ icons
these icon have information regarding the window they are on because most people are not gonna read this documentation lol

# the Excel file format
You can skip this part if the data has already been entered for you

The data for the program is read using a file in the directory of the program named 'Teacher_data.xlsx' 
If the file is not found program will ask for the file (img 1)
If a valid file is provided it will be copied to directory of the program with name 'Teacher_data.xlsx'

![excel file opened](https://i.ibb.co/dtwwDvN/image.png)

What you see here is a map of what gets read by the program the elements in green are read by the program
and elements with a white/not shown  background are ignored

one sheet of the excel file only contains the time table for one teacher 

### A1 : The department of the teacher
	The department can contain any numbers,charecters excluing ':'
	the value is read after the chracter ':'(i.e.. program ignores everything before it)
	extra spaces at the ends of the string is removed

### A2 :  Name Of Teacher
	The whole cell is read for the teacher name can contain any numbers,charecters
	extra spaces at the ends of the string is removed
	
### B4 - F11 : The time Table Of the teacher
	any spaces are removed
	any lowercase charecter is converted to uppercase
	empty cells are treated as free periods for the teacher
	
### Sheet names 
![sheet names](https://i.ibb.co/z7W2F6n/image.png)

	as there is a uniqe sheet for each teacher. in the final data file there will be alot of 
	sheets so,it is suggested to name the sheet as <teacher_name,teacher_deparment>. This is not
	read but helps in organising the sheets

### Example Data Files
[Template](https://filebin.net/i8kdp7j1ldd3w2gk/Teacher_data_template.xlsx)

[Example File](https://filebin.net/i8kdp7j1ldd3w2gk/Teacher_data.xlsx)


> Made with ❤ by Parth Sahni Using PySimpleGUI



	



 

 


