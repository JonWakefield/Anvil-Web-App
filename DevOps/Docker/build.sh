#!/bin/bash

# Description: Build script for anvil-web-app
#		Use Directions:
#		1. Navigate to the project directory
#		2. Run './build.sh' (or 'sudo ./build.sh')
#		   Running this command should result in the succesfull setup of the docker-compose file
#		   After all services have been set-up 'entry.sh' will start execution.
#			The final product will be a running web-server with a fully setup and functional database



# Gather the UID and GID of the current user.
# Note: Try uncommenting the following two-lines, if it doesn't work use default value of 1000
#MY_UID=$(id -u)
#MY_GID=$(id -g)
MY_UID=1000
MY_GID=1000

# Remove previous containers:
docker rm -f anvil_container
docker rm -f mariadb_container

# Remove all unused dangling docker images
docker image prune -a

# Build path for when running script via startup.sh
build_path="$HOME/Desktop/local_website/docker-compose.yaml"

# Build the docker image passing in the UID and GID args
# docker-compose build --build-arg MY_UID=$MY_UID --build-arg MY_GID=$MY_GID --no-cache
docker-compose -f "$build_path" build --build-arg MY_UID=$MY_UID --build-arg MY_GID=$MY_GID --no-cache

# Start the containers
#docker-compose up -d
docker-compose up 

# Executable command:
#docker exec -it anvil_container bash
