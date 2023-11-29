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
    from utils import mySQL_utils as localSQL
    from utils.add_user_funcs import hash_password, _get_user_password, email_exists, add_user

# Local host imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local host imports in add_users.py")
    from .utils.add_user_funcs import hash_password, _get_user_password, email_exists, add_user
    from .utils import mySQL_utils as localSQL



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

    # Add Admin user:
    name = "Admin"
    email = "Admin"
    password = "Hello" # Provide unhashed password
    role = "Admin"
    gins_accessible = ["Cherokee", "Spade", "UCG", "WhiteOak"]

    add_user(name, email, password, role, gins_accessible)

