""" Simulate Plastic detection entries into database"""

import random
from datetime import datetime, timedelta

# Uplink imports:
try:
    import mySQL_utils as localSQL

# Local Host imports:
except(ModuleNotFoundError) as mod_err:
    print("trying local server imports in simulate_plastic_events.py")
    from . import mySQL_utils as localSQL


def add_entries_to_table(num_entries, gin_name, num_gin_stands):

    first_event = random.randint(1, 8)
    days=random.randint(1, 30)
    minute=random.randint(1,6)
    org_min = minute
    
    print(f"Selected day is {days} ago")
    try:

        cnx = localSQL.sql_connect()

        for _ in range(num_entries):
            # Generate random data for each entry
            port = random.randint(4300, 4399)  # Random port number
            gin_stand_num = random.randint(1, num_gin_stands)  # Random gin stand number
            gin_stand_pos = random.randint(1, 2)  # Random gin stand position
            # UTC = (datetime.now() - timedelta(days)).strftime('%Y-%m-%d %H:%M:%S')  # Random UTC datetime
            UTC = (datetime.now() - timedelta(days)).replace(
                hour=first_event,
                minute=minute,
                second=random.randint(0,50),
                microsecond=0
            ).strftime('%Y-%m-%d %H:%M:%S') 

            # Define the SQL INSERT statement
            insert_query = f"""
                INSERT INTO plastic_events (port, gin_name, gin_stand_num, gin_stand_pos, UTC)
                VALUES ({port}, '{gin_name}', {gin_stand_num}, {gin_stand_pos}, '{UTC}')
            """

            # Insert data into the table
            localSQL.sql_insert(cnx, insert_query)

            minute += org_min

        print(f"{num_entries} entries added to the table successfully.")

    except (Exception) as e:
        print(f"Error: {e}")
    finally:
        localSQL.sql_closeConnection(cnx)


# Make sure code is only ran if user runs file"
if __name__ == "__main__":

    NUM_CLUSTERS = 5

    for i in range(NUM_CLUSTERS):
        # Num events to occur:
        num_events = random.randint(4, 10)
        gin_names = ['Spade', 'UCG', 'WhiteOak', 'Cherokee']  # Random gin name
        gin_info = {'Cherokee': 3, 'Spade': 4, 'UCG': 6, 'WhiteOak': 1}
        randint = random.randint(0,3)
        gin_name = gin_names[randint]

        num_gin_stands = gin_info[gin_name]

        print(f"Adding {num_events} to table for gin {gin_name}")
        add_entries_to_table(num_events, gin_name, num_gin_stands)


