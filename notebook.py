# sudo apt-get install python3-pyqt5
# sudo apt-get install pyqt5-dev-tools qtcreator
# sudo apt-get install sqlite3
# apt-get install python3-pyqt5.qtsql
# python3 notebook.py

import sys
from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets, QtSql, QtGui, QtCore

from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout



###

class People:
    def __init__(self, ids, firstname, lastname, phone, note):
        self.ids = ids
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.note = note

###

class DBConnection():
    def __init__(self, filename, server):
        db = QtSql.QSqlDatabase.addDatabase(server)
        db.setDatabaseName(filename)
        if not db.open():
            QMessageBox.critical(None, "Cannot open database",
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read the Qt SQL "
                    "driver documentation for information how to build it.\n\n"
                    "Click Cancel to exit.", QMessageBox.Cancel)

    def get_people(self):
        items = []
        query = QtSql.QSqlQuery()
        query.exec_("select * from people")
        while query.next():
            ids = query.value(0)
            firstname = query.value(1)
            lastname = query.value(2)
            phone = query.value(3)
            note = query.value(4)

            item = People(ids, firstname, lastname, phone, note)
            items.append(item)
            #print(ids, " ", firstname)
        return items

    def add_people(self, firstname, lastname, phone, note):
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO people (firstname, lastname, phone_number, note) "
                    "VALUES (?, ?, ?, ?)")
        query.addBindValue(firstname)
        query.addBindValue(lastname)
        query.addBindValue(phone)
        query.addBindValue(note)
        query.exec_()

    def del_people(self, id):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM people WHERE id=?")
        query.addBindValue(id)
        query.exec_()



dbc = DBConnection('db.sqlite', 'QSQLITE')


class MyTable(QWidget):
    def __init__(self, window, parent=None):
        super(MyTable, self).__init__(parent)
        self.window = window
        self.table = window.tablePeople

        self.table.setColumnCount(5)     # Устанавливаем три колонки
        self.table.setRowCount(1)        # и одну строку в таблице
 
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["ids", "name", "surname", "phone", "note"])
 
        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("ids")
        self.table.horizontalHeaderItem(1).setToolTip("name")
        self.table.horizontalHeaderItem(2).setToolTip("surname")
        self.table.horizontalHeaderItem(3).setToolTip("phone")
        self.table.horizontalHeaderItem(4).setToolTip("note")

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignRight)
        self.table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignRight)

        self.table.setColumnHidden(0,True)
        
    def table_create(self):
        index = 0
        items = dbc.get_people()
        #print (len(items))
        for item in items:
            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(item.ids)))
            self.table.setItem(index, 1, QTableWidgetItem(item.firstname))
            self.table.setItem(index, 2, QTableWidgetItem(item.lastname))
            self.table.setItem(index, 3, QTableWidgetItem(item.phone))
            self.table.setItem(index, 4, QTableWidgetItem(item.note))
            index += 1        


    def init(self, filename, server):
        import os
        if os.path.exists(filename):
            self.table_create()
        else:
            print ("filename is not exist!" )

    def mousePressEvent(self, event):
        print ("mousePressEvent" )
        if self.itemAt(event.pos()) is not None:
            self.clearSelection()
        QtGui.QTableWidget.mousePressEvent(self, event)

###

def handleAddPeopleButton():
    addwindow.show()


def handleDelPeopleButton(table):
    row = table.table.currentRow()
    if (row >=0):
        ids = table.table.item(row, 0).text().strip()
        dbc.del_people(ids)


def handleSearchName(table, text):
    columnIndex=1
    color_default = QtGui.QColor(255,255,255)
    color = QtGui.QColor(125,125,125)
    for row in range(table.table.rowCount()):
        if table.table.item(row, columnIndex).text().strip() == text.strip():
            table.table.item(row, columnIndex).setBackground(color)
        else:
            table.table.item(row, columnIndex).setBackground(color_default)            



def handleOkButton():
    print("add people to db")

    firstname = addwindow.lineEditFirstName.text()
    lastname = addwindow.lineEditLastName.text()
    phone = addwindow.lineEditPhone.text()
    note = addwindow.lineEditNote.text()
    dbc.add_people(firstname, lastname, phone, note)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print ("Killing")
            self.deleteLater()
        elif event.key() == QtCore.Qt.Key_A:
            print ("Call Add people")
            handleAddPeopleButton()

        event.accept()

    def mousePressEvent(self, event):
        print("click !")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    table = MyTable(window)
    table.init('db.sqlite', 'QSQLITE')

    window.pushButtonAddPeople.clicked.connect(handleAddPeopleButton)
    window.pushButtonDelPeople.clicked.connect(lambda: handleDelPeopleButton(table))
    window.pushButtonDelPeople.clicked.connect(table.table_create)

    window.lineEditSearch.returnPressed.connect(lambda: handleSearchName(table, window.lineEditSearch.text()))

    addwindow = uic.loadUi("addwindow.ui")
    addwindow.buttonBox.accepted.connect(handleOkButton)
    addwindow.buttonBox.accepted.connect(table.table_create)

    phone_tamplate = QRegExp(r'/\(?([0-9]{3})\)?([ .-]?)([0-9]{2})?([ .-]?)([0-9]{2})/')
    valid = QtGui.QRegExpValidator(phone_tamplate)
    addwindow.lineEditPhone.setValidator(valid)
    addwindow.lineEditPhone.setInputMask("###-##-##")

    window.show()
    app.exec()