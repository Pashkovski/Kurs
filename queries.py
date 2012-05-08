# -*- coding: utf-8 -*-
import psycopg2

def connect_to_db():
    # подключение к базе
    conn_str = "dbname=comm user=postgres password=abc678 port=5432"
    con=psycopg2.connect(conn_str)
    return con

def close_connection(con):
    con.close()

# для выполнения запроса
def executeQuery(query,con):
    cur = con.cursor()
    cur.execute(query)
    info=cur.fetchall()
    con.commit()
    cur.close()
    return info

def selectParentCategories(con):
    inf=executeQuery("select cat_name from categories where parent_cat_id is null;",con)
    return inf

def selectSubCategories(parentCategoryId,con):
    query="select cat_name from categories where parent_cat_id= "
    query+=" (select cat_id from categories where cat_name='"+str(parentCategoryId)+"');"
    inf=executeQuery(query,con)
    return inf

def selectCategoryId(categoryName,con):
    inf=executeQuery("select cat_id from categories where cat_name='"+str(categoryName)+"';",con)
    return inf

def selectAllFromCharacteristics(category,con):
    query="select ch_name,ch_type,ch_id from characteristics where ch_id in "
    query+=" (select ch_id  from categories_characteristics "
    query+=" where cat_id="+category+");"
    inf=executeQuery(query,con)
    return inf

def selectAllDistinctEnumValues(characteristicId,category,con):
    query="select distinct a.value from commodities_characteristics a "
    query+=" inner join characteristics b on a.ch_id=b.ch_id "
    query+=" where b.ch_type='en' and a.ch_id="+str(characteristicId) 
    query+=" and com_id in (select com_id from commodities where cat_id="+str(category)+");"
    inf=executeQuery(query,con)
    return inf
    
def selectMinValueForCertainCharacteristic(characteristicId,category,con):
    query= "select min(CAST(a.value AS real)) from commodities_characteristics a "
    query+=" inner join characteristics b on a.ch_id=b.ch_id "
    query+=" where b.ch_type='ran' and a.ch_id="+str(characteristicId)+" "
    query+=" and com_id in (select com_id from commodities where cat_id="+str(category)+");"
    inf=executeQuery(query,con)
    return inf
    

def selectMaxValueForCertainCharacteristic(characteristicId,category,con):
    query= "select max(CAST(a.value AS real)) from commodities_characteristics a "
    query+=" inner join characteristics b on a.ch_id=b.ch_id "
    query+=" where b.ch_type='ran' and a.ch_id="+str(characteristicId)+" "
    query+=" and com_id in (select com_id from commodities where cat_id="+str(category)+");"
    inf=executeQuery(query,con)
    return inf
    
def selectQuantity(category,ch_id_array,types_array,values_array,con):
    # формирование строки запроса
    query=" "
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
    # и окончательно:
    query="select count(*) from ( "+query+" ) as tab;"
    inf=executeQuery(query,con)
    inf=inf[0][0]
    return inf
    
    
def selectCommodities(category,ch_id_array,types_array,values_array,con):
    # формирование строки подзапроса, возвращающего номера товаров, удовлетворяющих поиску
    subquery=" "
    for i in range(0,len(ch_id_array)):
        if types_array[i]=='from':
            subquery+=" select cc.com_id as com_id from commodities_characteristics cc "
            subquery+=" inner join commodities c on c.com_id=cc.com_id "
            subquery+=" where c.cat_id="+str(category)+" "
            subquery+=" and cc.ch_id="+str(ch_id_array[i])+" "
            subquery+=" and CAST(cc.value AS real) between "+str(values_array[i])+" and "+str(values_array[i+1])+" "
        elif types_array[i]=='to':
            continue
        else:
            subquery+=" select cc.com_id from commodities_characteristics cc "
            subquery+=" inner join commodities c on c.com_id=cc.com_id "
            subquery+=" where c.cat_id="+str(category)+" "
            subquery+=" and cc.ch_id="+str(ch_id_array[i])+" "
            subquery+=" and cc.value='"+str(values_array[i])+"' "
        subquery+="  INTERSECT"
    # обрезка последнего 'intersect'
    subquery = subquery[:-10]
    # и окончательно:
    subquery="select distinct tab.com_id from ( "+subquery+" ) as tab;"
    
    inf=executeQuery(subquery,con)
    return str(inf)
    #return subquery


