""" Author: Jon Wakefield
    Date: 10/02/2023

    DESCRIPTION:
        - Stores server side globals variables for the Pides_VIEWER web-app.
        - Each Global variable or function includes commnets indicating where in the program the function / variable is called

"""
import json
import pandas as pd
from PIL.Image import Image


""" TYPE HINT GLOBALS: """
# Custom type hint for anvil_media (images)
AnvilMedia = Image
"""************************"""


""" GLOBAL VARIABLES: """
# JWT KEY (location of use: user_management.py):
JWT_KEY = "cotton2023"

# PATH GLOBALS:

# Location of Use: log_errors_utils.write_error_log
ERROR_LOG_PATH = r"/home/dcotton/app/logs/error_log.txt"
# ERROR_LOG_PATH = r"logs/error_log.txt"


# Location of Use: log_errors_utils.write_debug_log
DEBUG_LOG_PATH = r"/home/dcotton/app/logs/debug_log.txt"
# DEBUG_LOG_PATH = r"logs/debug_log.txt"

# Location of Use: gin_monitor_uplink.build_imageFilePathName
IMG_BASE_PATH = r"/var/www/PidesMonitor/images/"
""" ******************** """



""" GLOBAL FUNCTIONS: """

# Finished: JW 07/26/2023
def df2serialized(df: pd.DataFrame) -> json:
    """
        Function Description:
            -
            
        Input Args:
            -

        Output Args:
            -
    """
    """ Convert pandas df to serialized text for http request """
    # 

    #convert dataframe to dictionary
    data_dict = df.to_dict(orient='records')

    # Convert dictionary to JSON string:
    json_data = json.dumps(data_dict)
    
    return json_data

# Finished: JW 07/26/2023
def serialized2df(data: json) -> pd.DataFrame:
    """
        Function Description:
            -
            
        Input Args:
            -

        Output Args:
            -
    """
    """ Convert JSON to unserialized format pandas DataFrame """
    
    # load json string to dictionary
    dict_data = json.loads(data)

    # convert dictionary to dataframe:
    df = pd.DataFrame(dict_data)

    return df

""" ***************** """