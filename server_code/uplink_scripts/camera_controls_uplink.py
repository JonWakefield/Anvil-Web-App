"""
Author: JW
Date: 09/26/2023
Module Name: camera_controls_uplink.py


Description:
This Python module, "camera_controls_uplink.py," provides functions for managing camera controls and settings within an Anvil web application. 
It interacts with a database using custom SQL utilities to retrieve and modify camera-related configurations.

Key Functions:

1. `get_gin_location(gin_name: str) -> str`: Retrieves the location (state) of a gin based on its name.
2. `check_user_node_access(users_gins_accessible: list, nodes_gin: str) -> bool`: Checks if a user has access to a specific node based on their accessible gins.
3. `get_nodes_cam_settings(port_num: int)`: Retrieves camera settings for a connected node to display in the user interface.
4. `connect_to_node(node_data: json)`: Connects to a specified node, providing information about the node and its settings.
5. `update_node_color_balance(color_balance: int, port_num: int) -> bool`: Updates the color balance setting for a node.
6. `update_node_exposure_settings(exposure: str, port_num: int) -> bool`: Updates the exposure setting for a node.
7. `update_node_gain_settings(gain: float, port_num: int) -> bool`: Updates the gain setting for a node.
8. `update_blobsize_settings(min_blobsize: float, port_num: int) -> bool`: Updates the minimum blob size setting for a node.
9. `update_roi_settings(startx: float, stopx: float, starty: float, stopy: float, port_num: int) -> bool`: Updates the Region of Interest (ROI) settings for a node.
10. `modify_camera_settings(settings_data: json)`: Modifies camera settings based on user requests, including color balance, exposure, gain, and ROI.

This module plays a crucial role in managing and customizing camera settings, 
facilitating real-time monitoring and control of camera devices within the Anvil web application.
"""

import json
from typing import List, Dict

# Uplink imports:
try:
    import utils.mySQL_utils as localSQL
    from utils.log_errors_utils import write_error_log, write_debug_log

# Local server imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local imports in camera_controls_uplink.py")
    from ..utils import mySQL_utils as localSQL
    from ..utils.log_errors_utils import write_error_log, write_debug_log



# Working Function: JW - 10/10/2023
def get_gin_location(gin_name: str) -> str:
    """
        Function Description:
            - Called from connect_to_node, finds and returns the location (state) of the gin
                where the user entered node is located.

        Input Args:
            - gin_name (str): name of gin, used to retrieve location of the gin in select_query

        output args:
            - location (str): state where gin_name is located
    
    """

    try:
        cnx = localSQL.sql_connect()

        select_query = f"SELECT location FROM gins WHERE gin_name = '{gin_name}'"

        result = localSQL.sql_select(cnx, select_query)

        if result:
            location = result[0]

            return location

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: get_gin_location func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)


# Working Function: JW - 10/10/2023
def check_user_node_access(users_gins_accessible: List[str], nodes_gin: str) -> bool:
    """ 
        Function Description::
        - Called from camera_controls_uplink.connect_to_node.
        - Checks if the node found in the database, can be accessed by the user based on the gins the user has access to

        Input Args:
        - users_gins_accessible (list[str]): Stores list of gin_names user can access
            (Ex: ["UCG","Spade",...])

        Output Args:
        - Bool: Indicates (T/F) if user can access gin where the node is located
    
    """

    # Loop through the users accessible gins comparing them with the found nodes gin:
    for gin in users_gins_accessible:
        # Check if user has access to the node's gin:
        if(gin == nodes_gin):
            print(f"Found gin")
            return True

    # User does not have access to the node's gin:
    print("No gin gound!")
    return False


