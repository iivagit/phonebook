This is a demo example with PyQt5, sqlite for development and shell for testing.

The application environment settings are:
OS: Ubuntu 18.04
base memory: 10240 MB
processor: 6 CPUs
and the following packages should be installed:
$ sudo apt-get install python3-pyqt5
$ sudo apt-get install pyqt5-dev-tools qtcreator
$ sudo apt-get install sqlite3
$ apt-get install python3-pyqt5.qtsql
$ sudo apt install xdotool

How to use the application:

1. Create database as
python3 create_db.py

2. Start the application as
python3 notebook.py

There are possibilities:
1) you can add a person
- click "add people" button, 
- fill the necessary fields in the opened window 
-click "Ok"

2) you can delete person
Select a cell at necessary row that should be deleted and press "del people"

3) you can find person in the table
- print person name in the text field "search name" 
- press Enter
the found person/persons will be selected in table with grey background color

4) table shows all persons

Also you can use the following hot keys:
'a'/'A' – add people
'q'/'Q' – close program


Testing:
Please, see run_test.sh
It is an automated test that adds a person 
you can run it as: 
$ python3 notebook.py & ./run_test.sh