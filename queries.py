# -*- coding: utf-8 -*-
import psycopg2

def connect_to_db():
    # подключение к базе
    conn_str = "dbname=comm user=reader password=000000 port=5432"
    con=psycopg2.connect(conn_str)
    return con

def close_connection(con):
    con.close()

### для выполнения запроса ###
def executeQuery(query,con):
    cur = con.cursor()
    cur.execute(query)
    info=cur.fetchall()
    con.commit()
    cur.close()
    return info

### получение массива родительских категорий ###
def selectParentCategories(con):
    inf=executeQuery("select cat_name from categories where parent_cat_id is null;",con)
    return inf

### получение подкатегорий по заданной категории ###
def selectSubCategories(parentCategoryId,con):
    query="select cat_name from categories where parent_cat_id= "
    query+=" (select cat_id from categories where cat_name='"+str(parentCategoryId)+"');"
    inf=executeQuery(query,con)
    return inf

### получение id категории по её имени ###
def selectCategoryId(categoryName,con):
    inf=executeQuery("select cat_id from categories where cat_name='"+str(categoryName)+"';",con)
    return inf

### получение всех характеристик по категории ###
def selectAllFromCharacteristics(category,con):
    query="select ch_name,ch_type,ch_id from characteristics where ch_id in "
    query+=" (select ch_id  from categories_characteristics "
    query+=" where cat_id="+category+");"
    inf=executeQuery(query,con)
    return inf

### получение уникальных значений из базы по характеристике и категории ###
def selectAllDistinctEnumValues(characteristicId,category,con):
    query="select distinct a.value from commodities_characteristics a "
    query+=" inner join characteristics b on a.ch_id=b.ch_id "
    query+=" where b.ch_type='en' and a.ch_id="+str(characteristicId) 
    query+=" and com_id in (select com_id from commodities where cat_id="+str(category)+");"
    inf=executeQuery(query,con)
    return inf

### получение минимального значения из базы по характеристике и категории ###
def selectMinValueForCertainCharacteristic(characteristicId,category,con):
    query= "select min(CAST(a.value AS real)) from commodities_characteristics a "
    query+=" inner join characteristics b on a.ch_id=b.ch_id "
    query+=" where b.ch_type='ran' and a.ch_id="+str(characteristicId)+" "
    query+=" and com_id in (select com_id from commodities where cat_id="+str(category)+");"
    inf=executeQuery(query,con)
    return inf[0][0]
    
### получение максимального значения из базы по характеристике и категории ###
def selectMaxValueForCertainCharacteristic(characteristicId,category,con):
    query= "select max(CAST(a.value AS real)) from commodities_characteristics a "
    query+=" inner join characteristics b on a.ch_id=b.ch_id "
    query+=" where b.ch_type='ran' and a.ch_id="+str(characteristicId)+" "
    query+=" and com_id in (select com_id from commodities where cat_id="+str(category)+");"
    inf=executeQuery(query,con)
    return inf[0][0]

### возвращает строку подзапроса для получения набора товаров,      ###
### удовлетворяющих условиям поиска                                 ###
### (для использования функциями selectQuantity и selectCommodities ###
def getCommSubQuery2(category,ch_id_array,types_array,values_array,con):
    query=" "
    # цикл по всем характеристикам
    for i in range(0,len(ch_id_array)):
        if types_array[i]=='from':
            query+=" select cc.com_id from commodities_characteristics cc "
            query+=" inner join commodities c on c.com_id=cc.com_id "
            query+=" where c.cat_id="+str(category)+" "
            query+=" and cc.ch_id="+str(ch_id_array[i])+" "
            query+=" and CAST(cc.value AS real) between "+str(values_array[i])+" and "+str(values_array[i+1])+" "
        elif types_array[i]=='to':
            continue
        else:
            query+=" select cc.com_id from commodities_characteristics cc "
            query+=" inner join commodities c on c.com_id=cc.com_id "
            query+=" where c.cat_id="+str(category)+" "
            query+=" and cc.ch_id="+str(ch_id_array[i])+" "
            query+=" and cc.value='"+str(values_array[i])+"' "
        query+="  INTERSECT"
    # обрезка последнего 'intersect'
    query = query[:-10]
    return query

