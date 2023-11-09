"""
    NOT USED FOR DEPLOYMENT
    THIS SCRIPT IS ONLY USED FOR DEVELOPMENT

    Author: Jon Wakefield
    Date: 08/24/2023
    Decription:
        - This script is used tO simulate `imageAges` in the `ginStand` data-table
        - Allows for simluated "plastic events" to be added to the data-table
        - Helps verify gin monitor form is working


   

"""

import random
#Uplink Imports
try:
    from utils.dateTime_utils import get_currentEpochTime_secs
    import utils.mySQL_utils as localSQL

#Local Server imports:
except (ModuleNotFoundError) as mod_err:
    print("Trying local server imports in simulate_imageAges.py")
    from .dateTime_utils import get_currentEpochTime_secs
    from . import mySQL_utils as localSQL
    

def generate_random_numbers():
    # Number of rand ints to generate:
    # n = random.randint(1, 2)
    n = 2
    numbers = []

    # print(f"Number of random entries: {n}")

    # if n > 3:
    #     # don't update
    #     print("Not updating table..")
    #     return []

    for _ in range(n):
        number = random.randint(0,12)
        numbers.append(number)

    # print(f"Rows to update: {numbers}")


    return numbers


def get_last_n_rows_with_condition(n, condition_value):
    """ Function gets the length (# of rows) in  a table"""

    # Connect to database
    cnx = localSQL.sql_connect()

    # Create a cursor
    cursor = cnx.cursor()

    row_id_result = []

    for i in range(n):
        sql_query = f"SELECT Id FROM ginStands WHERE ginName = '{condition_value}' AND ginStandNum = {i+1} ORDER BY Id DESC LIMIT {1};"

        cursor.execute(sql_query)

    # length = cursor.fetchone()[0]
        result = cursor.fetchall()[0]
        print(result)
        row_id_result.append(result[0])

    cursor.close()
    localSQL.sql_closeConnection(cnx)

    print(row_id_result)

    # print(f" Last Id's for ginStand with ginName = {condition_value}: {result}")

    return row_id_result


def simulate_table_entries(ginName):
    """Simulate dummy time values to propagate into the ginStand data-table
        1. Get current time
        2. Put time into database
    """

    
    num_events = random.randint(1,3)

    time_consts = [-300, -60, -0, -180]
    gin_stand_num_list = [1,2,3,4]
    num_rows = len(gin_stand_num_list)
    gin_names = ['Cherokee', 'UCG', 'Spade', 'WhiteOak']
    # randNums = generate_random_numbers()

    cnx = localSQL.sql_connect()

    print(f"Simulating {num_events} entries...")
    for i in range(num_events):
        rand_gin = random.randint(0,3)
        # Get current time:
        currentTime = get_currentEpochTime_secs()

        # Manipulate the current time to give some variation:
        time = currentTime + time_consts[i]

        gin_stand_num = gin_stand_num_list[rand_gin]

        filePath = '/var/www/PidesMonitor/images/' + ginName + '/gs' + str(gin_stand_num) + '.png'

        HID_status = random.choice([True, False])

        # Store in database:
        # update_query = f"INSERT INTO ginStands (ginName, ginStandNum, pic_age, fileName) VALUES ('{ginName}', {random_intginNum}, {time}, '{filePath}');"
        update_query = f"INSERT INTO gin_stand_events (gin_name, gin_stand_num, pic_age, file_name, HID_status) VALUES ('{ginName}', {gin_stand_num}, {time}, '{filePath}', {HID_status});"


        localSQL.sql_insert(cnx, update_query)

    print(f"Added {num_rows} rows to table...")

    localSQL.sql_closeConnection(cnx)
    print("Table updated successfully")


from time import sleep
if __name__ == "__main__":
    # sleep(300)
    # start_simulate_table_entries()
    simulate_table_entries()
    # l = get_last_n_rows_with_condition(4, "UCG")