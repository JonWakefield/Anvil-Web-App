#!/bin/bash

# Start up shell script that performs the following actions for the user:
# Phase 1: Install all system dependencies:
    # 1) Install Git
    # 2) Install Ansible

# 1) Install Git
if command -v git &>/dev/null; then
    echo "Git is already installed."
else
    # Update package lists
    sudo apt update

    # Install Git:
    sudo apt install git -y

    # Verify installation
    git_version=$(git --version)
    if [[ $git_version ]]; then
        echo "Git install completed..."
    else
        echo "git installation failed... exiting script"
        exit 1 # Exit script if installation failed
    fi
fi


# 2) Install Ansible:
if command -v ansible &>/dev/null; then
    echo "Ansible is already installed."
else
    # Add Ansible repository
    sudo apt-add-repository --yes --update ppa:ansible/ansible

    # Install Ansible
    sudo apt install ansible -y 

    # Verify Ansible installation
    ansible_version=$(ansible --version)
    
    if [[ $ansible_version ]]; then
        echo "Ansible has been installed successfully. Version: $ansible_Version"

    else
        echo "Ansible installation failed... exiting script"
        exit 1 # exit the script if ansible installation fails
    fi
fi

# 3) Make project directory:
# Project holder
project_folder="$HOME/Desktop/local_website"

if [ ! -d "$project_folder" ]; then
    mkdir -p "$project_folder"
    if [ $? -eq 0 ]; then
        echo "project directory created"
    else
        echo "Failed to create project directory"
    fi
else
    echo "project directory folder already created, skipping creation..."
fi


# Phase 2:

# 1) Clone Pides_VIEWER

anvil_web_app_repo="https://github.com/jonwakefield/anvil-web-app"


if [ ! -d "$project_folder/Pides_VIEWER" ]; then
    git clone "$anvil_web_app_repo" "$project_folder/Pides_VIEWER"
    if [ $? -eq 0 ]; then
        echo "Repository downloaded successfully to $project_folder."
    else
        echo "Failed to download repository"
    fi
else
    echo "Destination folder '$project_folder' already exists. Skipping download. "
    exit 1
fi

# 2) Clone anvil-web-app dependencies

anvil_extras_repo="https://github.com/anvilistas/anvil-extras"
hash_routing_repo="https://github.com/s-cork/HashRouting"

# Clone anvil_extras repo:
if [ ! -d "$project_folder/anvil_extras" ]; then
    git clone "$anvil_extras_repo" "$project_folder/anvil_extras"
    if [ $? -eq 0 ]; then
        echo "Anvil Extras repo successfully installed"
    else
        echo "Failed to download anvil_extras repo"
    fi
else
    echo "Destination folder '$project_folder' already exists. Skipping download. "
    exit 1
fi


# Clone hash_routing repo:
if [ ! -d "$project_folder/HashRouting" ]; then
    git clone "$hash_routing_repo" "$project_folder/HashRouting"
    if [ $? -eq 0 ]; then
        echo "HashRouting repo successfully installed"
    else
        echo "Failed to download HashRouting repo"
    fi
else
    echo "Destination folder '$project_folder' already exists. Skipping download. "
    exit 1
fi

# Create WWW folder:
www_folder="$project_folder/www"

if [ ! -d "$www_folder" ]; then
    mkdir -p "$www_folder"
    if [ $? -eq 0 ]; then
        echo "'www' folder created successfully. "
    else
        echo "Failed to create the 'www' folder."
        exit 1
    fi
else
    echo "'www' folder already created... skipping creation..."
fi


# Move Docker files to `local_website/`
source_dir="$HOME/Desktop/local_website/Pides_VIEWER/DevOps/Docker/"
destination_dir="$HOME/Desktop/local_website/"

echo "Moving Docker files"
mv "${source_dir}"* "${destination_dir}"



# 3) Run ansible-startup script
ansible_script_path="$HOME/Desktop/local_website/Pides_VIEWER/DevOps/Ansible/server_setup.yaml"
hosts_script_path="$HOME/Desktop/local_website/Pides_VIEWER/DevOps/Ansible/hosts_cloud.ini"


# Check if Ansible script exists:
if [ -f "$ansible_script_path" ]; then
    # Run the ansible script
    echo "Running Ansible playbook..."
    ansible-playbook -i "$hosts_script_path" "$ansible_script_path"
    if [ $? -eq 0 ]; then
        echo "Ansible playbook executed successfully"
    else
        echo "Failed to execute Ansible Playbook"
    fi
else
    echo "Ansible playbook not found at '$ansible_script_path'."
fi


build_script_path="$HOME/Desktop/local_website/build.sh"
entry_script_path="$HOME/Desktop/local_website/entry.sh"


# Execute build.sh
if [ -f "$build_script_path" ]; then
    echo "Changing files to executables "
    chmod +x "$build_script_path"
    chmod +x "$entry_script_path"
    echo "Startin Docker build script"
    bash "$build_script_path"
    if [ $? -eq 0 ]; then
        echo "build.sh script executed successfully."
    else
        echo "Failed to execute build.sh script."
    fi
else
    echo "build.sh script not found at '$build_script_path'."
fi