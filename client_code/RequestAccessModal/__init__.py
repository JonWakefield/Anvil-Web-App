from ._anvil_designer import RequestAccessModalTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from anvil.js import window


class RequestAccessModal(RequestAccessModalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def check_fields_for_error(self, firstname, lastname, email, gin_name, role):
    """Check fields to ensure non-empty etc."""
    
    # Variable to indiciate if user left a field blank
    empty_field_bool = False
    
    # Check user is not empty:
    if firstname is '':
      self.firstName_error_label.visible = True
      empty_field_bool = True
    else:
      self.firstName_error_label.visible = False

    # Check user is not empty:
    if lastname is '':
      self.lastName_error_label.visible = True
      empty_field_bool = True
    else:
      self.lastName_error_label.visible = False
      
    # Check email is valid:
    if email is '':
      self.email_error_label.visible = True
      empty_field_bool = True
    else:
      self.email_error_label.visible = False
      
    # Check if a gin is selected:
    if gin_name is None:
      self.gin_error_label.visible = True
      empty_field_bool = True
    else:
      self.gin_error_label.visible = False

    # Check if a role is selected:
    if role is None:
      self.role_error_label.visible = True
      empty_field_bool = True
    else:
      self.role_error_label.visible = False

    # If user left a field blank, return:
    if empty_field_bool:
      return True
    return False
    

  def request_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Get fields:
    firstname = self.firstName_tb.text
    lastname = self.lastName_tb.text
    email = self.email_tb.text
    gin_name = self.gin_drop_down.selected_value
    role = self.role_drop_down.selected_value
    
    empty_fields = self.check_fields_for_error(firstname,
                                                lastname,
                                                email,
                                                gin_name,
                                                role)
    if empty_fields:
      print("returning...")
      return
    
    # Call uplink function to enter user data:
    user_data = json.dumps({
      'firstname': firstname,
      'lastname': lastname,
      'email': email,
      'gin_name': gin_name,
      'requested_role': role
    })

    # Call uplink function:
    returned_data = anvil.server.call("user_request_access", user_data)


    if returned_data:
      noti = Notification(f"Your request for gin access has been successfully received.")
      noti.show()
      self.raise_event("x-close-alert")
      # Refresh the users browser:
      # window.location.reload()
    else:
      # User was not created successfully:
      alert("Unable to request access. Please contact an Admin.")
      # error_code = returned_data['error_code']
        
        
    
    
    