def getCommSubQuery(category,ch_id_array,types_array,values_array,con):
    query=" "
    # цикл по всем характеристикам
    for i in range(0,len(ch_id_array)):
        if types_array[i]=='from':
            query+=" select cc.com_id from commodities_characteristics cc "
            query+=" inner join commodities c on c.com_id=cc.com_id "
            query+=" where c.cat_id="+str(category)+" "
            query+=" and cc.ch_id="+str(ch_id_array[i])+" "
            query+=" and CAST(cc.value AS real) between "+str(values_array[i])+" and "+str(values_array[i+1])+" "
        elif types_array[i]=='to':
            continue
        else:
            query+=" select cc.com_id from commodities_characteristics cc "
            query+=" inner join commodities c on c.com_id=cc.com_id "
            query+=" where c.cat_id="+str(category)+" "
            if str(values_array[i])!="не важно":
                query+=" and cc.ch_id="+str(ch_id_array[i])+" "
                query+=" and cc.value='"+str(values_array[i])+"' "
        query+="  INTERSECT"
    # обрезка последнего 'intersect'
    query = query[:-10]
    return query

### получение количества найденных товаров по заданным параметрам ###
def selectQuantity(category,ch_id_array,types_array,values_array,con):
    # формирование строки подзапроса
    query=getCommSubQuery(category,ch_id_array,types_array,values_array,con)
    # формирование запроса:
    query="select count(*) from ( "+query+" ) as tab;"
    # исполнение запроса
    inf=executeQuery(query,con)
    inf=inf[0][0]
    return inf
    
### получение инф-ции о найденных товарах по заданным параметрам ###
def selectCommodities(category,ch_id_array,types_array,values_array,con):
    # формирование строки подзапроса, возвращающего номера товаров, удовлетворяющих поиску
    subquery=getCommSubQuery(category,ch_id_array,types_array,values_array,con)
    subquery=" select distinct tab.com_id from ( "+subquery+" ) as tab "
    # формирование запроса, возвращающего информацию по характеристикам товаров
    query =" select * from commodities_characteristics"
    query+=" where com_id in ( "+subquery+" );"
    # формирование запроса, возвращающего имя и цену товаров
    query2 =" select com_id,com_name,price_r from commodities"
    query2+=" where com_id in ( "+subquery+" ) order by com_id asc;"
    # исполнение запросов
    info=executeQuery(query,con)
    nameAndPrice=executeQuery(query2,con)
    # упаковка и возврат
    allInfo=[info,nameAndPrice]
    return allInfo


### получение имени характеристики по ch_id ###
def selectCharName(ch_id,con):
    query= " select ch_name from characteristics "
    query+=" where ch_id="+str(ch_id)+" ;"
    inf=executeQuery(query,con)
    return inf[0][0]

### получение значения характеристики по com_id,ch_id ###
def selectCharacteristicValue(com_id,ch_id,con):
    query= " select value from commodities_characteristics "
    query+=" where ch_id="+str(ch_id)+" and com_id="+str(com_id)+" ;"
    inf=executeQuery(query,con)
    return inf[0][0]

### получение названия товара по com_id ###
def selectCommodityName(com_id,con):
    query= " select com_name from commodities "
    query+=" where com_id="+str(com_id)+" ;"
    inf=executeQuery(query,con)
    return inf[0][0]

### получение цены реализации товара по com_id ###
def selectCommodityPrice(com_id,con):
    query= " select price_r from commodities "
    query+=" where com_id="+str(com_id)+" ;"
    inf=executeQuery(query,con)
    return inf[0][0]
