"""

Author: Jon Wakefield
Date: 10/12/2023
Module Name: user_management.py

Description:
    This Python module provides a set of functions for user authentication and management using a MySQL database. 
    It also handles JSON Web Tokens (JWTs) for user authentication. This module serves as a part of a user management system and includes the following functionalities:

1. User authentication and JWT token generation.
2. Password hashing and verification.
3. User and email existence checks in the database.
4. Logging user access requests and actions.
5. Retrieving user and gin information from the database.
6. Changing user passwords and active gins.
7. Authentication of users based on email and password.

This module is designed to be integrated into a larger application for user management and access control. It relies on a MySQL database and a predefined JWT secret key for secure user authentication.

"""
import email
import json
import jwt
from datetime import datetime, timedelta
from Globals import JWT_KEY
import re
import mysql.connector

#Uplink imports:
try:
    import utils.mySQL_utils as localSQL
    from utils.dateTime_utils import get_currentEpochTime_secs
    from utils.log_errors_utils import write_error_log, write_debug_log
    from utils.add_user_funcs import email_exists, add_user, hash_password
# Local server imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local server imports in user_management.py")
    from ..utils import mySQL_utils as localSQL
    from ..utils.log_errors_utils import write_error_log, write_debug_log
    from ..utils.dateTime_utils import get_currentEpochTime_secs
    from ..utils.add_user_funcs import email_exists, add_user, hash_password


# JWT_KEY = "cotton2023"

# Working Function JW 10/12/2023
def decode_jwt(token: str) -> dict:
    """
        Function Description:
            - Called from user_management.retrieve_user_info
            - Decodes provided JWT and returns the payload

        Input Args:
            - token (str): JSON WEB TOKEN, retrieved from users local storage (cookie)

        Output Args:
            - payload (dict): key-values retrieved from JWT
            - payload = {
                'user_id': # users email
                'exp_date: # expiration date of token
            }
    """

    try:
        # Decode the token using the secret key:
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # The token has expired
        # Time to expire: 
        print("The token has expired...")
        return None
    except jwt.InvalidTokenError as err:
        # The token is not valed or has been tampered with
        print("Invalid Token!")
        print(f"The error: {err}")
        return None


# Working Function JW 10/12/2023
def generate_jwt(user_id: str) -> str:
    """
        Function Description:
            - Called from user_management.authenticate_user
            - Generates a JWT for a user using their email.
            - This process takes place after the users login credentials have been verified.

        Input Args:
            - user_id (str): email assoaciated with users account, stored in the JWT payload.
              Allows for persistant login

        Output Args:
            - token (str): Generated JWT using users email and expiration date.
            
    """

    # Calculate an expiration time (length of time for which the token is valid):
    # Set it to be 5 years from time of token creation.
    expiration_time = datetime.utcnow() + timedelta(days=365 * 5)

    # Create a payload containing user information
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }

    print("About to encode:")

    # Generate the JWT with the payload and the secret key:
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')

    # If using PyJWT < 2.8, uncomment the line below:
    # token = token.decode('utf-8')

    return token


def log_access_request(json_data: json) -> bool:
    """
        Function Description:
            - Called from anvil_uplink_router.user_request_access
            - Logs user request to gain access to the website
            - No access is granted, but records & stores data.

        Input Args:
            - json_data (json(dict)): Users data to be stored in data table
            - json_data = json.dumps({
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'gin_name': gin_name,
                'requested_role': role
            }) 

        Output Args:
            - bool: Indicates if users data was successfully stored.
            
    """

    # Convert to python dict:
    python_dict = json.loads(json_data)

    # Upack dictionary
    firstname = python_dict.get("firstname")
    lastname = python_dict.get("lastname")
    email = python_dict.get("email")
    gin_name = python_dict.get("active_gin")
    requested_role = python_dict.get("requested_role")

    # Get the current time
    current_time = datetime.utcnow()

    try:
        # Connect to database
        cnx = localSQL.sql_connect()

        insert_query = f"INSERT INTO log_user_request_acc (firstname, lastname, email, active_gin, requested_role, time_requested) VALUES ('{firstname}', '{lastname}', '{email}', '{gin_name}', '{requested_role}', '{current_time}')"

        localSQL.sql_insert(cnx, insert_query)

    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: log_access_request func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)

        return False
    finally:
        localSQL.sql_closeConnection(cnx)

    print(f"successfully added {firstname} {lastname} to table")

    return True

