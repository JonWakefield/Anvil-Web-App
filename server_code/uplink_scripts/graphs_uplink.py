"""
Author: JW
Date: 07/26/2023
Module Name: graphs_uplink.py

Description:
    This Python module serves as an interface for generating and managing user-specific trend graphs. 
    It provides functions for converting data between Pandas DataFrames and JSON, updating user preferences for graph settings in a database, 
    retrieving user-specific chart settings, and generating bar charts.

Functions:
- df2serialized(df: pd.DataFrame) -> json:
  Converts a Pandas DataFrame to a serialized JSON format suitable for HTTP requests.

- serialized2df(data: json) -> pd.DataFrame:
  Converts serialized JSON data into an unserialized Pandas DataFrame.

- update_database(chart_settings: dict) -> bool:
  Updates user-specific chart settings in a database based on the provided dictionary.

- create_user_chart_settings_entry(cnx, email: str, gin_name: str, num_gin_stands: int, chart_type="Event Cluster", chart_scale="Auto-Scale", retrieve_settings=False) -> bool or dict:
  Creates a new entry or updates existing user chart settings in the database. Optionally retrieves and returns chart settings.

- update_chart_settings(chart_settings: str) -> bool:
  Updates user chart settings based on a JSON-formatted input.

- retrieve_chart(user_data: json) -> anvil Media:
  Retrieves and generates a bar chart based on user-specific data and chart settings.

- get_user_chart_settings(user_email: str) -> tuple or bool:
  Retrieves user-specific chart settings from the database and returns them as a tuple or False if no settings are found.

Note: This module may have dependencies on external libraries and database connections, such as Pandas, Matplotlib, Seaborn, Anvil, and MySQL, 
        based on the context in which it is used.


"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # NOTE prevents: RuntimeError: main thread is not in main loop (NEEDED FOR UPLINK)
import json
from .graphs.bar_chart import BarChart
from Globals import df2serialized, serialized2df
from Globals import AnvilMedia


# Uplink imports:
try:
    import utils.mySQL_utils as localSQL
    from utils.log_errors_utils import write_error_log, write_debug_log
# Local host imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local host imports in graphs_uplink.py")
    from ..utils import mySQL_utils as localSQL
    from ..utils.log_errors_utils import write_error_log, write_debug_log




def update_database(chart_settings: dict) -> bool:
    """
        Function Description:
            - Called from graphs_uplink.update_chart_settings
            - Check if user has chart settings already stored, if not create a new row in table for them
            - Write new chart settings to data-table to `user_graph_settings`
            
        Input Args:
            - chart_settings (dict): dict storing users chart settings

        Output Args:
            - bool: Indicates if successful update of chart settings
    """

    #Unpack dict:
    email = chart_settings['email']
    gin_name = chart_settings['gin_name']
    num_gin_stands = chart_settings['num_gin_stands']
    chart_type =  chart_settings['graph-type']
    chart_scale =  chart_settings['graph-scale']

    try:
        # establish sql connection:
        cnx = localSQL.sql_connect()

        # Check if a user already has a row in the table:
        select_query = f"SELECT id FROM user_graph_settings WHERE user_email = '{email}'"

        existing_user = localSQL.sql_select(cnx, select_query)

        # If user already exists
        if existing_user:
            print(f"User {email} already exists... updating graph settings")

            # Update users stored graph settings:
            update_query = f"UPDATE user_graph_settings SET chart_type = '{chart_type}', chart_scale = '{chart_scale}', gin_name = '{gin_name}', num_gin_stands = {num_gin_stands} WHERE user_email = '{email}'" 

            localSQL.sql_update(cnx, update_query)

        else:
            # If user does not have chart settings stored, create a row in database for them:
            print(f"User {email} not found... creating new entry")
            returned_bool = create_user_chart_settings_entry(cnx,
                                                             email, 
                                                             gin_name, 
                                                             num_gin_stands,
                                                             chart_type=chart_type,
                                                             chart_scale=chart_scale)

    except (Exception) as sqlErr:
        # Create error message:
        err_msg = f"Encountered error in, File: graphs_uplink, Function: update_database func. \nError: {sqlErr}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    else:
        print("chart settings updated successfully")
        return True
    finally:
        localSQL.sql_closeConnection(cnx)


def create_user_chart_settings_entry(cnx,
                                     email: str, 
                                     gin_name: str, 
                                     num_gin_stands: int, 
                                     chart_type: str="Event Cluster", 
                                     chart_scale: str="Auto-Scale",
                                     retrieve_settings: bool=False):
    """
        Function Description:
            - Called from graphs_uplink.update_database and graphs_uplink.retrieve_chart
            - When called from retrieve_chart: retrieve_settings will be True.
                - This event occurs when the user wants to display a chart before first creating their own chart settings.
                  We will give them default chart settings for which ever gin is currently active.
            - Adds an entry (row) to table `user_graph_settings` for the user  
            
        Input Args:
            - cnx: database connection 
            - email (str): users email
            - gin_name (str): name of gin user wants graph to be from
            - num_gin_stands (int): number of gin stands from gin_name
            - chart_type (str): Type of chart (default is Event Cluster)
            - chart_scale (str): Auto-scale, 100 bales, etc.
            - retrieve_settings (bool): 

        Output Args:
            - If retrieve_settings: return users graph_results
                - graph_results (): Chart settings 
            - If not retrieve_settings: return bool 
    """

    try:

        # insert query to add (insert) a new row into user_graph_settings:
        insert_query = f"""INSERT INTO user_graph_settings (DataSource, chart_type, chart_scale, x_title, y1_title, y2_title, y1_data_column, y2_data_column, xy_font_color, xy_font_size, 
                                                                title, title_color, column_colors, legend, gin_name, num_gin_stands, user_email)
                                                                VALUES ('gin_data', '{chart_type}', '{chart_scale}', 'Event Clusters', 'Plastic Count', NULL, 'plastic', NULL, 'black', 10, 'Plastic Events', 
                                                                'black', 'standard', True, '{gin_name}', {num_gin_stands}, '{email}');"""

        localSQL.sql_insert(cnx, insert_query)

    except(Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: graphs_uplink, Function: create_user_chart_settings_entry func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False
    
    if retrieve_settings:
        # retrieve and return chart settings
        graph_results = get_user_chart_settings(email)

        return graph_results
    else:
        return True



def update_chart_settings(chart_settings: json) -> bool:
    """
        Function Description:
            - Called from anvil_uplink_router.update_chart_settings
            - Updates users chart settings data in database
            
        Input Args:
            - chart_settings (json(dict)): dict storing users new chart settings
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

    # Convert to type python dict
    chart_settings_dict = json.loads(chart_settings)

    # Write changes to database:
    update_bool = update_database(chart_settings_dict)

    return update_bool




