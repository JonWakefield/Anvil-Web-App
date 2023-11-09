"""
Author: JW
Date: 09/26/2023
Module Name: camera_controls_uplink.py

Description:
    The "gin_monitor_uplink.py" module provides functions for retrieving and simulating images and their ages in a gin 
    monitoring system within an Anvil web application. It interacts with a database using custom SQL utilities and allows users to monitor images, 
    their ages, and the status of Hand Intrusion Events (HIE).

Key Functions:

1. `build_imageFilePathName(gin_name, gin_stand_num)`: Constructs the file path and name for an image based on the gin name and stand number.
2. `get_plastic_image(json_data)`: Retrieves a plastic image, resizes it, and returns it as Anvil BlobMedia for display in the web application.
3. `get_image_ages(json_data: str)`: Retrieves the ages and status of images associated with a gin and its stands, allowing users to monitor image data in real-time.

This module plays a crucial role in providing real-time image monitoring within the Anvil web application, 
allowing users to track images and their ages.
"""

import json
from PIL import Image
import io
import anvil.media
from Globals import IMG_BASE_PATH

#Uplink imports:
try:
    import utils.mySQL_utils as localSQL
    from utils.dateTime_utils import get_currentEpochTime_secs
    from utils.simulate_imageAges import simulate_table_entries
    from utils.log_errors_utils import write_error_log, write_debug_log
# Local Server Imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local server imports in gin_monitory_uplink.py")
    from ..utils import mySQL_utils as localSQL
    from ..utils.log_errors_utils import write_error_log, write_debug_log
    from ..utils.dateTime_utils import get_currentEpochTime_secs
    from ..utils.simulate_imageAges import simulate_table_entries

# Function Working: JW 10/11/2023
def build_imageFilePathName(gin_name: str, gin_stand_num: str) -> str:
    """
        Function Description:
            - Constructs the file path to retrieve the image
        
        Input Args:
            - gin_name(str): Name of the gin where image was captured
            - gin_stand_num(str): Gin stand number in str format

        Output Args:
            - fpathName(str): fully constructed file path used to retrieve the image
    """
    fpathName = IMG_BASE_PATH + gin_name + '/gs' + gin_stand_num + '.png'

    #for testing locally
    # fpathName = '/home/linuxlite/ImageObject_Identifier/img_' + gin_stand_num  + '.png'

    return fpathName

# Function Working: JW 10/11/2023
def get_plastic_image(json_data: json) -> dict:
    """
        Function Description:
            - Called from anvil_uplink_router.get_plastic_image
            - Retrieves the image and converts to type anvil_blob_media to display back to user

        Input Args:
            - json_data = json.dumps({
                    'file_path': file_path_for_gin_stand_number_i,
                    'image_size': self.imageSize, # size of image (Varies based on users screen size)
                })

        Output Args:
            - {
                "image": anvil_image, 
            }
    
    """

    print("Getting a plastic image...")

    python_dict = json.loads(json_data)

    # process the input and determine the image fileName to read in 
    imageSize = python_dict.get("image_size")
    imgFilePathName = python_dict.get("file_path")

    # Get PIL Image:
    pil_img = Image.open(imgFilePathName)

    # Resize Image (if neccessary):
    resized_image = pil_img.resize(imageSize)

    bs = io.BytesIO()

    # Convert to bytes format:
    resized_image.save(bs, format="png")

    # Convert to type anvil.media to pass back to client and display 
    anvil_image = anvil.BlobMedia("image/png", bs.getvalue(), name="cotton") 

    # NOTE: cannot serialized type Anvil. Blob Meida
    return {
        "image": anvil_image, 
    }


# Function Working: JW 10/11/2023
def get_image_ages(json_data: json) -> json:
    """
        Function Description:
            - Called from anvil_uplink_router.get_image_ages
            - Retrieves image ages for each gin stand at a specific gin

        Input Args:
            - json_data = json.dumps({
                'gin_name': self.gin_name,
                'num_gin_stands': self.num_gin_stands
            })

        Output Args:
            - json.dumps({
                "img_time_taken": img_time_list, # list of times when plastic event occured (1 index for each gin stand num)
                "file_paths": file_path_list, # file path to retrieve each image (1 index for each gin stand num)
                "image_ages": age_list, # List of time since plastic event occured (1 index for each gin stand num)
                "HID_status": HID_status_list # list indicating if HIE was active (1 index for each gin stand num)
            })
    
    """
    # Convert json back to python dict:
    python_dict = json.loads(json_data)

    # Unpack the dict
    gin_name = python_dict.get("gin_name")
    num_gin_stands = python_dict.get("num_gin_stands")

    # 
    age_list = []
    img_time_list = []
    file_path_list = []
    HID_status_list = []

    try:
        # Connect to database
        cnx = localSQL.sql_connect()

        # Retrieve the most recent image for each gin stand:
        for i in range(num_gin_stands):
            select_query = f"SELECT pic_age, file_name, HID_status FROM gin_stand_events WHERE gin_name = '{gin_name}' AND gin_stand_num = {i+1} ORDER BY Id DESC LIMIT {1};"

            result = localSQL.sql_select(cnx, select_query)

            # If we find an image for a specific gin stand #, enter here:
            if result:
                result = result[0]
                # print(f"result in get_last_n_rows is {result} of type {type(result)}")

                # Time image was taken
                img_time_taken = result[0]
                # File path to image
                file_path = result[1]
                # Was HID active during the capture? (T/F)
                HID_status = result[2]

                # Subtract from current time:
                currentTime = get_currentEpochTime_secs()
                # Get time since image capture
                image_age = int((int(currentTime) - int(img_time_taken)) / 60) # convert to mins

                # Store all results in a list for returning back to user:
                age_list.append(image_age)
                img_time_list.append(img_time_taken)
                file_path_list.append(file_path)
                HID_status_list.append(HID_status)

            # If we don't find an entry for a specific gin stand num, enter else:
            else:
                # If we don't find an image, use no_image_found.png
                print(f"No entry found for gin {gin_name} stand {i}")
                no_image_path = "/var/www/PidesMonitor/images/no_image_found.png"
                # Set length of time to be anything:
                age_list.append(9999)
                img_time_list.append(9999) # high number
                file_path_list.append(no_image_path)
                HID_status_list.append(False)


    except(Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: gin_monitor_uplink, Function: get_image_ages func.\nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)

    finally:
        localSQL.sql_closeConnection(cnx)
       
    return json.dumps({
        "img_time_taken": img_time_list,
        "file_paths": file_path_list,
        "image_ages": age_list,
        "HID_status": HID_status_list
    })


def _simulate_events(gin_name: str):
    """ DEVELOPMENT FUNCTION, NOT USED IN DEPLOYMENT:

        Function Description:
            - Simulates plastic events occuring for a particular gin 

        Input Args:
            - gin_name (str): name of gin to simulate events for

    """
    simulate_table_entries(gin_name)


