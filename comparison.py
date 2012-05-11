# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import queries

# для правильного отображения кириллицы
Instanse = QtCore.QObject
def trUtf8(Instance, SourceText):
    return QtCore.QObject.trUtf8(Instance, SourceText)

class CoparisonWindow(QtGui.QDialog):
    
    def __init__(self,parent,con,app,compareId,current_subcategory):
        QtGui.QDialog.__init__(self, parent)
        
        self.setModal(True)
        
        ### Настройки окна ###
        self.setWindowTitle(trUtf8(app,"Сравнение товаров"))
        
        # Создание главного Layout
        main_layout=QtGui.QGridLayout()
        
        # добавление 2 ячеек
        label_new=QtGui.QLabel(trUtf8(app,"<b>Название</b>"))
        main_layout.addWidget(label_new,0,0)
        label_new=QtGui.QLabel(trUtf8(app,"<b>Цена</b>"))
        main_layout.addWidget(label_new,1,0)
        
        # добавление названий и цен
        # цикл по всем выбранным к сравнению товарам
        for s in range(0,len(compareId)):
            current_comm=compareId[s] # текущий товар
            # добавление названия
            current_comm_name  = queries.selectCommodityName(current_comm,con)
            label_new=QtGui.QLabel(trUtf8(app,"<b>"+str(current_comm_name)+"</b>"))
            main_layout.addWidget(label_new,0,s+1)
            # добавление цены
            current_comm_price = queries.selectCommodityPrice(current_comm,con)
            label_new=QtGui.QLabel(trUtf8(app,str(current_comm_price)))
            main_layout.addWidget(label_new,1,s+1)
        
        # получение инф-ции о характеристиках данной подкатегории
        # [(0-ch_name,1-ch_type,2-ch_id)...()]
        all_char=queries.selectAllFromCharacteristics(current_subcategory, con)
        # цикл по всем характеристикам
        for el in range(0,len(all_char)):
            current_char=all_char[el]    # текущая характеристика
            #добавляем label с её названием
            label_new=QtGui.QLabel(trUtf8(app,"<b>"+current_char[0]+"</b>"))
            main_layout.addWidget(label_new,el+2,0)
            # цикл по всем выбранным к сравнению товарам
            for s in range(0,len(compareId)):
                current_comm=compareId[s]
                current_comm_value=queries.selectCharacteristicValue(current_comm, current_char[2], con)
                label_new=QtGui.QLabel(trUtf8(app,str(current_comm_value)))
                main_layout.addWidget(label_new,el+2,s+1)
        
        # добавление layout
        self.setLayout(main_layout)
        