def retrieve_chart(user_data: json) -> AnvilMedia:
    """
        Function Description:
            - Called from anvil_uplink_router.retrieve_chart
            
        Input Args:
            - user_data (json(dict)): stores users `email` used to retrieve chart with WHERE sql keyword

        Output Args:
            - chart_anvil_media (Anvil.Media): retrieved matplotlib chart of type Anvil.Media for convient displaying on client.
    """

    # Convert to type Python Dict
    user_data_dict = json.loads(user_data)

    # Unpack dictionary
    email = user_data_dict['email']
    gin_name = user_data_dict['gin_name']
    num_gin_stands = user_data_dict['num_gin_stands']

    # Retrieve chart settings
    chart_settings = get_user_chart_settings(email)

    # If no chart settings found for user -> create entry and grab default settings:
    if not chart_settings:
        print(f"User {email} not found... creating new entry")

        try:
            cnx = localSQL.sql_connect()

            # Create user chart settings and retrieve default settings
            chart_settings = create_user_chart_settings_entry(cnx,
                                                              email, 
                                                              gin_name, 
                                                              num_gin_stands,
                                                              retrieve_settings=True)
            
        except(Exception) as err:
            print(f"Error in retrieve_chart func.\n{err}")

        finally:
            localSQL.sql_closeConnection(cnx)


    # Clear the chart:
    plt.clf()
    
    # Create the chart:
    # Create a bar chart instance
    barchart = BarChart(chart_settings)
    
    # For now only bar charts:
    chart_anvil_media = barchart.create_bar_chart()

    return chart_anvil_media


def get_user_chart_settings(user_email: str) -> tuple:
    """
        Function Description:
            - Called from graphs_uplink.retrieve_chart
            - Retrieves the stored user chart settings in table `user_graph_settings`
            - (See create_db_tables for all table settings)
            
        Input Args:
            - user_email (str): Email of user used in sql select WHERE keyword

        Output Args:
            - graph_results (tuple): Retrieved chart settings from `user_graph_settings` table
    """
    """ Simulate chart types and data"""

    # Get users chart settings:
    try:

        # Connect to database
        cnx = localSQL.sql_connect()

        # Select user chart settings (see create_db_tables for all table settings)
        select_query = f"SELECT * FROM user_graph_settings WHERE user_email = '{user_email}'" 

        graph_results = localSQL.sql_select(cnx, select_query)

        # If user has already specified their chart settings, we will enter here:
        if graph_results:
            print(f"Chart settings found for user {user_email}")
            graph_results = graph_results[0]

            return graph_results

        # If user has not set up chart settings we will return False (Will user default settings for users chart)
        else:
            # Occurs if user has not set up chart settings yet
            # Debug log
            print(f"Unable to retrieve chart settings for user {user_email}\nCreating new entry and using default settings...")

            return False
    

    except(Exception) as err:
        # Create error message:
        err_msg = f"Encountered error in, File: graphs_uplink, Function: get_user_chart_settings func. \nError: {err}"
        # Write error to error log:
        write_error_log(err_msg=err_msg)
        print(err_msg)
        return False

    finally:
        localSQL.sql_closeConnection(cnx)

    
 