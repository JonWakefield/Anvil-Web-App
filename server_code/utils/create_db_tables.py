"""
    Script creates the necessary data-tables for VISN web-app monitor

    anvil_imgClassification table:
    +----------+-----------+------+-----+---------+----------------+
    | Field    | Type      | Null | Key | Default | Extra          |
    +----------+-----------+------+-----+---------+----------------+
    | id       | int(11)   | NO   | PRI | NULL    | auto_increment |
    | Cotton   | char(32)  | YES  |     | NULL    |                |
    | Plastic  | char(32)  | YES  |     | NULL    |                |
    | Tray     | char(32)  | YES  |     | NULL    |                |
    | HID      | char(32)  | YES  |     | NULL    |                |
    | Other    | char(32)  | YES  |     | NULL    |                |
    | GotWrong | char(32)  | YES  |     | NULL    |                |
    | PATH     | char(128) | YES  |     | NULL    |                |
    | JOINT    | char(32)  | YES  |     | NULL    |                |
    +----------+-----------+------+-----+---------+----------------+

    anvil_imgProcessor table:
    +-----------+-----------+------+-----+---------+----------------+
    | Field     | Type      | Null | Key | Default | Extra          |
    +-----------+-----------+------+-----+---------+----------------+
    | id        | int(11)   | NO   | PRI | NULL    | auto_increment |
    | job_id    | char(128) | YES  |     | NULL    |                |
    | img_name  | char(64)  | YES  |     | NULL    |                |
    | img_label | char(32)  | YES  |     | NULL    |                |
    +-----------+-----------+------+-----+---------+----------------+

    users table:
    +-----------------+--------------+------+-----+---------+----------------+
    | Field           | Type         | Null | Key | Default | Extra          |
    +-----------------+--------------+------+-----+---------+----------------+
    | id              | int(11)      | NO   | PRI | NULL    | auto_increment |
    | username        | varchar(64)  | YES  |     | NULL    |                |
    | email           | varchar(64)  | YES  |     | NULL    |                |
    | password_hash   | varchar(255) | YES  |     | NULL    |                |
    | active_gin      | varchar(64)  | YES  |     | NULL    |                |
    | role            | varchar(64)  | YES  |     | NULL    |                |
    | gins_accessible | varchar(100) | YES  |     | NULL    |                |
    +-----------------+--------------+------+-----+---------+----------------+

    users_log table:
    +------------+-------------+------+-----+---------+----------------+
    | Field      | Type        | Null | Key | Default | Extra          |
    +------------+-------------+------+-----+---------+----------------+
    | id         | int(11)     | NO   | PRI | NULL    | auto_increment |
    | email      | varchar(64) | YES  |     | NULL    |                |
    | role       | varchar(64) | YES  |     | NULL    |                |
    | active_gin | varchar(64) | YES  |     | NULL    |                |
    | type       | varchar(32) | YES  |     | NULL    |                |
    | time       | datetime    | YES  |     | NULL    |                |
    +------------+-------------+------+-----+---------+----------------+

    log_user_request_acc table:
    +----------------+-------------+------+-----+---------+----------------+
    | Field          | Type        | Null | Key | Default | Extra          |
    +----------------+-------------+------+-----+---------+----------------+
    | id             | int(11)     | NO   | PRI | NULL    | auto_increment |
    | firstname      | varchar(64) | YES  |     | NULL    |                |
    | lastname       | varchar(64) | YES  |     | NULL    |                |
    | email          | varchar(64) | YES  |     | NULL    |                |
    | gin_name       | varchar(64) | YES  |     | NULL    |                |
    | requested_role | varchar(64) | YES  |     | NULL    |                |
    | time_requested | datetime    | YES  |     | NULL    |                |
    +----------------+-------------+------+-----+---------+----------------+

    plastic_events table:
    +---------------+-------------+------+-----+---------+----------------+
    | Field         | Type        | Null | Key | Default | Extra          |
    +---------------+-------------+------+-----+---------+----------------+
    | id            | int(11)     | NO   | PRI | NULL    | auto_increment |
    | port          | int(11)     | YES  |     | NULL    |                |
    | gin_name      | varchar(40) | YES  |     | NULL    |                |
    | gin_stand_num | int(11)     | YES  |     | NULL    |                |
    | gin_stand_pos | int(11)     | YES  |     | NULL    |                |
    | UTC           | datetime    | YES  |     | NULL    |                |
    +---------------+-------------+------+-----+---------+----------------+

    gins table:
    +----------------+-------------+------+-----+---------+----------------+
    | Field          | Type        | Null | Key | Default | Extra          |
    +----------------+-------------+------+-----+---------+----------------+
    | id             | int(11)     | NO   | PRI | NULL    | auto_increment |
    | gin_name       | varchar(32) | YES  |     | NULL    |                |
    | num_gin_stands | int(10)     | YES  |     | NULL    |                |
    | location       | varchar(32) | YES  |     | NULL    |                |
    +----------------+-------------+------+-----+---------+----------------+

    user_graph_settings table:
    +----------------+--------------+------+-----+---------+----------------+
    | Field          | Type         | Null | Key | Default | Extra          |
    +----------------+--------------+------+-----+---------+----------------+
    | id             | int(11)      | NO   | PRI | NULL    | auto_increment |
    | DataSource     | varchar(100) | YES  |     | NULL    |                |
    | chart_type     | varchar(20)  | YES  |     | NULL    |                |
    | chart_scale    | varchar(40)  | YES  |     | NULL    |                |
    | x_title        | varchar(100) | YES  |     | NULL    |                |
    | y1_title       | varchar(100) | YES  |     | NULL    |                |
    | y2_title       | varchar(100) | YES  |     | NULL    |                |
    | y1_data_column | varchar(100) | YES  |     | NULL    |                |
    | y2_data_column | varchar(100) | YES  |     | NULL    |                |
    | xy_font_color  | varchar(20)  | YES  |     | NULL    |                |
    | xy_font_size   | int(11)      | YES  |     | NULL    |                |
    | title          | varchar(200) | YES  |     | NULL    |                |
    | title_color    | varchar(20)  | YES  |     | NULL    |                |
    | column_colors  | varchar(40)  | YES  |     | NULL    |                |
    | legend         | tinyint(1)   | YES  |     | NULL    |                |
    | gin_name       | varchar(40)  | YES  |     | NULL    |                |
    | num_gin_stands | int(10)      | YES  |     | NULL    |                |
    | user_email     | varchar(40)  | YES  |     | NULL    |                |
    +----------------+--------------+------+-----+---------+----------------+

    gin_stand_events table:
    +---------------+--------------+------+-----+---------+----------------+
    | Field         | Type         | Null | Key | Default | Extra          |
    +---------------+--------------+------+-----+---------+----------------+
    | id            | int(11)      | NO   | PRI | NULL    | auto_increment |
    | gin_name      | varchar(32)  | YES  |     | NULL    |                |
    | gin_stand_num | int(10)      | YES  |     | NULL    |                |
    | pic_age       | int(11)      | YES  |     | NULL    |                |
    | file_name     | varchar(120) | YES  |     | NULL    |                |
    | HID_status    | tinyint(1)   | YES  |     | NULL    |                |
    +---------------+--------------+------+-----+---------+----------------+

    CamNodes_Info:
    +----+--------+------+----------+-------------+---------------------+
    | id | Active | port | GinName  | GinStandNum | GinStandPositionNum |
    +----+--------+------+----------+-------------+---------------------+
    | 16 | NULL   | 3389 | Spade    |           3 |                   1 |
    | 19 | NULL   | 3306 | UCG      |           2 |                   1 |
    | 20 | NULL   | 3350 | Spade    |           2 |                   1 |
    | 34 | NULL   | 5400 | Spade    |           2 |                   1 |
    | 35 | NULL   | 6000 | Spade    |           4 |                   1 |
    | 36 | NULL   | 3333 | WhiteOak |           1 |                   1 |
    | 37 | NULL   | 4444 | WhiteOak |           1 |                   1 |
    | 38 | NULL   | 1234 | UCG      |           3 |                   1 |
    +----+--------+------+----------+-------------+---------------------+




"""
try:
    import mysql.connector
    import mySQL_utils as localSQL
    import json
    # create_db_tables.py
    import anvil.tables as tables
    import anvil.tables.query as q
    from anvil.tables import app_tables
    import anvil.users
