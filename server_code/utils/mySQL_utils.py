import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
#!/usr/bin/env python3

### utils for local control of mySQL dbases

# must install 8.0.29 as 8.0.30 (latest version) has major issues that cause it not to work (utf8 errors)
#$ sudo pip3 install mysql-connector-python==8.0.29


#import pymysql   #this version is no longer stable, avoid

#works: tested {select, update, insert}
import mysql.connector  
import sys
import time

from threading import Thread


hostname = 'maria-db' # use the name of the service in the docker-compose file 
# hostname = 'localhost' 
username = 'ginuser'
pswd = 'Hello2018'
database = 'camera_nodes'

tableName = "Camera_Configuration"


#from getpass import getpass
from mysql.connector import connect, Error


#helper functions
import datetime as datetime
from datetime import date, timedelta

import time

#returns current date as string
def get_date() -> str:
    today = date.today()

    # dd/mm/YY
    sDate = today.strftime("%d/%m/%Y")
    print("sDate =", sDate)

    return sDate

def get_time() -> str:
    from datetime import datetime
    now = datetime.now()

    sTime = now.strftime("%H:%M:%S") 

    print("sTime: ", sTime)
    print()

    return sTime



def sql_connect(sql_user='ginuser',sql_password='Hello2018',sql_host='maria-db', sql_database='camera_nodes', sql_port=3306):
    try:
        # print("try  connection")
        cnx = mysql.connector.connect(user=sql_user, password=sql_password, host=sql_host, database=sql_database, port=sql_port)
        
        # print("cnx: ", cnx)  #will print something if it connects ok
        
        return cnx

    except Error as e:
        print(f"local SQL error: {e}")


def sql_closeConnection(cnx):
    try:
        cnx.close()
    except Error as e:
        print(e)



#select_query = 'select Number_of_Pics_to_Take, Progress_PicCapture from Camera_Configuration where Id=7'
#returns enumerable object; example at bottom of func on how to parse result (commented out); also see test_sql_select(...)
def sql_select(cnx, select_query):
    
    #print("try  connection")
    #cnx = mysql.connector.connect(user='ginuser', password='Hello2018', host='127.0.0.1', database='camera_nodes', port=3306)
    
    #print("cnx: ", cnx)  #will print something if it connects ok
    
    cursor = cnx.cursor()
    
    cursor.execute(select_query)
    #cnx.commit()
    
    result = cursor.fetchall()
    
    #for x in result:
    #    print("nPics: ",x)
    
    #cnx.close()    
    return result



#shows how to use
def test_sql_select():

    cnx = sql_connect()

    select_query = 'select Number_of_Pics_to_Take, Progress_PicCapture from Camera_Configuration where Id=7'
    result = sql_select(cnx, select_query)
    
    #use these commented out lines in your code to enumerate out results
    for x in result:
        print("nVals: ",x)
    
    sql_closeConnection(cnx)
    


# select in a range
# sQuery = 'select Epoch from Lidar where Epoch IN(%s,%s)'%( str(startEpoch), str(stopEpoch))



#insert_query = 'INSERT INTO Lidar (port, GinName, GinStandNum, RSSI, Distance) VALUES (2200, "Home", 2, 55, 101)'
def sql_insert(cnx, insert_query):
    
    #print("try  connection")
    #cnx = mysql.connector.connect(user='ginuser', password='Hello2018', host='127.0.0.1', database='camera_nodes', port=3306)
    
    #print("cnx: ", cnx)  #will print something if it connects ok
    
    cursor = cnx.cursor()
    
    cursor.execute(insert_query)
    cnx.commit()
        
    #cnx.close()


#example of how to use sql_insert(...)
def test_sql_insert():
    
    cnx = sql_connect()
    
    insert_query = 'INSERT INTO Lidar (port, GinName, GinStandNum, RSSI, Distance) VALUES (2200, "Home", 2, 55, 101)'
    sql_insert(cnx, insert_query)

    sql_closeConnection(cnx)
    


#update_query = 'update Camera_Configuration SET Number_of_Pics_to_Take=11 where Id=7'
def sql_update(cnx, update_query):
   
    cursor = cnx.cursor()
    
    cursor.execute(update_query)
    cnx.commit()


#example of how to use sql_update(...)
def test_sql_update():

    cnx = sql_connect()

    update_query = 'update Camera_Configuration SET Number_of_Pics_to_Take=12 where Id=7'
    sql_update(cnx, update_query)

    sql_closeConnection(cnx)
    