# Working Function: JW - 10/10/2023
def get_nodes_cam_settings(port_num: int) -> dict:
    """
        Function Description
            - Called from connect_to_node, retrieves the nodes already stored camera settings to display onto the UI

        Input Args:
            - port_num (int): ssh port number for the node to retrieve the camera settings

        Output Args:
            - cam_settings_dict (dict): dictionary containing retrieved camera settings from select_query
            - returns back to connect_to_node 
                cam_settings_dict = {
                    'color_balance': color_balance,
                    'gain': gain,
                    'exposure': exposure,
                    'min_blobsize': min_blobsize,
                    'roi_startx': roi_startx,
                    'roi_stopx': roi_stopx,
                    'roi_starty': roi_starty,
                    'roi_stopy': roi_stopy
                }
    """

    try:
        cnx = localSQL.sql_connect()

        select_query = f"SELECT ColorBalance, Gain, Exposure, Min_BlobSize, Roi_StartX, Roi_StopX, Roi_StartY, Roi_StopY FROM Camera_Configuration WHERE SSH_Port = {port_num}"

        result = localSQL.sql_select(cnx, select_query)

        if result:
            cam_settings = result[0]
            
            # Unpack settings
            color_balance = cam_settings[0]
            gain = cam_settings[1]
            exposure = cam_settings[2]
            min_blobsize = cam_settings[3]
            roi_startx = cam_settings[4]
            roi_stopx = cam_settings[5]
            roi_starty = cam_settings[6]
            roi_stopy = cam_settings[7]

            # Store in dict to return:
            cam_settings_dict = {
                'color_balance': color_balance,
                'gain': gain,
                'exposure': exposure,
                'min_blobsize': min_blobsize,
                'roi_startx': roi_startx,
                'roi_stopx': roi_stopx,
                'roi_starty': roi_starty,
                'roi_stopy': roi_stopy
            }

            return cam_settings_dict
        else:
            print(f"No pre. configured cam settings found for node {port_num}")

            return False

    except(Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: get_nodes_cam_settings func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)


# Working Function: JW - 10/10/2023
def connect_to_node(node_data: json):
    """
        Function Description:
            - Routed from anvil_uplink_router.connect_to_node, connects to camera node (port #)
            - Retrieves & returns camera settings for camera node

        Input args:
            - node_data = json.dumps({
                'email': users_email,
                'gins_accessible': users_gins_accessible,
                'port_num': user_entered_port_num
            })

        Output args:
            - returned_data = json.dumps({
                'found_node': BOOL (T/F), # indiciates if user entered value was found (If False, client will inform user)
                'gin_name': gin_name, # gin name of node
                'gin_stand_num': gin_stand_num, # gin stand num of node
                'node_position': node_position, # node positon (1 or 2)
                'gin_location': gin_location, # location of gin (state)
                'camera_settings': camera_settings # 
            })
    
    """

    # Convert to python dict
    node_data_dict = json.loads(node_data)

    # Unpack node_data
    email = node_data_dict['email']
    gins_accessible = node_data_dict['gins_accessible']
    port_num = node_data_dict['port_num']

    # Select node using port_num from CamNodes_Info:
    try:
        cnx = localSQL.sql_connect()

        select_query = f"SELECT Active, GinName, GinStandNum, GinStandPositionNum FROM CamNodes_Info WHERE port = {port_num}"

        result = localSQL.sql_select(cnx, select_query)

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: connect_to_node func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)

        # return found_node == False 
        returned_results = json.dumps({'found_node': False})

        return returned_results

    finally:
        localSQL.sql_closeConnection(cnx)

    if result:
        print(f"Found port num {port_num}")

        # Unpack result from select_query:
        result = result[0]
        active = result[0]
        gin_name = result[1]
        gin_stand_num = result[2]
        node_position = result[3]

        # Check if user has access to the gin where the node is located:
        user_accessible_node = check_user_node_access(gins_accessible, gin_name)

        if not user_accessible_node:
            # User does not have access to the gin where the node was found:
            # Package everything up to return to user:
            returned_results = json.dumps({
                'found_node': False,
                'err_code': 2 # return an error code informing user what the issue is with NOT finding the node
            })

            return returned_results
        
        # User can access node, so lets go get nodes location now:
        gin_location = get_gin_location(gin_name)

        # Get nodes camera settings:
        camera_settings = get_nodes_cam_settings(port_num)

        # Package everything up to return to user:
        returned_results = json.dumps({
            'found_node': True,
            'gin_name': gin_name,
            'gin_stand_num': gin_stand_num,
            'node_position': node_position,
            'gin_location': gin_location,
            'camera_settings': camera_settings
        })

        return returned_results

    else:
        print(f"Could not find node with port num {port_num}")

        # Package everything up to return to user:
        returned_results = json.dumps({
            'found_node': False,
            'err_code': 1 # return an error code (error code of 1 correspondes to issue with not finding a node with the entered port number in the database
        })

        return returned_results