except (ModuleNotFoundError) as mod_err:
    print("Module not found err in create_db_tables.py\n{mod_err}")

def create_anvil_imgClassification_table():

    # Create the table query:
    create_table_query = """
    CREATE TABLE anvil_imgClassification (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Cotton CHAR(32),
        Plastic CHAR(32),
        Tray CHAR(32),
        HID CHAR(32),
        Other CHAR(32),
        GotWrong CHAR(32),
        PATH CHAR(128),
        JOINT CHAR(32)
    )
    """

    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print("Table 'anvil_imgClassification' already created")
        return

    cnx.commit()

    print("Table 'anvil_imgClassification' sucessfully created")
        

def create_anvil_imgProcessing_table():

    # Create the table query:
    create_table_query = """
    CREATE TABLE anvil_imgProcessor (
        id INT AUTO_INCREMENT PRIMARY KEY,
        job_id CHAR(128),
        img_name CHAR(64),
        img_label CHAR(32)
    )
    """

    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print("Table 'anvil_imgProcessor' already created")
        return

    cnx.commit()

    print("Table 'anvil_imgProcessor' sucessfully created")


def create_users():

    # Create the table query:
    create_table_query = """
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(64),
        email VARCHAR(64),
        password_hash VARCHAR(255),
        active_gin VARCHAR(64),
        role VARCHAR(64),
        gins_accessible VARCHAR(100)
    )
    """
    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print("Table 'users' already created")
        print(sql_err)

    cnx.commit()
   

    print("Table 'users' sucessfully created")