def log_user_action(user_data: dict, action: str) -> bool:
    """
        Function Description:
            - Called from user_management.retrieve_user_info, user_management.change_user_password, user_management.change_gin
            - Records a users `action` to `users_log` datatable
            - Current things being logged: user log in, user log out, user password change, user gin change

        Input Args:
            - user_data (dict): dict storing users email, role, and current gin to be logged
            - action (str): Action describing what is being logged (i.e: 'login', 'logout')

        Output Args:
            - BOOL: indicates if successful loggin of user action
            
    """
    # Get current time indicating when user action happened.
    current_time = datetime.utcnow()
    # Unpack user_data dict
    email = user_data['email']
    role = user_data['role']
    gin_name = user_data['active_gin']

    try:
        cnx = localSQL.sql_connect()

        insert_query = f"INSERT INTO users_log (email, role, active_gin, type, time) VALUES ('{email}', '{role}', '{gin_name}', '{action}', '{current_time}')"

        localSQL.sql_insert(cnx, insert_query)

        print(f"logged {action} for {email}")
        return True
    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: log_user_action func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    
    finally:
        localSQL.sql_closeConnection(cnx)

def get_user_info_from_db(email: str) -> tuple:
    """
        Function Description:
            - Called from user_management.retrieve_user_info
            - Using the email retrieved from the users JWT, get other user info
                (username, active_gin, role, gins_accessible) from database

        Input Args:
            - email (str): Email retrieved from JWT's payload

        Output Args:
            - result (tuple): SQL select query's result
            - result = ('username','email','active_gin','role','gins_accessible')
            
    """

    try:
        # Connect to database
        cnx = localSQL.sql_connect()

        # Select data from `users` table:
        select_query = f"SELECT username, email, active_gin, role, gins_accessible FROM users WHERE email = '{email}';"

        result = localSQL.sql_select(cnx, select_query)[0]

    except(Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: get_user_info_from_db func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    
    finally:
        # Close connection
        localSQL.sql_closeConnection(cnx)

    return result

from typing import List
def get_gin_info_from_db(gins_accessible: List[str]) -> List[dict]:
    """
        Function Description:
            - Called from user_management.retrieve_user_info
            - Retrieve location of gins and number of gin stands for each gin the user has access to

        Input Args:
            - gins_accessible (list[str]): list storing names of gins the user can access.
            - Ex: ['UCG', 'Spade', 'Cherokee']

        Output Args:
            - List[dicts]: a List storing a dictionary at each index
            - list[0] = Dictionary storing key value pair of `key: gin_name`, `value: number_gin_stands`
            - list[1] = Dictionary storing key value pair of `key: gin_name`, `value: location_of_gin`
    """

    # Store key-value pair of: `gin_name`: 'location``
    gin_location_dict = {}

    # Store key-value pair of: `gin_name`: `num_gin_stands`
    num_gin_stands_dict = {}

    try:
        # Connect to database
        cnx = localSQL.sql_connect()

        for gin in gins_accessible:

            select_query = f"SELECT num_gin_stands, location FROM gins WHERE gin_name = '{gin}';"

            result = localSQL.sql_select(cnx, select_query)[0]

            num_stands = result[0]
            gin_location = result[1]

            # Add values to dicts:
            num_gin_stands_dict[gin] = num_stands
            gin_location_dict[gin] = gin_location

        # Return list storing dicts, for each gin
        return [num_gin_stands_dict, gin_location_dict]

    except(IndexError) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: get_gin_info_from_db func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    finally:
        localSQL.sql_closeConnection(cnx)




def retrieve_user_info(jwt: str) -> dict:
    """
        Function Description:
            - Called from anvil_uplink_router.check_user_login_status
            - Function is called after user's JWT has been found, retrieves info from datatable using JWT
            - Decodes the JWT which returns the `payload`. Payload stores users email and token expiration date
            - Once the token is decoded, the email is used to retrieve other user info from database (username, role, gins, etc.)

        Input Args:
            - JWT (str): JSON WEB TOKEN

        Output Args:
            - user_dict = {
                'username',
                'email',
                'active_gin',
                'role',
                'gins_accessible',
                'num_gin_stands',
                'gin_location'
            }
            
    """
    """use jwt to grab info on user"""

    # first decode the jwt to get the users payload:
    payload = decode_jwt(jwt)

    try:
        # unpack the payload:
        email = payload['user_id']
        exp_date = payload['exp']
    except (TypeError) as tErr:
        # decode_jwt returned Nonetype: (token is either expired or invalid)
        # User will have to resign in
        return None

    
    # use the retrieved email to get info on the user:
    retrieved_user_data = get_user_info_from_db(email)

    # retrieve gin info:
    username = retrieved_user_data[0]
    email = retrieved_user_data[1]
    active_gin = retrieved_user_data[2]
    users_role = retrieved_user_data[3]
    gins_accessible = json.loads(retrieved_user_data[4]) # store as list

    # Get gin info for each gin the user can access:
    gin_info = get_gin_info_from_db(gins_accessible)

    # unpack gin_info:
    num_gin_Stands = gin_info[0] # list
    gin_location = gin_info[1] # list

    # Pack everything up inside a dictionary:
    user_dict = {
        'username': username,
        'email': email,
        'active_gin': active_gin,
        'role': users_role,
        'gins_accessible': gins_accessible, 
        'num_gin_stands': num_gin_Stands,
        'gin_location': gin_location
    }
    
    # log user login attempt:
    returned_value = log_user_action(user_dict, 'login')

    return user_dict
        

def verify_old_password(cnx, email: str, cur_password: str) -> bool:
    """
        Function Description:
            - Called from user_management.change_user_password
            - Verifies that the old password provided by the user matches the password stored in the databse
            - Need to confirm user provided old password is correct.

        Input Args:
            - cnx: Database connection object
            - email (str): Email associated with current user
            - cur_password (str): user provided current password 

        Output Args:
            - bool: indicates if the provided current password matches the current stored password in database
            
    """
    """ Verify user provided password is == current stored password"""

    try:
        select_query = f"SELECT password_hash FROM users WHERE email = '{email}'"

        result = localSQL.sql_select(cnx, select_query)

        # Make sure we find a result
        if result:
            result = result[0]
            # Unhash stored password:
            password = hash_password(result[0])
            
            # Return boolean outcome:
            return cur_password == password

    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: verify_old_password func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    


def change_user_password(user_data: json) -> dict:
    """
        Function Description:
            - Called from anvil_uplink_router.change_user_password
            - Changes the password for a user

        Input Args:
            - user_data (json(dict)): stores user info,
            - user_data = json.dumps({
                'username': self.username,
                'email': self.email,
                'role': self.role,
                'active_gin': self.gin_name,
                'cur_password': cur_password,
                'new_password': new_password
            })

        Output Args:
            - returned_data (dict): indicates if successful password change (T/F)
            
    """
    # Convert json to python dict
    user_data = json.loads(user_data)

    # Unpack python dict
    email = user_data['email']
    cur_password = user_data['cur_password']
    new_password = user_data['new_password']

    try:
        cnx = localSQL.sql_connect()

        # verify the old password first:
        if not verify_old_password(cnx, email, cur_password):
            print("Password change failed. Incorrect old password")
            returned_data = {
                'changed_password': False,
                'error_code': 1 # Error Code 1 -> incorrect old password
            }
            return returned_data

        # Hash the new password:
        new_hashed_password = hash_password(new_password)

        #Update the users password in the database:
        update_query = f"UPDATE users SET password_hash = '{new_hashed_password}' WHERE email = '{email}'"

        localSQL.sql_update(cnx, update_query)

        # log user password change:
        returned_bool = log_user_action(user_data, 'password-change')

        # Return successful password change
        returned_data = {
            'changed_password': True
        }

        return returned_data
        
    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: change_user_password func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)

        returned_data = {
                'changed_password': False,
                'error_code': 2 # Error Code 2 -> unable to update user password in database
        }

    finally:
        localSQL.sql_closeConnection(cnx)


