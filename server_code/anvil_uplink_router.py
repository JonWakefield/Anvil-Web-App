"""
Anvil Uplink Router Module
Author: JW
Date: 07/26/2023
Module Name: graphs_uplink.py

Git clone link:
git clone ssh://raspberrypijon.tx%40gmail.com@anvil.works:2222/HAYJOOPAQQ6KMFOF.git Pides_VIEWER

Anvil Dependencies:
HashRouting: ZKNOF5FRVLPVF4BI
anvil_extras: C6ZZPAPN4YYF5NVJ

Description:
This Python module, "anvil_uplink_router.py," acts as a central router for various functions within an Anvil web application. 
It facilitates communication between different components of the application, including camera controls, picture capture, visualization monitoring, user management, 
trend graphs, and node connections. The module defines callable functions and custom type hints to streamline interactions with the Anvil platform.

Key Sections and Functions:

1. Camera Controls Uplink Functions:
   - `connect_to_node(node_data: json) -> dict`: Connects to a node for camera control.
   - `modify_node_camera_settings(cam_settings_data: json)`: Modifies camera settings for a connected node.

2. Picture Capture Control Form Uplink Functions:
   - `open_file_explorer() -> str`: Opens a file explorer for selecting source/destination directories.
   - `classify_images_simulate(image_full_path, img_name_list, job_id)`: Initiates image classification.
   - `start_classifier_build(json_data) -> str`: Starts building a classifier using provided data.
   - `check_classifier_progress(json_data) -> Tuple`: Checks the progress of the image classifier.
   - `submit_labels_to_db(json_data)`: Retrieves, labels, and stores images.

3. Visualization Monitor Form Uplink Functions:
   - `get_plastic_image(json_data) -> dict`: Retrieves plastic images for monitoring.
   - `get_image_ages(json_data: str) -> dict`: Retrieves image ages for monitoring.
   - `_simulate_events(gin_name)`: Simulates events for monitoring.

4. User Management Uplink Functions:
   - `add_to_cookie(value: str, key: str)`: Adds a key-value pair to the user's cookies.
   - `remove_from_cookie(key: str) -> bool`: Removes a key from the user's cookies.
   - `get_cookie_value(key: str) -> str`: Retrieves a value from the user's cookies.
   - `user_request_access(json_data: dict) -> bool`: Logs a user's access request.
   - `check_user_login_status() -> dict or None`: Checks if a user is logged in.
   - `user_login(user_creds: dict) -> bool or dict`: Authenticates and logs in a user.
   - `user_log_out(user_data: dict) -> bool`: Logs out a user.
   - `change_gin_access(user_data: dict) -> bool`: Changes a user's access to a gin.
   - `change_user_password(user_data: dict) -> bool`: Changes a user's password.

5. Trend Graphs Uplink Functions:
   - `update_chart_settings(chart_settings: json) -> bool`: Updates chart settings.
   - `retrieve_chart(user_data: json) -> AnvilMedia`: Retrieves a chart.
   - `generate_pdf() -> PdfRenderer`: Generates a PDF from a form.

6. Nodes Connected Uplink Functions:
   - `check_if_all_gins_accessible(gins_accessible: json) -> bool`: Checks if a user has access to view all gins.
   - `check_nodes_connected(gin_query: str) -> json`: Checks connected nodes.
   - `check_for_node_entry(port_num)`: Checks for a node entry.
   - `add_node_connection(node_params: str) -> bool`: Adds a node connection.
   - `update_node_connection(node_params: str) -> bool`: Updates a node connection.
   - `remove_node_connection(node_params: str) -> bool`: Removes a node connection.

This module enhances code organization and readability, making it easier to manage complex interactions in the Anvil web application.
"""


import json
import anvil.server
import anvil.media
from time import sleep
from Globals import AnvilMedia
import anvil.pdf
from typing import List, Tuple, Dict

#Uplink imports:
try:
    from uplink_scripts import picture_capture_controls_uplink
    from uplink_scripts import camera_controls_uplink
    from uplink_scripts import gin_monitor_uplink
    from uplink_scripts import user_management
    from uplink_scripts import graphs_uplink
    from uplink_scripts import nodes_connected_uplink

# Local host imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local host imports in anvil_uplink_router.py")
    from .uplink_scripts import picture_capture_controls_uplink
    from .uplink_scripts import camera_controls_uplink
    from .uplink_scripts import gin_monitor_uplink
    from .uplink_scripts import user_management
    from .uplink_scripts import graphs_uplink
    from .uplink_scripts import nodes_connected_uplink




