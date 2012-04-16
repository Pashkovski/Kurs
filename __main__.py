﻿# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import psycopg2

Instanse = QtCore.QObject
def trUtf8(Instance, SourceText):
    return QtCore.QObject.trUtf8(Instance, SourceText)

class MyWindow(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        con=psycopg2.connect("dbname=comm user=postgres password=abc678 port=5432")
        cur = con.cursor()
   
        self.setWindowTitle(trUtf8(app,"Подбор и сравнение товаров в интернет-магазине"))
        self.resize(700, 700)
        self.layout_cent=QtGui.QHBoxLayout()
        self.layout_left=QtGui.QVBoxLayout()
        self.layout_right=QtGui.QVBoxLayout()
    
        self.label_left=QtGui.QLabel(trUtf8(app,"Выберите категорию товара:"))
        self.label_right1=QtGui.QLabel(trUtf8(app,"Категория:"))
        cur.execute("select cat_name from categories where parent_cat_id is null;")
        info=cur.fetchall()
        self.checklist_right1=QtGui.QComboBox()
        for el in info:
            self.checklist_right1.addItem(trUtf8(app,str(el[0])))
        self.connect(self.checklist_right1, QtCore.SIGNAL("activated(QString)"),self,QtCore.SLOT("categor(QString)"))
        self.layout_left.addWidget(self.label_left)
        self.layout_right.addWidget(self.label_right1)
        self.layout_right.addWidget(self.checklist_right1)
        self.layout_cent.addLayout(self.layout_left)
        self.layout_cent.addLayout(self.layout_right)
    
        con.commit()
        cur.close()
        con.close()
        self.setLayout(self.layout_cent)
        
    @QtCore.pyqtSlot('QString')
    def categor(self, value):
        self.label_left.setText(trUtf8(app,"Выберите подкатегорию товара"))
        
        # удаление ненужного на self.layout_right
        if self.layout_right.count()==3:
            it=self.layout_right.itemAt(2)
            self.layout_right.removeItem(it)
            
        con=psycopg2.connect("dbname=comm user=postgres password=abc678 port=5432")
        cur = con.cursor()
        cur.execute("select cat_name from categories where parent_cat_id=(select cat_id from categories where cat_name='"+str(value)+"');")
        info=cur.fetchall()
        self.checklist_right2=QtGui.QComboBox()
        for el in info:
            self.checklist_right2.addItem(trUtf8(app,str(el[0])))
        con.commit()
        cur.close()
        con.close()
        self.layout_right.addWidget(self.checklist_right2)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