# Working Function: JW - 10/10/2023
def update_node_color_balance(color_balance: int, port_num: int) -> bool:
    """
        Function Description:
            - Called from camera_controls_uplink.modify_camera_settings
            - Updates the current color balance setting for the specified port_num

        Input Args:
            - color_balance (int): New color_balance to store in data-table
            - port_num (int): Port # of specific node to update

        Output Args:
            - BOOL: Indicates if successfully updating of color_balance
    

    """
    try:
        cnx = localSQL.sql_connect()

        update_query = f"UPDATE Camera_Configuration SET ColorBalance = {color_balance} WHERE SSH_Port = {port_num}"

        localSQL.sql_update(cnx, update_query)

        # NOTE: need to test what happens when port_num not found
        print(f"successfully update gain for node {port_num}")
        return True

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: update_node_color_balance func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)

# Working Function: JW - 10/10/2023
def update_node_exposure_settings(exposure: str, port_num: int) -> bool:
    """
        Function Description:
            - Called from camera_controls_uplink.modify_camera_settings
            - Updates the current exposure setting for the specified port_num

        Input Args:
            - exposure(str): New exposure value being written to data-table
            - port_num(int): Port # of specific node to update

        Output Args:
            - BOOL: Indicates if successfully updating of exposure
    
    """
    try:
        cnx = localSQL.sql_connect()

        update_query = f"UPDATE Camera_Configuration SET Exposure = '{exposure}' WHERE SSH_Port = {port_num}"

        localSQL.sql_update(cnx, update_query)

        # NOTE: need to test what happens when port_num not found
        print(f"successfully update exposure for node {port_num}")
        return True

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: update_node_exposure_settings func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)

# Working Function: JW - 10/10/2023
def update_node_gain_settings(gain: float, port_num: int) -> bool:
    """
        Function Description:
            - Called from camera_controls_uplink.modify_camera_settings
            - Updates the current gain setting for the specified port_num

        Input Args:
            - gain(float): New gain value being written to data-table
            - port_num(int): Port # of specific node to update

        Output Args:
            - BOOL: Indicates if successfully updating of gain
    
    """
    
    try:
        cnx = localSQL.sql_connect()

        update_query = f"UPDATE Camera_Configuration SET Gain = '{gain}' WHERE SSH_Port = {port_num}"

        localSQL.sql_update(cnx, update_query)

        # NOTE: need to test what happens when port_num not found
        print(f"successfully update gain for node {port_num}")
        return True

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: update_node_gain_settings func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    finally:
        localSQL.sql_closeConnection(cnx)

# Working Function: JW - 10/10/2023
def update_blobsize_settings(min_blobsize: float, port_num: int) -> bool:
    """
        Function Description:
            - Called from camera_controls_uplink.modify_camera_settings
            - Updates the current min_blobsize setting for the specified port_num

        Input Args:
            - min_blobsize(float): New min_blobsize value being written to data-table
            - port_num(int): Port # of specific node to update

        Output Args:
            - BOOL: Indicates if successfully updating of min_blobsize
    
    """

    try:
        cnx = localSQL.sql_connect()

        update_query = f"UPDATE Camera_Configuration SET Min_BlobSize = {min_blobsize} WHERE SSH_Port = {port_num}"

        localSQL.sql_update(cnx, update_query)

        # NOTE: need to test what happens when port_num not found
        print(f"successfully updated min_blobsize for node {port_num}")
        return True

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: update_blobsize_settings func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)

