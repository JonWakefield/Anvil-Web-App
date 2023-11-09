# Shell Build script to run all ansible playbooks:

#echo "Running deployment ansible script"
# Run `notes on deployment` ansible script:

#echo "Deployment successfully setup"

echo "Running Anvil-Web-App Playbook..."
# Run playbook here
ansible-playbook -i inventory.ini anvil-web-app.yaml

echo "Anvil Web App Successfully Set Up"

echo "Setting up maria-db"
# Run maria-db playbook here:
ansible-playbook -i inventory.ini maria-db.yaml

echo "Maria-db successfully set-up"


