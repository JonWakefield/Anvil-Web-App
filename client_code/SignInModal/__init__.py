from ._anvil_designer import SignInModalTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import json
from anvil.js import window

class SignInModal(SignInModalTemplate):
  def __init__(self,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def log_in_button_click(self, **event_args):
    """ Check if username and password is correct"""

    # Variable to indiciate if user left a field blank
    empty_field_bool = False

    # Get fields:
    email = self.email_tb.text
    password = self.password_tb.text

    if email is '':
      self.email_error_label.visible = True
      empty_field_bool = True
    else:
      self.email_error_label.visible = False

    if password is '':
      self.password_error_label.visible = True
      empty_field_bool = True
    else:
      self.password_error_label.visible = False

    if empty_field_bool:
      return

    user_login_creds = json.dumps({
      'email': email,
      'password': password
    })

    returned_value = anvil.server.call("user_login", user_login_creds)

    if returned_value:
      self.login_failed_label.visible = False
      # Refresh the users browser:
      window.location.reload()
    else:
      self.login_failed_label.visible = True
    



      