# Working Function: JW - 10/10/2023
def update_roi_settings(startx: float, stopx: float, starty: float, stopy: float, port_num: int) -> bool:
    """
        Function Description:
            - Called from camera_controls_uplink.modify_camera_settings
            - Updates the current roi range settings for the specified port_num

        Input Args:
            - startx (float): Starting x number
            - stopx (float): Stoping x number
            - starty (float): starting y number
            - stopy (float): stoping y number
            - port_num(int): Port # of specific node to update

        Output Args:
            - BOOL: Indicates if successfully updating of roi range
    
    """

    try:
        cnx = localSQL.sql_connect()

        update_query = f"UPDATE Camera_Configuration SET Roi_StartX = {startx}, Roi_StopX = {stopx}, Roi_StartY = {starty}, Roi_StopY = {stopy} WHERE SSH_Port = {port_num}"

        localSQL.sql_update(cnx, update_query)

        # NOTE: need to test what happens when port_num not found
        print(f"successfully updated roi's for node {port_num}")
        return True

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: camera_controls_uplink, Function: update_roi_settings func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)

    
# Working Function: JW 10/10/2023    
def modify_camera_settings(settings_data: json) -> json:
    """
        Function Description:
            - Called from anvil_uplink_router.modify_node_camera_settings
            - Modifies camera settings for camera node:
            Settings code:
            100 -> Update Color Balance
            200 -> Update Exposure & Gain
            300 -> Update ROI (Blob size) 

        Input Args:
            - settings_data (json(Dict)): Contains key-value pair of cam settings to update (key) with new value

        Output Args:
            - returned_dict (json(Dict)): Truthy value indicating if settings were successfully written to database
    
    """
    # Unpack json into settings_dict:
    settings_dict = json.loads(settings_data)

    # Determine which settings the user wants to modify
    settings_code = settings_dict['settings_code']
    port_num = settings_dict['port_num']

    returned_dict = {}

    # check Function Doc String for settings_code legend:
    if settings_code == 100:

        # Modify color balance camera settings
        color_balance = settings_dict['color_balance']

        # TODO: need to know how to put `custom color balance` setting into data-table

        # Write changes to database
        valid_colbal_update = update_node_color_balance(color_balance, port_num)

        # Use valid_colbal_update (T/F) to inform user if settings were successfully updated.
        returned_dict['color_bal_update'] = valid_colbal_update
        
        return json.dumps(returned_dict)

    elif settings_code == 200:

        # modify exposure and gain camera settings
        gain = settings_dict['gain']
        exposure = settings_dict['exposure']

        # Check if user entered a gain value (if they did not, don't update gain)
        if gain is not None:
            # Update camera gain:
            valid_gain_update = update_node_gain_settings(gain, port_num)

            # Keep track if gain updated correctly to inform user
            returned_dict['gain_update'] = valid_gain_update     


        # Check if user entered an exposure value (if they did not, don't update exposure)
        if exposure is not None:
            # Update camera exposure:
            valid_exposure_update = update_node_exposure_settings(exposure, port_num)

            # Keep track if gain updated correctly to inform user
            returned_dict['exposure_update'] = valid_exposure_update



        # Convert to json format
        return json.dumps(returned_dict)

    elif settings_code == 300:
        # Modify ROI (& blob size) camera settings
        
        min_blobsize = settings_dict['min_blobsize']
        roi_startx = settings_dict['roi_startx']
        roi_stopx = settings_dict['roi_stopx']
        roi_starty = settings_dict['roi_starty']
        roi_stopy = settings_dict['roi_stopy']

        # Update blobsize if user entered a value:
        if min_blobsize is not None:

            valid_blobsize_update = update_blobsize_settings(min_blobsize, port_num)

            returned_dict['blobsize_update'] = valid_blobsize_update


        # Check if a start value is provided to update settings:
        if roi_startx is not None:

            valid_roi_update = update_roi_settings(roi_startx, 
                                                   roi_stopx, 
                                                   roi_starty, 
                                                   roi_stopy, 
                                                   port_num)
            
            returned_dict['roi_update'] = valid_roi_update


        return json.dumps(returned_dict)
