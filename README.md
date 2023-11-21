# PIDES Viewer

### Description:

    - This repository includes the complete code-base to setup, execute, and run the PIDES Viewer Anvil-web-app.

### Table of Contents:

    - [Description](#description)
    - [Installation](#installation)
    - [Contributing](#contributing)


### Website Features

    - User specific accounts and persistant login
    - Website operates on users local network, ensuring isolated data protection
    - Ability remotely configure RPi Camera Settings
    - Ability to view, add, or remove RPi camera nodes, allowing for quick setup, diagnosis, and install 
    - Up to date gin monitoring activity
    - Easy-to-build charts to monitor gin stand output and view results.


## Installation:

    Prerequisites

1. Clone git repository:
    `git clone https://github.com https://github.com/jonwakefield/anvil-web-app`

2a. After cloning, give `startup.sh` executable privileges:
    `chmod +x startup.sh`

2b. Run startup.sh
    `./startup.sh`

3. After running startup.sh, the localwebsite should available on your network

### Client-to-Server File Connections:

    - All Client-Side Forms can be found in the client_code folder
        - To communicate with a server side module, all client side forms route to anvil_uplink_router.py
          (This helps organize the code by allowing each client-form to have its own respective server module)

    - Anvil_uplink_router:
        - Routes recieved client data to the appropriate server side module

        - Returns data back to client side
        - Ex: FormCamControls --[data]--> anvil_uplink_router --[data]--> camera_controls_uplink --[returned_data]--> anvil_uplink_router --[returned_data]--> FormCamControls

    Graphical Representation:
    ![Alt text](image.png) 

#### Table Explanations:

    - Table: anvil_imgClassification
        - Description:
            Table used to store labels for images, path to images, and JOINT classifiers prediction.

        - Files Used In:
            picture_capture_controls.py
            stack.py


        Structure:
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


    - Table: anvil_imgProcessor
        - Description: 
            Tables stores images & identification number on images that are currently being processed by the JOINT classifier
        - Files Used In:
            picture_capture_controls.py

        Structure:
        +-----------+-----------+------+-----+---------+----------------+
        | Field     | Type      | Null | Key | Default | Extra          |
        +-----------+-----------+------+-----+---------+----------------+
        | id        | int(11)   | NO   | PRI | NULL    | auto_increment |
        | job_id    | char(128) | YES  |     | NULL    |                |
        | img_name  | char(64)  | YES  |     | NULL    |                |
        | img_label | char(32)  | YES  |     | NULL    |                |
        +-----------+-----------+------+-----+---------+----------------+

    - Table: users
        - Description: 
            Table stores user info, role, hashed password, active gin and gins accessible. Users info must be stored in table for a user to log in
        - Files Used In:
            user_management.py


        Structure:
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

    - Table: users_log
        - Description: 
            Logs user activity including: login, logout, password change, and gin change
        - Files Used In:
            user_management.py

        Structure:
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


    - Table: log_user_request_acc
        - Description: 
            Logs user account creation request. Does not have an connection to `users` table.
        - Files Used In:
            user_management.py

        Structure:
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

    - Table: plastic_events
        - Description:
            Table that stores detected plastic events. Events are used to create graphs displayed to user.  

        - Files Used In:
            bar_chart.py

        Structure:
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


    - Table: gins
        - Description: 
            Stores basic gin info including gin name, number of gin stands,and location (state) of gin.
        - Files Used In:
            user_management.py
            nodes_connected_uplink.py

        Structure:
        +----------------+-------------+------+-----+---------+----------------+
        | Field          | Type        | Null | Key | Default | Extra          |
        +----------------+-------------+------+-----+---------+----------------+
        | id             | int(11)     | NO   | PRI | NULL    | auto_increment |
        | gin_name       | varchar(32) | YES  |     | NULL    |                |
        | num_gin_stands | int(10)     | YES  |     | NULL    |                |
        | location       | varchar(32) | YES  |     | NULL    |                |
        +----------------+-------------+------+-----+---------+----------------+

    - Table: user_graph_settings
        - Description: 
            Stores chart settings for each user allowing them to have user specific chart data
        - Files Used In:
            graphs/graphs_uplink.py


        Structure:
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

    - Table: gin_stand_events
        - Description: 
            Table stores detected gin events and location of image; allowing for retrieval and displaying of image to user.
        - Files Used In:
            gin_monitor_uplink.py

        Structure:
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

    - Table: CamNodes_Info
        - Description: 
            Table stores port # and location (gin name, gin stand num, and position) of port #, allowing for modification of camera settings on the correct node.
        - Files Used In:
            camera_controls_uplink.py

        Structure:
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


