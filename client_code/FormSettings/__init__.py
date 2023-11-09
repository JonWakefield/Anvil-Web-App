from ._anvil_designer import FormSettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from HashRouting import routing
from .. import Globals
from time import sleep
from anvil.js import window
import json

# obv this is a comment

@routing.route('settings', full_width_row=True) 
class FormSettings(FormSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.username = Globals.user['username']
    self.email = Globals.user['email']
    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin']
    self.gins_accessible = Globals.user['gins_accessible']

    self.password_change_label.visible = False

    # Set up the users list of accessible gins
    self.gin_name_drop_down.items = self.gins_accessible
    self.gin_name_drop_down.selected_value = self.gin_name
    
  def log_out_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    user_data = Globals.user
    returned_data = anvil.server.call("user_log_out", user_data)

    if returned_data:
      # Refresh the users browser:
      routing.set_url_hash(url_pattern='')
      routing.clear_cache()
      window.location.reload()
    else:
      alert("Unable to log out. Please contact an administrator")

  def change_password_button_click(self, **event_args):
    """Allow users to change password"""

    cur_password = self.current_password_tb.text
    new_password = self.new_password_tb.text

    user_data = json.dumps({
      'username': self.username,
      'email': self.email,
      'role': self.role,
      'active_gin': self.gin_name,
      'cur_password': cur_password,
      'new_password': new_password
    })

    returned_dict = anvil.server.call("change_user_password", user_data)

    changed_password = returned_dict['changed_password']
    if changed_password:
      self.password_change_label.text = "Password Successfully Changed"
      self.password_change_label.foreground = "#333"
      self.password_change_label.visible = True
    else:
      error_code = returned_dict['error_code']
      if error_code == 1:
        self.password_change_label.text = "Incorrect Current Password"
        self.password_change_label.foreground = "#FF0000"
        self.password_change_label.visible = True
      elif error_code == 2:
        self.password_change_label.text = "Unable to Update password"
        self.password_change_label.foreground = "#FF0000"
        self.password_change_label.visible = True
      
      

  def change_gin_button_click(self, **event_args):
    """ Change which gin user has access too"""

    # Get users selection:
    new_gin = self.gin_name_drop_down.selected_value
    user_data = json.dumps({
      'username': self.username,
      'email': self.email,
      'role': self.role,
      'active_gin': new_gin
    })
    print(f"new gin: {new_gin}")
    returned_bool = anvil.server.call("change_gin_access", user_data)

    if returned_bool:
      # refresh page:
      window.location.reload()
    else:
      alert("Error changing gin. Please contact an admin")

  def show_cur_password(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if(self.show_cur_password_cbox.checked):
      self.current_password_tb.hide_text = False
    else:
      self.current_password_tb.hide_text = True

  def show_new_password(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if(self.show_new_password_cbox.checked):
      self.new_password_tb.hide_text = False
    else:
      self.new_password_tb.hide_text = True

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""

    anvil.server.call("_check_user_password", self.username)










