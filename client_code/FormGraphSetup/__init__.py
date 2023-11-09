from ._anvil_designer import FormGraphSetupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from HashRouting import routing
import json
from .. import Globals


@routing.route('graph-setup', full_width_row=True)
class FormGraphSetup(FormGraphSetupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.email = Globals.user['email']
    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin']
    self.gin_location_dict = Globals.user['gin_location']
    self.num_gin_stands_dict = Globals.user['num_gin_stands']
    self.gins_accessible = Globals.user['gins_accessible']

    self.drop_down_gin_name.items = self.gins_accessible
    
  def update_graph_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Get drop-down values:
    graph_type = self.drop_down_graph_type.selected_value
    graph_scale = self.drop_down_graph_scale.selected_value
    gin_name = self.drop_down_gin_name.selected_value
    
    # Get number of gin stands at selected gin:
    num_gin_stands = self.num_gin_stands_dict[gin_name]

    # format values for database:
    formated_args = format_values(graph_type, graph_scale)

    # graph_type = formated_args[0]
    # graph_scale = formated_args[1]
    
    graph_settings = json.dumps({
      'email': self.email,
      'gin_name': gin_name,
      'num_gin_stands': num_gin_stands,
      'graph-type': graph_type,
      'graph-scale': graph_scale
    })

    # Update values in database:
    update_bool = anvil.server.call('update_chart_settings', graph_settings)

    if update_bool:
      # Route user to chart page:
      routing.set_url_hash('graph-viewer')
      routing.reload_page() # This forces __init__ in FormTrendGraphs to be called on each change in graph settings
    else:
      alert("Error updating chart settings.\nPlease Contact an Admin")


def format_values(*args):
  """replace all whitespace with - in *args """
  formated_args = []
  for arg in args:
    # print(f"before formatting: {arg}")
    formated_arg = arg.replace(' ','').lower()
    formated_args.append(formated_arg)
    # print(f"After formatting: {formated_arg}")

  return formated_args
    
