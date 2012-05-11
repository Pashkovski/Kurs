# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import queries
import comparison

# для правильного отображения кириллицы
Instanse = QtCore.QObject
def trUtf8(Instance, SourceText):
    return QtCore.QObject.trUtf8(Instance, SourceText)

class MyWindow(QtGui.QWidget):
    ### состояние окна ###
    # 0 - не инициализировано
    # 1 - только запущено
    # 2 - выбрана категория
    # 3 - выбрана подкатегория
    # 4 - нажата кнопка "Показать"
    condition=0
    
    RIGHTPARTWIDTH = 250  # ширина правой части окна
    LEFTPARTWIDTH  = 380  # ширина левой  части окна
    WINDOWWIDTH    = 700  # ширина окна
    WINDOWHEIGHT   = 600  # высота окна
    CHARACSPACING  = 10   # отступ между формами ввода значений
    
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)

        ### настройки окна ###
        self.setWindowTitle(trUtf8(app,"Подбор и сравнение товаров в интернет-магазине"))
        self.setFixedSize(self.WINDOWWIDTH,self.WINDOWHEIGHT)
        # создание лейблов
        self.label_left=QtGui.QLabel(trUtf8(app,"Выберите категорию товара:"))
        self.label_right1=QtGui.QLabel(trUtf8(app,"<center><b>Категория:</b></center>"))
        # получение родительских категорий
        categories=queries.selectParentCategories(con)
        # создание Combo на основе полученных категорий
        self.combo1=QtGui.QComboBox()
        self.combo1.setFixedWidth(self.RIGHTPARTWIDTH)
        for cat in categories:
            self.combo1.addItem(trUtf8(app,str(cat[0])))
        self.connect(self.combo1, QtCore.SIGNAL("activated(QString)"),self,QtCore.SLOT("categor(QString)"))
        
        ### добавление всего ###
        self.layout_cent=QtGui.QHBoxLayout()
        self.layout_left=QtGui.QVBoxLayout()
        self.layout_right=QtGui.QVBoxLayout()
        self.layout_left.addWidget(self.label_left)
        self.layout_right.addWidget(self.label_right1)
        self.layout_right.addWidget(self.combo1)
        self.layout_right.addStretch()
        self.layout_cent.addLayout(self.layout_left)
        self.layout_cent.addStretch()
        self.layout_cent.addLayout(self.layout_right)
        self.setLayout(self.layout_cent)
        
        ### новое состояние ###
        self.condition=1
        
        
    ###### При выборе категории ######
    @QtCore.pyqtSlot('QString')
    def categor(self, value):
        ### изменяем текст слева ###
        self.label_left.setText(trUtf8(app,"Выберите подкатегорию товара:"))
        
        ### изменения на self.layout_right и self.layout_left
        ### при  попадании из разных состояний
        if self.condition==1:
            it=self.layout_right.itemAt(2)
            self.layout_right.removeItem(it)
            self.label_right2=QtGui.QLabel(trUtf8(app,"<center><b>Подкатегория:</b></center>"))
            self.layout_right.addWidget(self.label_right2)
        if self.condition==2:
            it=self.layout_right.itemAt(4)
            self.layout_right.removeItem(it)
            self.layout_right.removeWidget(self.combo2)
            self.combo2.deleteLater()
        if self.condition in (3,4):
            it=self.layout_right.itemAt(5)
            self.layout_right.removeItem(it)
            self.layout_right.removeWidget(self.widget_inner)
            self.widget_inner.deleteLater()
            self.layout_right.removeWidget(self.combo2)
            self.combo2.deleteLater()
            if self.condition ==4:
                self.layout_left.removeWidget(self.scr)
                self.scr.deleteLater()
                self.layout_left.removeWidget(self.comparebtn)
                self.comparebtn.deleteLater()
        
        # получение подкатегорий
        info=queries.selectSubCategories(value, con)
        # создание Combo для подкатегорий на основе выбранной категории  
        self.combo2=QtGui.QComboBox()
        self.combo2.setFixedWidth(self.RIGHTPARTWIDTH)
        for el in info:
            self.combo2.addItem(trUtf8(app,str(el[0])))
        self.connect(self.combo2, QtCore.SIGNAL("activated(QString)"),self,QtCore.SLOT("podcategor(QString)"))
        # добавление Combo на Layout
        self.layout_right.addWidget(self.combo2)
        self.layout_right.addStretch()
        
        ### новое состояние ###
        self.condition=2
        
        
    # при выборе подкатегории    
    @QtCore.pyqtSlot('QString')
    def podcategor(self, value):
        ### изменяем текст слева ###
        self.label_left.setText(trUtf8(app,"Выберите требуемые характеристики товара:"))
          
        ### изменения на self.layout_right и self.layout_left
        ### при  попадании из разных состояний
        if self.condition==2:
            it=self.layout_right.itemAt(4)
            self.layout_right.removeItem(it)
        if self.condition in (3,4):
            it=self.layout_right.itemAt(5)
            self.layout_right.removeItem(it)
            self.layout_right.removeWidget(self.widget_inner)
            self.widget_inner.deleteLater()
            if self.condition ==4:
                self.layout_left.removeWidget(self.scr)
                self.scr.deleteLater()
                self.layout_left.removeWidget(self.comparebtn)
                self.comparebtn.deleteLater()
        
        # сохранение информации о текущей подкатегории
        info=queries.selectCategoryId(value, con)
        self.current_subcategory=str(info[0][0])
        
        # получение информации о характеристиках текущей подкатегории
        info=queries.selectAllFromCharacteristics(self.current_subcategory, con)
        
        # создание Widget и Layout для добавления на них элеметов
        self.widget_inner=QtGui.QWidget()
        self.widget_inner.setFixedWidth(self.RIGHTPARTWIDTH)
        self.layout_inner=QtGui.QVBoxLayout()
        
        # массивы с текущей информацией о набранных характеристиках
        self.widgets_array=[]
        self.ch_id_array=[]
        self.types_array=[]
        
        ### добавление элементов на widget_inner и в массив ###
        label_right3=QtGui.QLabel(trUtf8(app,"<center><b>Характеристики:</b></center>"))
        self.layout_inner.addWidget(label_right3)
        for el in info:     # цикл по каждой характеристике из выбранной подкатегории
            # el[0] - ch_name, el[1] - ch_type, el[2] - ch_id
            # добавляем label с названием характеристики
            text_for_label=QtCore.QString("<center>")
            text_for_label.append(trUtf8(app,el[0]))
            text_for_label.append("</center>")
            label_next=QtGui.QLabel(text_for_label,self.widget_inner)
            self.layout_inner.addWidget(label_next)
            ### добавляем формы для ввода её значений ###
            if el[1]=='ran':
                ### если это не перечислимая характеристика ###
                # создаём горизонтальный layout для компоновки форм
                layout_next=QtGui.QHBoxLayout()
                # создаём формы
                lab_next_from=QtGui.QLabel(trUtf8(app,"От"),self.widget_inner)
                l_e_next_from=QtGui.QLineEdit(self.widget_inner)
                lab_next_to=QtGui.QLabel(trUtf8(app,"До"),self.widget_inner)
                l_e_next_to=QtGui.QLineEdit(self.widget_inner)
                # по-умолчанию ставим минимальное и максимальное значение из базы
                minVal=queries.selectMinValueForCertainCharacteristic(el[2],self.current_subcategory,con)
                l_e_next_from.setText(str(minVal))
                maxVal=queries.selectMaxValueForCertainCharacteristic(el[2],self.current_subcategory,con)
                l_e_next_to.setText(str(maxVal))
                # соединяем формы со слотом
                self.connect(l_e_next_from, QtCore.SIGNAL("textEdited(QString)"),self,QtCore.SLOT("changeRanChar(QString)"))
                self.connect(l_e_next_to, QtCore.SIGNAL("textEdited(QString)"),self,QtCore.SLOT("changeRanChar(QString)"))
                # сохраняем инфо в массивы с текущей информацией
                self.widgets_array.append(l_e_next_from)
                self.ch_id_array.append(el[2])
                self.types_array.append('from')
                self.widgets_array.append(l_e_next_to)
                self.ch_id_array.append(el[2])
                self.types_array.append('to')
                # добавляем формы на виджет
                layout_next.addWidget(lab_next_from)
                layout_next.addWidget(l_e_next_from)
                layout_next.addWidget(lab_next_to)
                layout_next.addWidget(l_e_next_to)
                # добавляем внутренний layout в layout
                self.layout_inner.addLayout(layout_next)
            else:
                ### если это перечислимая характеристика ###
                # получение из БД всех возможных уникальных значений перечисления
                info2=queries.selectAllDistinctEnumValues(el[2],self.current_subcategory,con)
                # создание Combo и добавление значений перечисления
                combo_new=QtGui.QComboBox()
                # добавление значения "не важно"
                combo_new.addItem(trUtf8(app,"не важно"))
                # добавление остальных значений
                for el2 in info2:
                    combo_new.addItem(trUtf8(app,str(el2[0])))
                # соединяем форму со слотом
                self.connect(combo_new, QtCore.SIGNAL("activated(QString)"),self,QtCore.SLOT("changeEnChar(QString)"))
                # сохраняем инфо в массивы с текущей информацией
                self.widgets_array.append(combo_new)
                self.ch_id_array.append(el[2])
                self.types_array.append('en')
                # добавляем Combo на layout
                self.layout_inner.addWidget(combo_new)
            # добавляем небольшой отступ вниз
            self.layout_inner.addSpacing(self.CHARACSPACING)
            
        ### новое состояние ###
        # (стоит не в конце, т.к. changeChar требует 3 состояния)
        self.condition=3
            
        ### создание лейбла "Найдено" и кнопки "Показать" ###
        self.found=QtGui.QLabel(trUtf8(app,"Найдено : "),self.widget_inner)
        self.showbtn=QtGui.QPushButton(trUtf8(app,"Показать"))
        self.connect(self.showbtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("showResults()"))
        # запуск слота (первое изменение хар-к)
        self.changeChar("init")
        # Размещение их на layout
        layout_bottom=QtGui.QHBoxLayout()
        layout_bottom.addWidget(self.found)
        layout_bottom.addWidget(self.showbtn)
        self.layout_inner.addLayout(layout_bottom)
        
        ### добавление всего на правый Layout ###
        self.widget_inner.setLayout(self.layout_inner)
        self.layout_right.addWidget(self.widget_inner)
        self.layout_right.addStretch()

        
    ### при изменении характеристики ( new_value - новое значение измененной хар-ки ) ###
    @QtCore.pyqtSlot('QString')
    def changeEnChar(self,new_value):
        self.changeChar("init")
    
    
        ### при изменении характеристики ( new_value - новое значение измененной хар-ки ) ###
    @QtCore.pyqtSlot('QString')
    def changeRanChar(self,new_value):
        # далее много проверок на то, что ввёл пользователь
        string_is_valid=True
        for el in new_value:
            if el not in ('0','1','2','3','4','5','6','7','8','9','.'):
                string_is_valid=False
                break
        if new_value.count('.') not in (0,1):
            string_is_valid=False
        if new_value[-1:] not in ('0','1','2','3','4','5','6','7','8','9'):
            string_is_valid=False
        if string_is_valid==True:
            self.changeChar("init")
        else:
            self.showbtn.setEnabled(False)
            # Изменяем кол-во найденных
            strToAdd="<span style='font: bold 14px'>Найдено  :  </span><span style='font: bold 18px'>0</span>"
            self.found.setText(trUtf8(app,strToAdd))
            
    ### непосредственное изменение характеристики ( new_value - новое значение измененной хар-ки ) ###
    ### вызывается методами changeEnChar, changeRanChar и при первой загрузке
    @QtCore.pyqtSlot('QString')
    def changeChar(self,new_value):
        # Получаем кол-во найденных
        fc=self.foundQuantity()
        # Изменяем кол-во найденных
        strToAdd="<span style='font: bold 14px'>Найдено  :  </span><span style='font: bold 18px'>"+str(fc)+"</span>"
        self.found.setText(trUtf8(app,strToAdd))
        
        ### Делаем кнопку "Показать" активной/не активной в зав-ти от кол-ва найденного
        if int(fc)==0:
            self.showbtn.setEnabled(False)
        else:
            self.showbtn.setEnabled(True)
    
    ### возвращает кол-во найденных при заданных параметрах ###
    def foundQuantity(self):
        if self.condition in (3,4): # если окно в 3 или 4 состоянии
            # далее цикл по всем виджетам
            values_array=self.getValuesArray()
            return queries.selectQuantity(self.current_subcategory,self.ch_id_array,self.types_array,values_array,con)
        return 0
    
    
    ### возвращает значения введённых форм (все, по очереди) ###
    def getValuesArray(self):
        values_array=[]
        for el in self.widgets_array:
            if isinstance(el,QtGui.QComboBox):
                cb=QtGui.QComboBox()
                cb=el
                values_array.append(str(cb.currentText()))
            else:
                le=QtGui.QLineEdit()
                le=el
                values_array.append(str(le.text()))
        return values_array

    
    # при нажатии кнопки "Показать"
    @QtCore.pyqtSlot()
    def showResults(self):
        ### изменяем текст слева ###
        self.label_left.setText(trUtf8(app,"<center>Выбранные товары:</center>"))
        
        ### изменения на self.layout_left
        ### при попадании из состояния 4
        if self.condition ==4:
            self.layout_left.removeWidget(self.scr)
            self.scr.deleteLater()
            self.layout_left.removeWidget(self.comparebtn)
            self.comparebtn.deleteLater()
        
        # создаём scrollarea
        self.scr=QtGui.QScrollArea()
        self.scr.setFixedWidth(self.LEFTPARTWIDTH)
        self.scr.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        #self.scr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        # создаём widget и layout для товаров
        com_layout = QtGui.QVBoxLayout()
        com_widget = QtGui.QWidget()
        
        ### заполняем layout ###
        # получаем значения из введённых форм
        values_array=self.getValuesArray()
        # получаем инфо из базы
        allInfo = queries.selectCommodities(self.current_subcategory,self.ch_id_array,self.types_array,values_array,con)
        # распаковываем
        self.ch_info=allInfo[0]           # info:         [ (0-com_id, 1-ch_id,    2-value  ) ... ()]
        self.nameAndPrice=allInfo[1]   # nameAndPrice: [ (0-com_id, 1-com_name, 2-price_r) ... ()]
        
        ### 2 массива для работы функций сравнения товаров ###
        # массив для хранения checkbox -ов ( для получения выбранных товаров)
        self.checkboxes_array=[]
        # массив для хранения id товаров для соответствующих checkbox-ов выше
        self.selected_comm_array=[]
        
        # цикл по всем найденным товарам
        for el in self.nameAndPrice:
            # создаём layout для checkboxa и названия товара
            name_layout=QtGui.QHBoxLayout()
            # создаём checkbox
            name_checkbox=QtGui.QCheckBox()
            self.connect(name_checkbox,QtCore.SIGNAL("stateChanged(int)"),self,QtCore.SLOT("changedCheck(int)"))
            # создаём имя товара
            com_str="<span style='font: bold 14px'>"+str(el[1])+"</span>"
            com_label=QtGui.QLabel(trUtf8(app,com_str))
            # сохраняем в массивы хранения инфы
            self.checkboxes_array.append(name_checkbox)
            self.selected_comm_array.append(el[0])
            # компонуем
            name_layout.addWidget(name_checkbox)
            name_layout.addWidget(com_label)
            com_layout.addLayout(name_layout)
            
            # цену товара вставляем отдельно, т.к. она в отдельном месте лежит
            com_str_new="<p style='font: 12px'>Цена : <b>"+str(el[2])+"</b></p>"
            com_label_new=QtGui.QLabel(trUtf8(app,com_str_new))
            com_layout.addWidget(com_label_new)
            
            # цикл по всем характеристикам товара
            for ch in self.ch_info:
                if ch[0]!=el[0]: continue
                else:
                    # ищем название характеристики
                    char_name=queries.selectCharName(ch[1],con)  ###              
                    # пишем характеристику товара
                    com_str_new="<p style='font: 12px'>"+char_name+" : <b>"+str(ch[2])+"</b></p>"
                    com_label_new=QtGui.QLabel(trUtf8(app,com_str_new))
                    com_layout.addWidget(com_label_new)
            com_layout.addSpacing(50)

        # создание кнопки "Сравнить"
        self.comparebtn=QtGui.QPushButton(trUtf8(app,"Сравнить"))
        self.comparebtn.setEnabled(False)
        self.connect(self.comparebtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("compareComm()"))
        
        #com_layout.addWidget(self.comparebtn)
        
        # добавляем всё в окно
        com_widget.setLayout(com_layout)
        self.scr.setWidget(com_widget)
        self.layout_left.addWidget(self.scr)
        self.layout_left.addWidget(self.comparebtn)
        
        ### новое состояние ###
        self.condition=4

    ### при изменении значений на любом из ЧекБоксов ###
    @QtCore.pyqtSlot('int')
    def changedCheck(self,new_state):
        # смотрим сколько ЧекБоксов выбрано
        count=0
        for i in self.checkboxes_array:
            if i.isChecked(): count +=1
        if count>1:
            self.comparebtn.setEnabled(True)
        else:
            self.comparebtn.setEnabled(False)

    ### при нажатии кнопки "Сравнить" ###
    @QtCore.pyqtSlot()
    def compareComm(self):
        # получаем id товаров, которые нужно сравнить
        compareId=[]
        for i in range(0,len(self.checkboxes_array)):
            if self.checkboxes_array[i].isChecked():
                compareId.append(self.selected_comm_array[i])
        
        ### создание и отображение вложенного окна сравнения
        cw=comparison.CoparisonWindow(self,con,app,compareId,self.current_subcategory)
        cw.show()

    ### при закрытии ###
    def closeEvent(self,event):
        queries.close_connection(con)
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    # подключение к базе
    con=queries.connect_to_db()
    # создание и отображение главного окна
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
    