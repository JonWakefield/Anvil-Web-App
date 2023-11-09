import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import open_form, alert

from . import Globals


def main():
  # check if a user is logged in
  # Try to access cookie to see if a user is logged in or not:
  returned_user_data = anvil.server.call("check_user_login_status")

  if returned_user_data is None:
    print("Did not find a user")
    # Redirect user to login template:
    open_form("FormLandingPage")
  else:
    print("Found user!")
    print(returned_user_data)
    # Store user data in a global var
    Globals.user = returned_user_data

    open_form("MainRouter")


# Program starts here:
if __name__ == "__main__":
  main()
