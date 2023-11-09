from ._anvil_designer import FormCamControlsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import json
from .. import Globals

from HashRouting import routing

# routing decoration
@routing.route('camera-controls')
class FormCamControls(FormCamControlsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.username = Globals.user['username']
    self.role = Globals.user['role']
    self.email = Globals.user['email']
    self.gin_name = Globals.user['active_gin']
    self.gin_location = Globals.user['gin_location']
    self.num_gin_stands = Globals.user['num_gin_stands']
    self.gins_accessible = Globals.user['gins_accessible']

    self.active_gin_location = self.gin_location[self.gin_name]
    self.active_num_gin_stands = self.num_gin_stands[self.gin_name]

    # Keep track if user is connected to an active node
    self.connected_to_node = False


  def check_valid_port_num(self, port_num) -> bool:
    """ Checks to ensure entered port number is valid"""
    # Make sure entered port is valid:
    try:
      if((len(str(port_num)) != 4) or (isinstance(port_num, float))):
        alert("Invalid Port Number...")
        return False
    except (TypeError) as err:
      alert("Please enter a port # first")
      return False
    return True
    
  def display_color_balance_setting(self, color_balance: int):
    """Select which radio button to have selcted based no color_balance value"""
    color_balance = str(color_balance)
    
    # No color balance value found in database:
    if(color_balance == str(0)):
      self.rb_colbal_2800.selected = False
      self.rb_colbal_5000.selected = False
      self.rb_colbal_6500.selected = False
      self.rb_colbal_custom.selected = False
      
    elif(color_balance == self.rb_colbal_2800.value):
      self.rb_colbal_2800.selected = True
    elif(color_balance == self.rb_colbal_5000.value):
      self.rb_colbal_5000.selected = True
    elif(color_balance == self.rb_colbal_6500.value):
      self.rb_colbal_6500.selected = True
    else:
      self.rb_colbal_custom.selected = True
    
  def node_connect_button_click(self, **event_args):
    """Connect to node"""

    self.port_num = self.port_num_tb.text

    # Check if entered port # is valid:
    valid_port = self.check_valid_port_num(self.port_num)
    if not valid_port:
      return

    connect_to_node_data = json.dumps({
      'email': self.email,
      'gins_accessible': self.gins_accessible,
      'port_num': self.port_num
    })

    returned_data = anvil.server.call("connect_to_node", connect_to_node_data)

    returned_dict = json.loads(returned_data)
    
    found_node = returned_dict['found_node']

    if found_node:
      # Keep track if user is connected to an active node
      self.connected_to_node = True      
      # Unpack returned data dict:
      self.node_gin_name = returned_dict['gin_name']
      self.node_gin_stand_num = returned_dict['gin_stand_num']
      self.node_position = returned_dict['node_position']
      self.node_gin_location = returned_dict['gin_location']

      # Update text boxes:
      self.gin_name_tb.text = self.node_gin_name
      self.gin_stand_num_tb.text = self.node_gin_stand_num
      self.node_position_tb.text = self.node_position
      self.gin_location_tb.text = self.node_gin_location[0]

      # Unpack pre-configured camera settings
      camera_settings = returned_dict['camera_settings']

      # If no camera settings were found, inform user:
      if not camera_settings:
        noti = Notification(f"Unable to find pre-configured camera settings for node {self.port_num}")
        noti.show()

        # Clear all text box fields:
        self.display_color_balance_setting(color_balance=0)
        self.text_box_gain.text = ''
        self.text_box_exposure.text = ''
        self.text_box_blob_size.text = ''
        self.text_box_roi_x_min.text = ''
        self.text_box_roi_x_max.text = ''
        self.text_box_roi_y_min.text = ''
        self.text_box_roi_y_max.text = ''
        
      else:
        # Unpack dict & load previously configured camera settings onto the form:
        color_balance = camera_settings['color_balance']
        gain = camera_settings['gain']
        exposure = camera_settings['exposure']
        min_blobsize = camera_settings['min_blobsize']
        roi_startx = camera_settings['roi_startx']
        roi_stopx = camera_settings['roi_stopx']
        roi_starty = camera_settings['roi_starty']
        roi_stopy = camera_settings['roi_stopy']
        
        # Populate form:
        self.display_color_balance_setting(color_balance)
        self.text_box_gain.text = gain
        self.text_box_exposure.text = exposure
        self.text_box_blob_size.text = min_blobsize
        self.text_box_roi_x_min.text = roi_startx
        self.text_box_roi_x_max.text = roi_stopx
        self.text_box_roi_y_min.text = roi_starty
        self.text_box_roi_y_max.text = roi_stopy
        
      
    else:
      # Keep track if user is connected to an active node
      self.connected_to_node = False
      # Could not find the user entered node #
      try:
        found_issue = returned_dict['err_code']
      except (KeyError) as err:
        alert("Error in connecting to node. View error_log.txt for more info")
        return
      if found_issue == 1:
        # Node could not be found because the port num does not exist in database
        noti = Notification(f"Unable to find entered port num in database")
        # Update text boxes:
        self.gin_name_tb.text = "-"
        self.gin_stand_num_tb.text = "-"
        self.node_position_tb.text = "-"
        self.gin_location_tb.text = "-"
        noti.show()
      elif found_issue == 2:
        # Node info could not be returned because user does not have access to gin:
        noti = Notification(f"Unable to return node info, user does not have access.\n Please contact an admin")
        noti.show()
  
  def get_selected_radio_button(self):
    """ Get the selected color balance radio button"""

    if self.rb_colbal_2800.selected:
      return self.rb_colbal_2800.value
    elif self.rb_colbal_5000.selected:
      return self.rb_colbal_5000.value
    elif self.rb_colbal_6500.selected:
      return self.rb_colbal_6500.value
    else:
      # if the custom radio button is selected:
      color_balance_white = self.text_box_cb_white.text
      color_balance_red = self.text_box_cb_red.text
      return (color_balance_white, color_balance_red)

  def radio_but_custom_selected(self, **event_args):
    """Method is called when the custom radio button is selected"""
    self.column_panel_4.role = ""
    self.label_cb_help.visible = True
    self.column_panel_10.visible = True
    self.column_panel_11.visible = True

  def radio_but_noncustom_selected(self, **event_args):
    """Method is called when 1 of the three non-custom radio buttons is selected"""
    self.column_panel_4.role = "bottom-border"
    self.label_cb_help.visible = False
    self.column_panel_10.visible = False
    self.column_panel_11.visible = False
    
  def update_colorbal_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    # First check and make sure user is connected to an active node:
    if not self.connected_to_node:
      alert("Please connect to a node first")
      return False

    # Get user entered colorbalance data:
    color_balance = self.get_selected_radio_button()

    print(f"Color balance value: {color_balance}")

    node_color_bal_data = json.dumps({
      'email': self.email,
      'port_num': self.port_num,
      'gin_name': self.node_gin_name,
      'gin_stand_num': self.node_gin_stand_num,
      'settings_code': 100,
      'color_balance': color_balance
    })

    returned_data = anvil.server.call("modify_node_camera_settings", node_color_bal_data)

    # Convert from json to dict
    returned_dict = json.loads(returned_data)

    # Get our bools to indicate if successful update
    color_updated_bool = returned_dict['color_bal_update']

    if color_updated_bool:
      noti = Notification(f"Color Balance successfully updated")
      noti.show()
    else:
      alert("Error occurred. Unable to update color balance.\n Error stored in error_log.txt")
      
  def convert_exp_units(self, exposure, exp_units):
    """
    Convert microseconds (μs) to milliseconds (ms).

    Args:
        exposure (float or int): Value in microseconds.
        exp_units possible units

    Returns:
        float: Equivalent value in milliseconds.
    """
    if exp_units == "ms":
      return exposure
    else:
      return exposure / 1000.0 

  def check_valid_gain_input(self, gain_user_input):
    ''' Check to see if the user inputted value in the "gain" text box is valid
        Valid IF input is INTEGER BETWEEN 1 & 100
    '''

    if ((isinstance(gain_user_input, int)) and (gain_user_input > 0 and gain_user_input <= 100)):
      return True
    else:
      alert(f"Unable to write to database. Check Gain value is between 1-100.\nValue Entered: {gain_user_input}")
      return False

  def check_valid_exposure_input(self, exposure_user_input):
    ''' Check to ensure user inputted value for gain text box is valid.
        Valid IF integer value between 0 - 500
    '''
   
    # Now do validity check in units milli
    if (exposure_user_input >= 200 and exposure_user_input <= 1000):
      return True
    else:
      alert(f"Unable to write to database. Check Exposure value is between 200-1000 ms.\nValue Entered: {exposure_user_input} ms")
      return False

  def update_cam_settings_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    # First check and make sure user is connected to an active node:
    if not self.connected_to_node:
      alert("Please connect to a node first")
      return False

    # Get user entered settings data:
    gain = self.text_box_gain.text
    exposure = self.text_box_exposure.text
    exp_units = self.drop_down_exposure_units.selected_value

    # Convert exposure to base unit of ms:
    exposure = self.convert_exp_units(exposure, exp_units)

    # Check valid values entered:
    if not self.check_valid_gain_input(gain):
      return
    if not self.check_valid_exposure_input(exposure):
      return

    # Package everything into a dict:
    node_cam_settings_data = json.dumps({
      'email': self.email,
      'port_num': self.port_num,
      'gin_name': self.node_gin_name,
      'gin_stand_num': self.node_gin_stand_num,
      'settings_code': 200,
      'exposure': exposure,
      'gain': gain
    })

    returned_data = anvil.server.call("modify_node_camera_settings", node_cam_settings_data)

    # Convert from json to dict
    returned_dict = json.loads(returned_data)

    # Try to get our bools (if user did not enter value, exception will be raised)
    try:
      gain_updated_bool = returned_dict['gain_update']
      if gain_updated_bool:
        noti = Notification(f"Gain value successfully updated")
        noti.show()
      else:
        # Error occured when trying to update gain:
        alert("Error occurred. Unable to update gain.\n Error stored in error_log.txt")
        
    except(KeyError) as err:
      # occurs when user did not enter value to update gain
      # This is perfectly fine: A user may only want to update exposure
      pass

    # Try to get our bools (if user did not enter value, exception will be raised)
    try:
      exposure_updated_bool = returned_dict['exposure_update']
      if exposure_updated_bool:
        noti = Notification(f"Exposure value successfully updated")
        noti.show()
      else:
        # Error occured when trying to update exposure:
        alert("Error occurred. Unable to update exposure.\n Error stored in error_log.txt")
  
    except(KeyError) as err:
      # occurs when user did not enter value to update exposure
      # This is perfectly fine: A user may only want to update gain
      pass


  def check_valid_blobsize_input(self, blobsize_user_input):
    ''' Check to ensuer user inputted value for blob size is valid.
        Valid IF integer value between 1 - 100  
    '''
    if ((isinstance(blobsize_user_input, int)) and (blobsize_user_input >= 100 and blobsize_user_input <= 10000)):
      return True
    else:
      alert(f"Unable to write to database. Check Min. blob size value is between 1-100.\nValue Entered: {blobsize_user_input}")
      return False

  def check_roi_values(self, *roi_args) -> bool:
    """
        Function Description:
          - Checks if the user entered values for startx, stopx, starty, stopy, are valid
            Valid Range: (UN_KNOWN)

        Input Args:
          - *roi_args -> user entred values for start/stop x/y (4 total)

        Output Args:
          - BOOL: If all arguments are not None -> return true, else return False
    """
    for arg in roi_args:
      # If an arg is none (aka user left field blank -> return False)
      if arg is None:
        alert("Please enter a value for each ROI region.")
        return False
    return True
   
  def update_roi_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    # First check and make sure user is connected to an active node:
    if not self.connected_to_node:
      alert("Please connect to a node first")
      return False

    # Get user entered settings data:
    min_blobsize = self.text_box_blob_size.text
    
    # Check to make sure entered min_blobsize is valid:
    if not self.check_valid_blobsize_input(min_blobsize):
      return
      
    # Get ROI values:
    roi_startx = self.text_box_roi_x_min.text
    roi_stopx = self.text_box_roi_x_max.text
    roi_starty = self.text_box_roi_y_min.text
    roi_stopy = self.text_box_roi_y_max.text
    if not self.check_roi_values(roi_startx, roi_stopx, roi_starty, roi_stopy):
      return
    

    # Store everything in a python dict:
    node_roi_settings = json.dumps({
      'email': self.email,
      'port_num': self.port_num,
      'gin_name': self.node_gin_name,
      'gin_stand_num': self.node_gin_stand_num,
      'settings_code': 300,
      'min_blobsize': min_blobsize,
      'roi_startx': roi_startx,
      'roi_stopx': roi_stopx,
      'roi_starty': roi_starty,
      'roi_stopy': roi_stopy
    })

    returned_data = anvil.server.call("modify_node_camera_settings", node_roi_settings)

    # Convert from json to dict
    returned_dict = json.loads(returned_data)

    # Get our bools to indicate if successful update
    blobsize_updated_bool = returned_dict['blobsize_update']
    roi_updated_bool = returned_dict['roi_update']

    if blobsize_updated_bool:
      noti = Notification(f"Min. BlobSize successfully updated")
      noti.show()
    else:
      alert("Error occurred. Unable to update blobsize.\n Error stored in error_log.txt")
      
    if roi_updated_bool:
      noti = Notification(f"ROI values successfully updated")
      noti.show()
    else:
      alert("Error occurred. Unable to update ROI.\n Error stored in error_log.txt")

    def form_show(self, **event_args):
      """This method is called when the column panel is shown on the screen"""
      alert("form show!!")
      # silent call to the server on form show
      
      

     