def change_gin(user_data: json) -> bool:
    """
        Function Description:
            - Called from anvil_uplink_router.change_gin_access
            - Changes the users current active gin

        Input Args:
            - user_data (json(dict)): dictionary storing user info 
            - user_data = json.dumps({
                'username': self.username,
                'email': self.email,
                'role': self.role,
                'active_gin': new_gin
            })

        Output Args:
            - bool: indicates if successful gin change operation.
            
    """
    """Change which gin user current has access to view data for"""

    # Convert to python dict
    user_data = json.loads(user_data)

    # unpack dict:
    email = user_data['email']
    gin_name = user_data['active_gin']
  

    # 1. change 'users' data-table WHERE email
    try:
        cnx = localSQL.sql_connect()

        update_query = f"UPDATE users SET active_gin = '{gin_name}' WHERE email = '{email}'"

        localSQL.sql_update(cnx, update_query)

    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: change_gin func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)

    # 2. log change
    returned_bool = log_user_action(user_data, 'Gin-Change')

    return True

def verify_password(stored_password: str, password: str) -> bool:
    """
        Function Description:
            - Called from user_management.authenticate_user
            - Checks if the password stored in database matches user entered password on login attempt

        Input Args:
            - stored_password (str): Password stored in database for a specific user account
            - password (str): User entered password for login attempt

        Output Args:
            - bool: indicates (T/F) if stored_password matches user entered password
            
    """
    # Unhash the stored password
    unhashed_stored_password = hash_password(stored_password)

    return unhashed_stored_password == password


