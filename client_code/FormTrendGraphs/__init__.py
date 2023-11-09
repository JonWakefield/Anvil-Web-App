from ._anvil_designer import FormTrendGraphsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.media
from HashRouting import routing
import json
from .. import Globals

@routing.route('graph-viewer', full_width_row=True)
class FormTrendGraphs(FormTrendGraphsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.email = Globals.user['email']
    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin']
    self.gin_location_dict = Globals.user['gin_location']
    self.num_gin_stands_dict = Globals.user['num_gin_stands']

    self.active_gin_location = self.gin_location_dict[self.gin_name]
    self.active_num_gin_stands = self.num_gin_stands_dict[self.gin_name]

    retrieve_chart_data = json.dumps({
      'email': self.email,
      'gin_name': self.gin_name,
      'num_gin_stands': self.active_num_gin_stands,
    })

    # Retrieve a chart to display:
    retrieved_chart = anvil.server.call("retrieve_chart", retrieve_chart_data)
    if(retrieved_chart is False):
      self.no_data_label.visible = True
      self.chart_image.visible = False
    else:
      self.chart_image.source = retrieved_chart
      self.no_data_label.visible = False

  
  def download_chart(self, **event_args):
    """This method is called when the button is clicked"""
    
    orig =  self.chart_image.source
    new = anvil.BlobMedia('image/jpg',orig.get_bytes(),name=f"GinBarPlot.jpg")
    # anvil.media.download(new)
    anvil.media.download(self.chart_image.source)

