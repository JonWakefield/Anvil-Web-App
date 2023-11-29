#!/bin/bash

# Description: Entry Script for `local_website` web-app Dockerfile.
#		This script is ran as the final step in the Dockerfile
#		`ENTRYPOINT ["app/entry.sh"]`
# 		Script first waits for MariaDB to be set-up, then adds all necessary anvil tables to database
#		Next, the script adds users to the database
#		Lastly, the script starts the web-app local server

echo "In the entry.sh file"
# set -e

# Wait for the MariaDB service to be ready
until nc -z -w 1 maria-db 3306; do
	echo "Waiting for MariaDB to start..."
	sleep 1
done

echo "MariaDB started... Creating tables..."

# Run python script to create tables
python /home/dcotton/app/Pides_VIEWER/server_code/utils/create_db_tables.py
echo "Tables created successfully... adding users in add_users.py"

# Add useres to `users` table
python /home/dcotton/app/Pides_VIEWER/server_code/add_admin_user.py

echo "Users added... Starting local server"


# Obtain the host devices IP address:
host_ip=$(hostname -I | cut -d' ' -f1)

echo "Host ip: $host_ip"
# Navigate to the app directory:
cd /home/dcotton/app
# anvil-app-server --app Pides_VIEWER --origin http://192.168.1.227:3030 --dep-id ZKNOF5FRVLPVF4BI=HashRouting --dep-id C6ZZPAPN4YYF5NVJ=anvil_extras
anvil-app-server --app Pides_VIEWER --origin http://"$host_ip":3030 --data-dir /home/dcotton/anvil-data --dep-id ZKNOF5FRVLPVF4BI=HashRouting --dep-id C6ZZPAPN4YYF5NVJ=anvil_extras
