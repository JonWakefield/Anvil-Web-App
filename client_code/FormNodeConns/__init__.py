from ._anvil_designer import FormNodeConnsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from HashRouting import routing
import json
from .. import Globals
import copy

@routing.route('node-connections', full_width_row=False)
class FormNodeConns(FormNodeConnsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin']
    self.gins_accessible = copy.copy(Globals.user['gins_accessible'])
    self.all_num_gin_stands_dict = Globals.user['num_gin_stands']

    # Get gin specific # gin stands
    self.num_gin_stands = self.all_num_gin_stands_dict[self.gin_name]
    
    self.gin_numbers_list = [str(i) for i in range(1, self.num_gin_stands + 1)]

    self.gin_stand_drop_down.items = self.gin_numbers_list

    # Setup list of possible gins to add-node to:
    self.gin_name_drop_down.items = self.gins_accessible
    self.gin_name_drop_down.selected_value = self.gin_name

    # IDEA: Check if user has access to all gins: Reason: Need way to determine "All Gins" and unassigned in gin_search_drop_down.items
    result_bool = anvil.server.call("check_if_all_gins_accessible", json.dumps(self.gins_accessible))

    # Setup drop_down items 
    if result_bool:
      self.gins_accessible.append("All Gins")
      self.gins_accessible.append("Unassigned")
      self.gin_search_drop_down.items = self.gins_accessible
    else:     
      self.gin_search_drop_down.items = self.gins_accessible
      
    self.gin_search_drop_down.selected_value = self.gin_name

    # Get connected nodes
    self.repeating_panel_node_conns.items = anvil.server.call("check_nodes_connected", self.gin_name)
    self.nodeConns_data_grid.rows_per_page = 10

    # Any code you write here will run before the form opens.
  

  def get_nodes_connected_timer_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    # get gin search value (if any):
    search_value = self.gin_search_drop_down.selected_value
    
    with anvil.server.no_loading_indicator:
      self.repeating_panel_node_conns.items = anvil.server.call("check_nodes_connected", search_value)

  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # get gin search value (if any):
    search_value = self.gin_search_drop_down.selected_value
    self.repeating_panel_node_conns.items = anvil.server.call("check_nodes_connected", search_value)

  
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
    
  
  def add_node_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #Check if entered port num is valid:
    port_num = self.port_num_tb.text
    valid_port = self.check_valid_port_num(port_num)
    if not valid_port:
      return

    selected_gin = self.gin_name_drop_down.selected_value
    selected_stand_num = self.gin_stand_drop_down.selected_value

    if selected_gin is None:
      noti = Notification(f"Please select a Valid Gin")
      noti.show()
      return
    if selected_stand_num is None:
      noti = Notification(f"Please select a Valid Gin Stand Number")
      noti.show()
      return
      


    # Check if port_num exists in database
    existing_node_info = anvil.server.call("check_for_node_entry", str(port_num))

    if existing_node_info is not None:
      # unpack retrieved node info:
      gin_name = existing_node_info.get('gin_name')
      gin_stand_num = existing_node_info.get('ginstand_num')
      c = confirm(f"Entry already exists for camera-node port # {port_num}\nGin Name: {gin_name}, Gin stand Num: {gin_stand_num}\nWould you like to replace the current entry?")
      if c:
        # Add new params for node to database:   
        # Get user entered node params:
        node_params = json.dumps({
              'gin_stand': self.gin_name_drop_down.selected_value,
              'gin_stand_num': self.gin_stand_drop_down.selected_value,
              'port_num': port_num,
        })
        
        returned_value = anvil.server.call("update_node_connection", node_params)
        
        if(returned_value):
          noti = Notification(f"Camera Node successfully Updated")
          # refresh the table
          self.search_button_click()
          noti.show()
        else:
          alert(f"Unable to update value in database\n{returned_value}")
    else:
      print("could not find an existing node!")
      # Still add...
      # Get user entered node params:
      node_params = json.dumps({
            'gin_stand': self.gin_name_drop_down.selected_value,
            'gin_stand_num': self.gin_stand_drop_down.selected_value,
            'port_num': port_num,
      })
      # Add new params for node to database:        
      returned_value = anvil.server.call("add_node_connection", node_params)
      
      if(returned_value):
        noti = Notification(f"Camera Node successfully added")
        # refresh the table
        self.search_button_click()
        noti.show()
      else:
        alert(f"Unable to add value to database\n{returned_value}")

    self.port_num_tb.text = ""
  

  def delete_port_num(self, **event_args):
    """This method is called when the button is clicked"""
    # Get user selected row:
    port_to_delete = self.delete_port_num_tb.text
    # Get the data panel rows:
    data_panel_rows = self.repeating_panel_node_conns.get_components()

    # Check if entered port # is valid:
    valid_port = self.check_valid_port_num(port_to_delete)
    if not valid_port:
      return

    # check that the entered port num exists:
    for row_panel in data_panel_rows:
      row_content = row_panel.get_components()
      rows_port_num = row_content[0].text
      if (rows_port_num == port_to_delete):
        print("port num found")
        # call uplink function here
        node_params = json.dumps({
          'port_num': row_content[0].text,
          'gin_name': row_content[1].text,
          'gin_stand_num': row_content[2].text,
        })
        removed_row_bool = anvil.server.call("remove_node_connection", node_params)
        if(removed_row_bool):
          noti = Notification(f"Camera Node successfully removed")
          # Refresh the table
          self.search_button_click()
          noti.show()
        else:
          alert("Unable to remove camera node")
        return

    alert(f"Unable to find entry for entered port num: {port_to_delete}\nPlease re-check entered number")

  def gin_name_drop_down_change(self, **event_args):
    """When gin name selected is changed -> update possible gin_stand #s based on gin"""

    try:
      # Get new selected gin name
      gin_name = self.gin_name_drop_down.selected_value
  
      # Get gin specific # gin stands
      num_gin_stands = self.all_num_gin_stands_dict[gin_name]
      
      self.gin_numbers_list = [str(i) for i in range(1, num_gin_stands + 1)]

      # Update possible gin stand #s
      self.gin_stand_drop_down.items = self.gin_numbers_list
    except (KeyError) as err:
      return
      







    

      


