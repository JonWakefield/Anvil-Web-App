
#write error log to /home/pi/Desktop/Anvil/uplink_dev/Pides_VIEWER/error_log.txt.txt

import datetime

# Uplink imports:
try:
    import utils.mySQL_utils as sql
    from Globals import ERROR_LOG_PATH, DEBUG_LOG_PATH

# Local host imports:
except (ModuleNotFoundError) as mod_err:
    print("trying local host imports in log_errors_utils.py")
    from . import mySQL_utils as localSQL
    from Globals import ERROR_LOG_PATH, DEBUG_LOG_PATH


def write_error_log(err_msg):

    # get the current date time 
    current_datetime = datetime.datetime.now()

    # Formate the datetime
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    err_msg += " :  " + formatted_datetime


    # save
    try:
        fp = open(ERROR_LOG_PATH,"a+")

        err_msg += "\n\n"
        
        fp.write(err_msg)
        print("wrote message")
        fp.close()
    except (Exception) as err:
        print(f"error in log_errors_uitls.\n Unable to log error message {err}")
    
    
def write_debug_log(sMsg):
    
    sTime = sql.get_time()
    sDate = sql.get_date()

    sMsg += " :  " + sTime + ", " + sDate

    try:
        # save
        fp = open(DEBUG_LOG_PATH,"a+")

        sMsg += "\n\n"
        
        fp.write(sMsg)

        fp.close()
    except (Exception) as err:
        print(f"error in log_errors_uitls.\n Unable to log debug message {err}")