# ******** START camera controls UPLINK functions *********** #


# Working Function: JW 10/10/2023
@anvil.server.callable
def connect_to_node(node_data: json) -> json:
    """
        Function Description:
            - Called from FormCamControls (client), connects to camera node (port #)
            - Returns camera settings for camera node

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
    # Call connect_to_node to connect to a node and retrieve node info & camera settings
    returned_data = camera_controls_uplink.connect_to_node(node_data)
 
    return returned_data


# Working Function JW 10/10/2023
@anvil.server.callable
def modify_node_camera_settings(cam_settings_data: json) -> json:
    """
        Function Description:
            - Called from FormCamControls (client), updates a nodes camera settings
            - User must already be connected to a node first
            - Returns 

        Input Args:
            - cam_settings_data = json.dumps({
                'email': self.email,
                'port_num': self.port_num,
                'gin_name': self.node_gin_name,
                'gin_stand_num': self.node_gin_stand_num,
                'settings_code': 300,
                ADDITIONAL CAMERA SETTINGS ARGS BASED ON settings_code #:
                ...
            })
            Settings code:
            100 -> Update Color Balance
            200 -> Update Exposure & Gain
            300 -> Update ROI (Blob size) 

        Output Args:
            - returned_data
    
    """
    # Call modify_camera_settings to update nodes camera settings in database:
    returned_data = camera_controls_uplink.modify_camera_settings(cam_settings_data)

    return returned_data

# ********* END camera controls UPLINK FUNCTIONS *************#



# *************** START PICTURE CAPTURE CONTROL FORM UPLINK FUNCTIONS *********** #

# Tested & Working, JW 07-25-2023
@anvil.server.callable
def open_file_explorer():
    """
        Opens a file explorer navigator for the user to select the source and / or destination directory.

        Returns str(file_path)
        *Depending on when function is called, file_path could be either the source or destination dir.
    """
    file_path = picture_capture_controls_uplink.open_file_explorer()

    return file_path

# Tested & Working, JW 07-25-2023
@anvil.server.callable
def classify_images_simulate(image_full_path, img_name_list, job_id):
    """ Uplink router func to classify_images_simulate function in pictureCapControls_uplink.py
    """

    picture_capture_controls_uplink.classify_images_simulate(image_full_path, img_name_list, job_id)



# Tested & Working, JW 07-25-2023
@anvil.server.callable
def start_classifier_build(json_data):
    """
        json_data: {image_path, num_images}
    """

    job_id = picture_capture_controls_uplink.start_classifier_build(json_data)

    return job_id


# Tested & Working, JW 07-25-2023
@anvil.server.callable
def check_classifier_progress(json_data):
    """
        This function will be called every n seconds once timer reaches 0...
        1. Every n seconds go out and check database to see how many images / n are ready
            1a. if > n images are done, return % finished and update progress bar.
            1b. if n images are done retrieve labels, set flag HIGH indiciating we are ready to display the images to the user

    """

    returned_list = picture_capture_controls_uplink.check_classifier_progress(json_data)

    return returned_list[0], returned_list[1], returned_list[2], returned_list[3], returned_list[4]

    


# Tested & Working, JW 07-25-2023
@anvil.server.callable
def submit_labels_to_db(json_data):
    """ 
        Retrieves images from src directory, runs through classifier, adds images to users stack, and returns images and labels.

        Function Outline:
        1. Unpack JSON data
        2. Determine if retreiving previously used images, or grabing new images from directory.
            Using a Try / Except statement, that returns a IndexError if the index (page_num) is not valid (aka grab new images then)
        3. Access the source directory (file_path) and randomly selected num_images_to_get from directory.
        4. Convert each image to type Anvil.BlobMedia so that we can display them in a Canvas component.
            4a. TEMPORARY: assign image a "dummy" label of either HID or Cotton
            4b. TODO: ADD in classifers to replace "dummy" labels
        5. Check if user already has a stack made for them, if not create one using user_id
            5a. Add images to already made or newly created user stack
        6. Check if MAX_STACK_HEIGHT has been exceeded, if so remove first entry from stack.
        6. Return the images (img_list), img_labels (img_label_dict), img names (img_name_list), and update_database BOOLEAN indicator 
    """
    picture_capture_controls_uplink.submit_labels_to_db(json_data)
    return

# *************** END PICTURE CAPTURE CONTROL FORM UPLINK FUNCTIONS *********** #


# *************** START VISN MONITOR FORM UPLINK FUNCTIONS *********** #


# Tested & Working, JW 09-15-2023
@anvil.server.callable
def get_image_ages(json_data: json) -> json: 
    """
        Function Description:
            - Called from FormGinMonitoring (client)
            - Retrieves the most recent image ages for a gin  

        Input Args:
            - json_data = json.dumps({
                'gin_name': self.gin_name,
                'num_gin_stands': self.num_gin_stands
            })

        Output Args:
            - returned_dict (json(dict)): ({
                "img_time_taken": img_time_list, # list of times when plastic event occured (1 index for each gin stand num)
                "file_paths": file_path_list, # file path to retrieve each image (1 index for each gin stand num)
                "image_ages": age_list, # List of time since plastic event occured (1 index for each gin stand num)
                "HID_status": HID_status_list # list indicating if HIE was active (1 index for each gin stand num)
            })
    """

    # Call function and retrieve image ages for each gin stand
    returned_dict = gin_monitor_uplink.get_image_ages(json_data)

    return returned_dict

# Tested & Working, JW 10/11/2023
@anvil.server.callable
def get_plastic_image(json_data: json) -> dict:
    """
        Function Description:
            - Called from FormGinMonitoring (client)
            - Retrieves plastic image for a gin stand num 

        Input Args:
            - json_data = json.dumps({
                    'file_path': file_path_for_gin_stand_number_i,
                    'image_size': self.imageSize, # size of image (Varies based on users screen size)
                })

        Output Args:
            - Returns image of type anvil_blob_media
            - returned_img = {
                "image": anvil_image, 
            }
    """

    # Retrieve plastic image 
    returned_img = gin_monitor_uplink.get_plastic_image(json_data)

    return returned_img

# Tested & Working, JW 10/11/2023 (dev. function)
@anvil.server.callable
def _simulate_events(gin_name: str):
    """ DEVELOPMENT FUNCTION, NOT FOR PRODUCTION.

        Function Description:
            - simulates plastic events being adding to data-table

        Input Args:
            - Name of gin to simulate events for

        Output Args:
            - None

    """
    gin_monitor_uplink._simulate_events(gin_name)

    return

# *************** END VISN MONITOR FORM UPLINK FUNCTIONS *********** #



# *************** START USER MANAGEMENT UPLINK FUNCTIONS *********** #



# Working Function JW 10/10/2023
@anvil.server.callable
def add_to_cookie(value: str, key: str):
    """
        Function Description:
            - Called From anvil_uplink_router.user_login
            - Add (Store) value to cookie
            - 10/11/2023: Only cookie being added is JWT for persistant login

        Input Args:
            - value (str): value being stored (Added) to the cookie
            - key (str): key associated with the value being added (think python dicts)

        Output Args:
            - 

    """

    # Store a key, value pair in the users cookie (default expiration is 30 days):
    anvil.server.cookies.local[key] = value

    # Log addition of cookie
    print(f"Added value {value} to key {key}...")


# Working Function JW 10/10/2023
@anvil.server.callable
def remove_from_cookie(key: str) -> bool:
    """
        Function Description:
            - Called From anvil_uplink_router.check_user_login_status, anvil_uplink_router.user_login, anvil_uplink_router.user_log_out
            - Removes key-value pair stored in cookie

        Input Args:
            - key (str): key used to retrieve and delete cookie

        Output Args:
            - BOOL: Indicates if successful deletion of key-value pair
            
    """
    
    try:
        # Delete `value` associated `key`
        del anvil.server.cookies.local[key]

        print(f"deleted value for key {key}")

        return True
    except (Exception) as err:
        print(f"Unable to delete {key} from cookie.\n{err}")
        return False


# Working Function JW 10/10/2023
@anvil.server.callable
def get_cookie_value(key: str) -> str:
    """
        Function Description:
            - Called from anvil_uplink_router.check_user_login_status and anvil_uplink_router.user_login
            - Retrieves the value stored in a cookie using a `key`
            - Used to determine if a JWT is stored in the users local storage (persistant login)

        Input Args:
            - key (str): Used to retrieve `value` in cookie

        Output Args:
            - retrieved_value (str): retrieved `value` linked to `key`.
            
    """

    # Retrieve cookie's value from `key`
    retrieved_value = anvil.server.cookies.local.get(key, None)

    print(type(retrieved_value))
    print(retrieved_value)

    return retrieved_value


# Working Function JW 10/10/2023
@anvil.server.callable
def user_request_access(json_data: json) -> bool:
    """
        Function Description:
            - Called From RequestAccessModal (client)
            - User can fill out a form to request access to website
            - Users data is stored, but does not grant them access to the website.
            - Setup to allow for easy retrieve / access to users that want data while also recording potential visiters.

        Input Args:
            - json_data (json(dict)): Stores "user" entered info
            - json_data = json.dumps({
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'gin_name': gin_name,
                'requested_role': role
            })

        Output Args:
            - returned_bool (bool): Indicates if users data was successfully stored in a data-table
            
    """

    # Store & log users request to gain access to the website
    returned_bool = user_management.log_access_request(json_data)

    return returned_bool


# Working Function JW 10/10/2023
@anvil.server.callable
def check_user_login_status():
    """
        Function Description:
            - Called from MainModule (Client) on initial loading of web-app
            - Determines if a user is logged in by checking if a JWT is stored in users cookie.
            - If user is signed -> retrieve user info (email, active_gin, gins accessible, role)
            - If a user is not signed in, return None and redirect user to landing page where they
                can login or request access.

        Input Args:
            - None

        Output Args:
            - If user is not signed in (no cookie found) -> return None
            - Is a user is logged in (cookie found) -> return retrieved_user_data (dict)
            - retrieved_user_data (dict) = {
                'username': users_username,
                'email': users_email,
                'active_gin': users_current_gin,
                'role': users_role,
                'gins_accessible': users_gins_accessible, 
                'num_gin_stands': active_gins_num_gin_stands,
                'gin_location': location_of_gin (state)
            }
    """
    # Check & See if user has a token (JWT) in their cookie jar:
    retrieved_value = get_cookie_value("access-token")

    # If a JWT is not found -> return & prompt user to login
    if retrieved_value is None:
        return None
    
    print("jwt found.. getting info...")

    # If token is found, use the token to grab the users info from data-table `users`
    retrieved_user_data = user_management.retrieve_user_info(retrieved_value)

    # If token is exp or invalid, remove it from cookie jar:
    if retrieved_user_data is None:
        # del token
        print("Deleting invalid token...")
        remove_from_cookie('access-token')
        # return none, enforcing user to re-login
        return None

    # Return user_data, redirecting user to their home page
    return retrieved_user_data


# Working Function JW 10/10/2023
@anvil.server.callable
def user_login(user_creds: json) -> bool:
    """
        Function Description:
            - Called from SignInModal (Client)
            - Called when user wants to sign into their account, checks if user provided credidentials are valid

        Input Args:
            - user_creds (json(dict)): Json dict storing user login credientials: `email`, `password`

        Output Args:
            - bool: Indicates if successful login (aka user provided email and password are valid), 
            - returns false if provided user_creds are not valid
            
    """

    retrieved_value = user_management.authenticate_user(user_creds)

    # chec if type dict (aka user logged in successfully, else wont be type dict):
    if(isinstance(retrieved_value, dict)):
        created_user = retrieved_value['created_user']
        token = retrieved_value['token']

        # Remove a cookie just to be safe:
        remove_from_cookie('access-token')

        # Check cookie value:
        get_cookie_value("access-token")

        # Add new token to users cookie jar:
        add_to_cookie(token, 'access-token')
        
        # Add a delay here: (fixes cookie not getting stored in users browser bug)
        sleep(4)

        return created_user
    else:
        return retrieved_value


# Working Function JW 10/10/2023
@anvil.server.callable
def _check_user_password(email: str) -> bool:
    """ DEVELOPMENT FUNCTION NOT USED IN PRODUCTION
        Function Description:
            - Called be called from anywhere.
            - Used to verify password changes were working correctly
            - To use, create a button on any anvil form, call this function with an email argument.
            - returned value from function will be unhashed users password

        Input Args:
            - email (str): users email 

        Output Args:
            - retrieved_password (str): Password stored for `email`
              (Will be False if email is not found in database)
    """
    """ Developer function to check user password"""

    # Call function to get password from database
    retrieved_password = user_management._get_user_password(email)

    # Return password
    return retrieved_password


# Working Function JW 10/10/2023
@anvil.server.callable
def user_log_out(user_data: dict) -> bool:
    """
        Function Description:
            - Called from FormSettings (client)
            - Logs user out by deleting stored JWT in clients local storage

        Input Args:
            - user_data (dict): Contains user data to log users logout action

        Output Args:
            - bool: Indicates if successful logout attempt.
            
    """

    # Remove token from users cookie jar
    returned_bool = remove_from_cookie('access-token')

    # log user logout
    log_bool = user_management.log_user_action(user_data, 'logout')

    # Add a delay here: (seems to fix cookie not getting stored in users browser bug)
    sleep(4)

    return returned_bool


# Working Function JW 10/10/2023
@anvil.server.callable
def change_gin_access(user_data: json) -> bool:
    """
        Function Description:
            - Called from FormSettings (client)
            - Changes the users current active gin,
            - This is needed for forms like gin monitor where only one gin can be monitored at a time

        Input Args:
            - user_data (json(dict)): Dict storing users data.
            - user_data = json.dumps({
                'username': self.username,
                'email': self.email,
                'role': self.role,
                'active_gin': new_gin
            })

        Output Args:
            - returned_bool (bool): indicates if successfull gin change (T/F)
            
    """
    """ Change which gin user has access too"""

    returned_bool = user_management.change_gin(user_data)

    return returned_bool


# Working Function JW 10/10/2023
@anvil.server.callable
def change_user_password(user_data: json) -> dict:
    """
        Function Description:
            - Called from FormSettings (client)

        Input Args:
            - user_data (json(dict)): user info need for changing password and loggin password change
            - user_data = json.dumps({
                'username': self.username,
                'email': self.email,
                'role': self.role,
                'active_gin': self.gin_name,
                'cur_password': cur_password,
                'new_password': new_password
            })

        Output Args:
            - returned_dict (dict): indicates if password change was successful
            - If unsuccessful password change, provides error code for reason it was unsuccesful
            
    """
    # Call change_user_password to change password stored in database
    returned_dict = user_management.change_user_password(user_data)

    return returned_dict



# *************** END user management FORM UPLINK FUNCTIONS *********** #


# *************** START TREND GRAPHS UPLINK FUNCTIONS *********** #


# Working Function JW 10/15/2023
@anvil.server.callable
def update_chart_settings(chart_settings: json) -> bool:
    """
        Function Description:
            - Called from FormGraphSetup (client) on button click.
            - Updates the chart settings stored for the user.

        Input Args:
            - chart_settings (json(dict)): Stores chart settings 
            - chart_settings = json.dumps({
                'email': self.email,
                'gin_name': gin_name, # Selected gin name from drop down
                'num_gin_stands': num_gin_stands, # num of gin stands from gin_name
                'graph-type': graph_type, # type of graph: ( 1 day, 7day, 30 day, season total)
                'graph-scale': graph_scale # Auto-scale, 100 bales, etc.
            })

        Output Args:
            - BOOL: Indicates if successful update of users chart settings (T/F)
    """

    # CAll update_chart_settings to store new settings.
    retrieved_bool = graphs_uplink.update_chart_settings(chart_settings)

    return retrieved_bool

# Working Function JW 10/15/2023
@anvil.server.callable
def retrieve_chart(user_data: json) -> AnvilMedia:
    """
        Function Description:
            - Called from FormTrendGraphs (client), retrieves matplotlib chart
            - Uses the currently stored chart settings for user, and retrieves a chart
            - Chart is of type AnvilMedia for easy displaying on client side
            
        Input Args:
            - user_data (json(dict)):  user data for selecting correct row in data-table
            - user_data = json.dumps({
                'email': self.email,
                'gin_name': self.gin_name,
                'num_gin_stands': self.active_num_gin_stands,
            })

        Output Args:
            - retrieved_chart (AnvilMedia): Retrieved matplotlib chart of type AnvilMedia (aka an Image)
    """
    
    # Use user_data to create and retrieve chart:
    retrieved_chart = graphs_uplink.retrieve_chart(user_data)

    return retrieved_chart


# Not Working: JW 10/15/2023
@anvil.server.callable
def generate_pdf():
    """ Non-Working function

        - Function Description:
            - Would be called from FormTrendGraphs (client)
            - Generates a PDF of the currently opened form.
    """
    pdf = anvil.pdf.render_form('FormTrendGraphs', route=False)
    # pdf = PdfRenderer(page_size='A4').render_form('FormTrendGraphs',route=False)

    return pdf

# -----------------END trend GRAPHS UPLINK FUNCTIONS ---------------------- #


# *************** START NODES Connected UPLINK FUNCTIONS *********** #

# Tested & Working, JW 09-18-2023
@anvil.server.callable
def check_if_all_gins_accessible(gins_accessible: json) -> bool:
    """
        Function Description:
            - Called from FormNodeConns, in __innit__ method
            - Checks if the user has access to all gins
            - If they have access to all gins display the additional `all gins` and `unassigned`  options for Node Connections

        Input Args:
            - gins_accessible (json(list)): list of all gins the user has access to view.

        Output Args:
            - BOOL: Indicates if user has access to all gins (T/F)
    """

    # Check database:
    returned_bool = nodes_connected_uplink.check_if_all_gins_accessible(gins_accessible)

    return returned_bool

# Tested & Working, JW 09-18-2023
@anvil.server.callable
def check_nodes_connected(gin_query: str) -> json:
    """
        Function Description:
            - Called from FormNodeConns (client), called in __init__ method and when timer reaches tick amount
            - Checks which nodes are connected and retrieves information on the nodes for displaying.

        Input Args:
            - gin_query (str): name of gin to search for connected nodes on

        Output Args:
            - retrieved_data (json(List(Dict))): List of dictionaries where each index in the list is a nodes info for gin `gin_query`
    """
    # Call check_nodes_connected to get list of nodes connected to a gin
    retrieved_data = nodes_connected_uplink.check_nodes_connected(gin_query)

    return retrieved_data

# Tested & Working, JW 09-18-2023
@anvil.server.callable
def check_for_node_entry(port_num: int) -> dict:
    """
        Function Description:
            - Called from FormNodesConns (client), in add_node_button_click
            - Checks to see if user entered node number exists in database
            - If node exists -> ask user if they want to overwrite already stored node data

        Input Args:
            - port_num (int): int of port number to check if exists

        Output Args:
            - retrieved_node_info (dict): Info of `port_num` node
    """

    # Check if `port_num` exists in database:
    retrieved_node_info = nodes_connected_uplink.check_for_port_entry(port_num)

    return retrieved_node_info

# Tested & Working, JW 09-18-2023
@anvil.server.callable
def add_node_connection(node_params: json) -> bool:
    """
        Function Description:
            - Called from FormNodesConns (client), in add_node_button_click
            - Addes node info to database using user entered info.

        Input Args:
            - node_params (json(dict)): node parameters being written to database
            - node_params = json.dumps({
                'gin_stand': self.gin_name_drop_down.selected_value,
                'gin_stand_num': self.gin_stand_drop_down.selected_value,
                'port_num': port_num,
            })

        Output Args:
            - returned_bool (bool): Indicates if successfully added results to datatable


    """
    # Write node_params to table
    returned_bool = nodes_connected_uplink.add_node(node_params)

    return returned_bool

# Tested & Working, JW 09-18-2023
@anvil.server.callable
def update_node_connection(node_params: json) -> bool:
    """
        Function Description:
            - Called from FormNodeConns (client), in add_node_button_click
            - Updates a camera nodes settings in the database (gin name, gin stand num, position)

        Input Args:
            - node_params (json(dict)): parameters to update in database
            - node_params = json.dumps({
              'gin_stand': self.gin_name_drop_down.selected_value,
              'gin_stand_num': self.gin_stand_drop_down.selected_value,
              'port_num': port_num,
            })

        Output Args:
            - returned_bool (bool): Indicates if successful update of parameters in database
    """
    # Use node_params to update node info in database 
    returned_bool = nodes_connected_uplink.update_node(node_params)

    return returned_bool
    
# Tested & Working, JW 09-18-2023
@anvil.server.callable
def remove_node_connection(node_params: json) -> bool:
    """
        Function Description:
            - Called from FormNodeConns (client), delete_port_num
            - Removes a port number from the table `CamNodes_Info`

        Input Args:
            - node_params (json(dict)): Node parameters
            - node_params = json.dumps({
                'port_num': row_content[0].text,
                'gin_name': row_content[1].text,
                'gin_stand_num': row_content[2].text,
            })

        Output Args:
            - returned_bool (bool): Indicates if succesfully removed info on node from table
    """
    # Call remove_node to remove node from table:
    returned_bool = nodes_connected_uplink.remove_node(node_params)

    return returned_bool

# *************** END nodes connected UPLINK FUNCTIONS *********** #


if __name__ == '__main__':

    #Connect to our Anvil WebApp
    anvil.server.connect("server_6QGH5ZF3VP27AI3BRVEFJNMN-HAYJOOPAQQ6KMFOF")
    

    #Continously loop through, waiting for uplink call
    try:
        anvil.server.wait_forever()
    except KeyboardInterrupt:
        pass


