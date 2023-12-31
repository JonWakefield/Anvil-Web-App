"""
    Author: Jon Wakefield
    Date: 10/12/2023
    Module Name: add_users.py

    Description: Adds users to database:
        - Add users to data table `users`.
        - Hashes password for increased security
        - Provides example for how to use program
        - use _get_user_password to check hash algorithm works correctly


    Names of gins, please match each:
        - Cherokee
        - Spade
        - UCG
        - WhiteOak

    Names of roles, please match each:
        - Admin
        - Coordinator
        - Geo-Coordinator
        - Manager
        - Technician
"""

import json

# Uplink importS:
try:
    import utils.mySQL_utils as localSQL
# Local host imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local host imports in add_users.py")
    from . import mySQL_utils as localSQL



def email_exists(email: str) -> bool:
    """ 
        Function Description:
            -Checks if a email is already stored in the database

        Input Args:
            - email (str): Email to check if alreaddy in table

        Output Args:
            - Bool: returns true if email is already in data table. False otherwise
            
    """
    try:
        cnx = localSQL.sql_connect()

        query = f"SELECT email FROM users WHERE email = '{email}';"

        result = localSQL.sql_select(cnx, query)

        if result:
            return True
        return False

    except (Exception) as sql_err:
        print(f"error in email_exists. \n{sql_err}")
        return False
    finally:
        localSQL.sql_closeConnection(cnx)



def add_user(name: str, email: str, password: str, role: str, gins_accessible: list):
    """ 
        Function Description:
            - Adds user to `users` table.

        Input Args:
            - name (str): name of user
            - email (str): Email to add for user
            - password (str): Unhashed password
            - role (str): role of users
            - gins_accessible (list): list of gin names user can access

        Output Args:
            - 
            
    """

    # First check if email is already in table (if it is, can't add user):
    if email_exists(email):
        print(f"email {email} already in table. Can't add user")
        return False
    
    # Hash the users password
    hashed_password = hash_password(password)

    # remove all whitespace in name
    username = name.replace(" ","")

    # Convert to json:
    gins_json = json.dumps(gins_accessible)

    try:
        # Connect to database
        cnx = localSQL.sql_connect()

        insert_user = f"INSERT INTO users (username, email, password_hash, active_gin, role, gins_accessible) VALUES ('{username}', '{email}', '{hashed_password}', '{gins_accessible[0]}', '{role}', '{gins_json}');"
        localSQL.sql_insert(cnx, insert_user)

    except (Exception) as err:
        print(f"unable to add user.\nError: {err}")
        return False
    finally:
        localSQL.sql_closeConnection(cnx)

    print(f"successfully added user {name}")

    return True


# Working Function JW 10/12/2023
def hash_password(password: str) -> str:
    """
        Function Description:
            - Called from user_management.change_user_password
            - Hashes the users password for increased protection
            - Uses XOR With key

        Input Args:
            - password (str): Unhashed password provided from user

        Output Args:
            - output (str): Hashed Password
            
    """
    """ XOR users password with cotton2023"""

    key = "cotton2023"
    output = ""

    # Repeat the key to match the length of the input string
    key_repeated = key * (len(password) // len(key)) + key[:len(password) % len(key)]


    # Perform XOR operation character by character
    for index, char in enumerate(password):
        result = ord(char) ^ ord(key_repeated[index])
        output += chr(result)


    return output




def _get_user_password(email: str) -> str:
    """ DEVELOPMENT FUNCTION NOT USED IN PRODUCTION
        Function Description:
            - Called from anvil_uplink_router._check_user_password
            - Checks that a users password is stored correctly 

        Input Args:
            - email (str): email for user

        Output Args:
            - password (str): Unhashed password returned to user
            
    """

    try:
        cnx = localSQL.sql_connect()

        select_query = f"SELECT password_hash FROM users WHERE email = '{email}'"

        result = localSQL.sql_select(cnx, select_query)[0]

    except (Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: user_management, Function: _get_user_password func. \nError: {err}"
        # Write error to error log:
        # write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    finally:
        localSQL.sql_closeConnection(cnx)

    print(f"hashed password for user {email} from data-table: {result[0]}")
    print(f"length of hashed password from data-table: {len(result[0])}")

    # Unhash password:
    password = hash_password(result[0])

    print(f"unhashed password: {password}")

    return password






if __name__ == "__main__":
    """
        Names of gins, please match each:
            - Cherokee
            - Spade
            - UCG
            - WhiteOak

        Names of roles, please match each:
            - Admin
            - Coordinator
            - Geo-Coordinator
            - Manager
            - Technician
    """

    # Example 2:
    ex_name = "Tim Manager"
    ex_email = "manager@email.com"
    ex_password = "Hello"
    ex_role = "Manager"
    ex_gins_accessible = ["Spade", "UCG"]

    add_user(ex_name, ex_email, ex_password, ex_role, ex_gins_accessible)


    # Example 3:
    ex_name = "Technician"
    ex_email = "tech@email.com"
    ex_password = "Hello"
    ex_role = "Technician"
    ex_gins_accessible = ["UCG"]

    add_user(ex_name, ex_email, ex_password, ex_role, ex_gins_accessible)

    # Example 4: long password
    ex_name = "Coord"
    ex_email = "cord@email.com"
    ex_password = "Hello1234$$$HelloWay123"
    ex_role = "Coordinator"
    ex_gins_accessible = ["Cherokee", "Spade", "UCG", "WhiteOak"]

    add_user(ex_name, ex_email, ex_password, ex_role, ex_gins_accessible)


    # Can check if the password was hashed correctly using _get_user_password

    # Example usage: Provide email for password to check (found in uplink_scripts.user_management.py)
    # Should print the correct unhashed password that was defined.
    # _get_user_password(email=ex_email)
    




# Not in use functions:
def create_username(first: str, last: str) -> str:
    """ Function not currently in use
        Designed for quick way to create username
    """
    return first + last

def username_exists(username: str) -> bool:
    """ Function not currently in use
        Function Description:
            - Checks if a username alrady exists, can not have two users with the same username in the database

        Input Args:
            -

        Output Args:
            -
            
    """
    """ Check if a username is already in the datatable"""
    try:
        cnx = localSQL.sql_connect()

        query = f"SELECT username FROM user_management WHERE username = '{username}';"

        result = localSQL.sql_select(cnx, query)

        # print(f"result is {result} of type {type(result)}")
        if result:
            return True
        return False

    except (Exception) as sql_err:
        print(f"error in username_exists. \n{sql_err}")
        return False
    finally:
        localSQL.sql_closeConnection(cnx)
