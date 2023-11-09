

#dump sql camera_nodes; for txd to offServer storage


# mysqldump -u ginuser -pHello2018 camera_nodes > /home/pi/pides_ops/camera_nodes_10_10_2022.sql

import time
import datetime
# import dateTime_utils as dtu
 
year = 2021
month=7
day = 7
hr = 1
mins = 2
secs = 1

timeDate_tuple =  (year, month, day, hr, mins, secs, 0,0,0)

epoch = int(time.mktime(timeDate_tuple))



# for linux:
#epoch = datetime.datetime(year=2021, month=7, 7, 1, 2, 1).strftime('%s')
#epoch = datetime.datetime(timeStruct )
    
# for windows:
# epoch = datetime.datetime(2021, 7,7 , 1,2,1).strftime('%S')
#print(epoch)

#returns epoch local time as PlasticCont_Beta is writing local time to fileName; so laser needs to write compatible epoch time
def get_currentEpochTime_secs():
    current_UTC_epochTime_secs = int(time.time())
    
    current_UTC_time_hr = datetime.datetime.utcnow().hour
    current_local_time_hr = datetime.datetime.now().hour
    
    delta_timeDifference = current_UTC_time_hr - current_local_time_hr
    
    if(delta_timeDifference < 0):
        delta_timeDifference += 24     
        
        
    delta_timeZone_secs = 3600 * delta_timeDifference
    
    # print(delta_timeZone_secs)
    
    #time.mktime(current_UTC_time.timetuple())
    #current_epochTime_secs = current_UTC_epochTime_secs - delta_timeZone_secs
    current_epochTime_secs = current_UTC_epochTime_secs
    
    
    return current_epochTime_secs

def get_epoch(year, month, day, hr, mins, secs):
    epoch = 0
    try:
        timeDate_tuple =  (year, month, day, hr, mins, secs, 0,0,0)
    except:
        sMsg = "error converting timedate to epoch, line 38 dateTime_utils.py"
        print(sMsg)

    

    epoch = int(time.mktime(timeDate_tuple))
    
    return epoch
    

def convert_dateTime_to_epoch(sYear, sMonth, sDay, sHr, sMin, sSec):
    year = int(sYear)
    month = int(sMonth)
    day = int(sDay )
    hour = int(sHr)
    mins = int(sMin)
    secs = int(sSec)
    
    
    #structTime = time.localtime()
    #datetime.datetime(*structTime[:6])
    #datetime.datetime(2009, 11, 8, 20, 32, 35)
    dt_timeTuple = datetime.datetime(year, month, day, hour, mins, secs).timetuple()
    
    #time_tuple = (year, month, day, hour, mins, secs,0,0,0)
    #time_obj = time.struct_time(time_tuple)
    
    #epoch_time = int(time.mktime(time_obj))
    epoch_time = int(time.mktime(dt_timeTuple))
    
    return epoch_time
    
    return epoch_time

def extract_HR_Min_Sec_time(sT):
    sHour = ''
    sMin = ''
    sSec = ''
    
    
    sF = sT.split(':')
    
    cnt = len(sF)
    if(cnt >= 3):
        sHour = sF[0]
        sMin=sF[1]
        sSec = sF[2]
        
    return sHour, sMin, sSec

def extract_YR_Day_Mon_date(sD):
    sYear = ''
    sDay = ''
    sMonth = ''
    sF = sD.split('-')
    
    cnt = len(sF)
    if(cnt >= 3):
        sYear = sF[0]
        sDay = sF[2]
        sMonth = sF[1]
    
    return sYear, sDay, sMonth

def extract_dateTime(fileName):
    sDate= ''
    sTime= ''
    
    sF_list = fileName.split('_')
 
    cnt = len(sF_list)
    if(cnt >= 3):
        sName = sF_list[0]
        sDate = sF_list[1]
        sT = sF_list[2]
        
        sT_list = sT.split('.')
        cnt = len(sT_list)
        if(cnt >=2 ):
            sTime = sT_list[0]
        else:
            sMsg = "error line 114 in dateTime_utils.py in extract_dateTime; invalid sT string"
            print(sMsg)
            return sDate, sTime   #return blanks as we have error

    return sDate, sTime

def extract_epochTime(fileName):
    
    epochTime = -99
    
    try:
        sDate, sTime = extract_dateTime(fileName)
        
        sYear, sDay, sMonth = extract_YR_Day_Mon_date(sDate)
        sHour, sMin, sSec = extract_HR_Min_Sec_time(sTime)
        
        epochTime = convert_dateTime_to_epoch(sYear, sMonth, sDay, sHour, sMin, sSec)
    
    except:
        sMsg = "exception caught line 116 in extract_epochTime, dateTime_utils.py"
        print(sMsg)
    
    
    return epochTime