def create_users_log():
    """Log user log in and log outs"""

    # Create the table query:
    create_table_query = """
    CREATE TABLE users_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(64),
        role VARCHAR(64),
        active_gin VARCHAR(64),
        type VARCHAR(32),
        time DATETIME
    )
    """
    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print("Table 'users_log' already created")
        print(sql_err)

    cnx.commit()

    print("Table 'users_log' sucessfully created")


def create_log_user_request_acc():
    """"""

    # Create the table query:
    create_table_query = """
    CREATE TABLE log_user_request_acc (
        id INT AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(64),
        lastname VARCHAR(64),
        email VARCHAR(64),
        gin_name VARCHAR(64),
        requested_role VARCHAR(64),
        time_requested DATETIME
    )
    """
    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print(f"SQL error in function create_user_request_access: \n{sql_err}")
        print("Table 'log_user_request_acc' already created")
        return

    cnx.commit()

    print("Table 'log_user_request_acc' sucessfully created")


def create_plastic_events_table():
    """"""

    create_table_query = """
    CREATE TABLE plastic_events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        port int,
        gin_name VARCHAR(40),
        gin_stand_num INT,
        gin_stand_pos INT,
        UTC DATETIME
    )
    """

    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print(f"SQL error in function create_simulate_cotton_data: \n{sql_err}")
        print("Table 'plastic_events' already created")
    else:
        print("Table 'plastic_events' sucessfully created")
        cnx.commit()


def create_gins_table():
    """Stores all gin names and location of gin"""

    create_table_query = """
    CREATE TABLE gins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gin_name VARCHAR(32),
        num_gin_stands INT(10),
        location VARCHAR(32)
    )
    """

    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print(f"SQL error in function create_graph_settings_table: \n{sql_err}")
        print("Table 'gins' already created")
    else:
        print("Table 'gins' sucessfully created")

    # insert each gin into table:
    insert_spade_query = f"INSERT INTO gins (gin_name, num_gin_stands, location) VALUES ('Spade', 4, 'Texas');"
    insert_ucg_query = f"INSERT INTO gins (gin_name, num_gin_stands, location) VALUES ('UCG', 6, 'Texas');"
    insert_cherokee_query = f"INSERT INTO gins (gin_name, num_gin_stands, location) VALUES ('Cherokee', 3, 'Alabama');"
    insert_whiteOak_query = f"INSERT INTO gins (gin_name, num_gin_stands, location) VALUES ('WhiteOak', 1, 'Missouri');"

    localSQL.sql_insert(cnx, insert_spade_query)
    localSQL.sql_insert(cnx, insert_ucg_query)
    localSQL.sql_insert(cnx, insert_cherokee_query)
    localSQL.sql_insert(cnx, insert_whiteOak_query)



    cnx.commit()