def is_valid_email(email: str) -> bool:
    """
        Function Description:
            - Called from user_management.authenticate_user
            - Determine if the user entered email is valid
            - An invalid email is an email that does not include a `@` symbol or uses unapproved characters in the case of an
                attempt to perform SQL injection.
            - More detailed description about whats going on in this function can be found here:
                https://developers.google.com/edu/python/regular-expressions

        Input Args:
            - email (str): argument being checked if valid or not

        Output Args:
            - bool: Indicates if valid email (T -> yes, valid)
    
    """
    # Define a regular expression pattern for a valid email address:
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+'

    # Use the re module to match the input against the pattern:
    if re.match(email_pattern, email):
        print(f"{email} is valid!")
        return True
    else:
        print(f"{email} is not valid!")
        return False



def authenticate_user(user_creds: json) -> dict:
    """
        Function Description:
            - Called from anvil_uplink_router.user_login
            - Checks if user provided login credientials (user_creds) are valid
            - If successfull will create a JWT for user and log them in.
            - If invalid will inform user password or username is incorrect

        Input Args:
            - user_creds (json(dict)): stores user entered `email`, `password

        Output Args:
            - If successful login: returns dict with created JWT
            - if unsuccessful login: Bool value of False -> informs user credientials could not be verified
            
    """

    # Unpack json
    user_creds_dict = json.loads(user_creds)

    # Get user entered login credentials:
    email = user_creds_dict.get("email")
    password = user_creds_dict.get("password")

    # Check for valid email & SQL injection
    # if not is_valid_email(email):
    #     return False

    try:

        cnx = localSQL.sql_connect()

        # Use escape input to prevent sql injections:
        # escaped_input = cnx.converter.escape(email)

        select_query = f"SELECT email, password_hash FROM users WHERE email = '{email}'"

        result = localSQL.sql_select(cnx, select_query)

        # If there an email in database that matches user entered email, enter:
        if result:
            
            result = result[0]
            # Verify the password:
            stored_password = result[1]

            if verify_password(stored_password, password):
                print(f"User {email} Authenticated successfully")
                # log this

                # Generate a JWT token for the user:
                token = generate_jwt(user_id=email)

                # Package up return data
                returned_data = {
                    'created_user': True,
                    'token': token
                }
                return returned_data
            
            else:
                print("Authentication failed. Incorrect password.")
                return False
            
        else:
            print("Authentication Failed. User not found")
            return False
        
    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: authenticate_user func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        # Close connection:
        localSQL.sql_closeConnection(cnx)



def add_user_to_db(new_user_info: json) -> bool:
    """
        Function Description:
            -

        Input Args:
            - 

        Output Args:
            - 
    
    """
    # Convert json to python dict
    new_user_info_dict = json.loads(new_user_info)

    # Unpack dictionary:
    name = new_user_info_dict['name']
    email = new_user_info_dict['email']
    password = new_user_info_dict['password']
    role = new_user_info_dict['role']
    gins_accessible = new_user_info_dict['gins_accessible']

    # Add user to table:
    user_added_bool = add_user(name,
                                email,
                                password,
                                role,
                                gins_accessible)
    
    return user_added_bool
    

def remove_user_from_db(user_info: json) -> bool:
    """
        Function Description:
            -

        Input Args:
            - 

        Output Args:
            - 
    
    """

    email_dict = json.loads(user_info)

    # Un pack dictionary
    user_email = email_dict['user_email']
    remove_email = email_dict['remove_email']

    # Cant remove email of currently logged in user:
    if user_email == remove_email:
        return False

    try:

        cnx = localSQL.sql_connect()

        # Setup delete query:
        delete_query = f"DELETE FROM users WHERE email = '{remove_email}'"

        localSQL.sql_insert(cnx, delete_query)
                    
    except (Exception) as sql_err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: remove_user_from_db func. \nError: {sql_err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        # Close connection:
        localSQL.sql_closeConnection(cnx)


    return True