def create_user_graph_settings_table():

    create_table_query = """
    CREATE TABLE user_graph_settings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        DataSource VARCHAR(100),
        chart_type VARCHAR(20),
        chart_scale VARCHAR(40),
        x_title VARCHAR(100),
        y1_title VARCHAR(100),
        y2_title VARCHAR(100),
        y1_data_column VARCHAR(100),
        y2_data_column VARCHAR(100),
        xy_font_color VARCHAR(20),
        xy_font_size INT,
        title VARCHAR(200),
        title_color VARCHAR(20),
        column_colors VARCHAR(40),
        legend BOOLEAN,
        gin_name VARCHAR(40),
        num_gin_stands INT(10),
        user_email VARCHAR(40)
    )
    """


    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print(f"SQL error in function create_user_graph_settings_table: \n{sql_err}")
        print("Table 'user_graph_settings' already created")
    else:
        print("Table 'user_graph_settings' sucessfully created")


    cnx.commit()

    # Add our graph types to the table:
    """ Time interval Codes:
            1. start of season (Oct. 15)
            2. 30 days
            3. 7 days
            4. 12 hours
    """


def create_gin_stand_events_table():
    """"""

    create_table_query = """
    CREATE TABLE gin_stand_events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gin_name VARCHAR(32),
        gin_stand_num INT(10),
        pic_age INT(11),
        file_name VARCHAR(120),
        HID_status BOOLEAN
    )
    """

    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print(f"SQL error in function create_gin_stand_events_table: \n{sql_err}")
        print("Table 'gin_stand_events' already created")
    else:
        print("Table 'gin_stand_events' sucessfully created")

    cnx.commit()


def create_CamNodes_Info_table():
    """"""
    create_table_query = """
    CREATE TABLE CamNodes_Info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        port INT(10),
        GinName VARCHAR(32),
        GinStandNum INT(10),
        GinStandPositionNum INT(10),
        Active BOOLEAN  
    )
    """

    try:
        cursor.execute(create_table_query)
    except (mysql.connector.errors.ProgrammingError) as sql_err:
        print(f"SQL error in function create_CamNodes_Info_table: \n{sql_err}")
        print("Table 'CamNodes_Info' already created")
    else:
        print("Table 'CamNodes_Info' sucessfully created")

    cnx.commit()


if __name__ == "__main__":

    # Establish connection to the database
    # NOTE: IF USING ON A LOCALHOST (UBUNUT, RPI, ETC.) COMMENT THE BELOW cnx = ... LINES OUT
    cnx = mysql.connector.connect(
        host="maria-db",
        user="ginuser",
        password="Hello2018",
        database="camera_nodes"
    )

    # NOTE: IF USING INSIDE OF DOCKER CONTAINER COMMENT THE BELOW cnx = ... LINES OUT
    # cnx = mysql.connector.connect(
    #     host="localhost",
    #     user="ginuser",
    #     password="Hello2018",
    #     database="camera_nodes"
    # )


    # Create a cursor object to execute SQL statements:
    try:
        cursor = cnx.cursor()
    except (Exception) as err:
        print("Encountered an error, unable to login to database")
        print(err)
    else:
        # NOTE: comment out already created to tables to create only specific tables
        create_anvil_imgClassification_table()
        create_anvil_imgProcessing_table()
        create_users()
        create_gins_table()
        create_users_log()
        create_CamNodes_Info_table()
        create_log_user_request_acc()
        create_user_graph_settings_table()
        create_plastic_events_table()
        create_gin_stand_events_table()
    finally:
        cnx.close()