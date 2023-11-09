from ._anvil_designer import MainRouterTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from time import sleep
import random
import json
from HashRouting import routing

# Import all our forms for routing
from ..FormCamControls import FormCamControls
from ..FormTrendGraphs import FormTrendGraphs
from ..FormNodeConns import FormNodeConns
from ..FormPicCapControls import FormPicCapControls
from ..FormGinMonitoring import FormGinMonitoring
from ..FormHomePage import FormHomePage
from ..FormRoutingError import FormRoutingError
from ..FormGraphSetup import FormGraphSetup
from ..FormSettings import FormSettings

# Import our modules:
from .. import MainModule
from .. import Globals

@routing.main_router
class MainRouter(MainRouterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Get user info:
    self.username = Globals.user['username']
    self.email = Globals.user['email']
    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin']
    self.gins_accessible = Globals.user['gins_accessible']

    # Get the users permisible urls
    self.role_permissions = Globals.role_permissions[self.role]
          
    # Hide links that user doesn't have access to based on role:
    if(self.role.lower() == "coordinator" or self.role.lower() == "geo-coordinator" or self.role.lower() == "manager"):
      self.link_camera_controls.visible = False
      self.link_node_conns.visible = False
      self.link_pic_capture_controls.visible = False
    elif(self.role.lower() == "technician"):
      self.link_camera_controls.visible = False
      self.link_pic_capture_controls.visible = False
      self.link_gin_monitoring.visible = False
      self.graphs_menu_link.visible = False
      

    # Form links:
    self.link_camera_controls.tag.url_hash = 'camera-controls'
    self.link_node_conns.tag.url_hash = 'node-connections'
    self.link_pic_capture_controls.tag.url_hash = 'picture-capture-controls'
    self.link_gin_monitoring.tag.url_hash = 'gin-monitor'
    self.link_graph_setup.tag.url_hash = 'graph-setup'
    self.link_graph_viewer.tag.url_hash = 'graph-viewer'
    self.link_home_page.tag.url_hash = ''
    self.link_settings_page.tag.url_hash = 'settings'
    self.links = [self.link_camera_controls, 
                  self.link_node_conns,
                  self.link_graph_viewer,
                  self.link_pic_capture_controls,
                  self.link_gin_monitoring,
                  self.link_home_page,
                  self.link_settings_page,
                  self.link_graph_setup]

  
    set_default_error_handling(self.error_handler)


  def nav_link_click(self, **event_args):
    """This method is called when a navigation link is clicked"""
    # Get the url hash the user just clicked on:
    url_hash = event_args['sender'].tag.url_hash
    # Check if user has permission to visit the page:
    if url_hash in self.role_permissions:
        # Set route & Allow user to visit the page:
        routing.set_url_hash(url_hash)
    else:
        # user can't visit that page, so redirect them to the home page:
        routing.set_url_hash('')


  
  def on_navigation(self, **nav_args):
    # this method is called whenever routing navigates to a new url
    selected_url_hash = nav_args['url_hash']
    for link in self.links:
      if link.tag.url_hash == selected_url_hash:
        link.role = 'selected' 
      else:
        link.role = ''


  def on_form_load(self, **nav_args):
    # this method is called whenever the routing module has loaded a form into the content_panel
    selected_url_hash = nav_args['url_hash']
    
    # Make sure user has permission to visit form:
    if not Globals.check_user_form_privleges(selected_url_hash, self.role_permissions):
      routing.set_url_hash('', replace_current_url=True)
      routing.reload_page() # This forces __init__ in FormTrendGraphs to be called on each change in graph settings

  def error_handler(self, err):
    # alert(str(err), title="An error has occurred")
    # TODO: Maybe instead of an alert -> print error message on a new error_page
    pass

  def graphs_menu_link_click(self, **event_args):
    """This method is called when the link is clicked"""

    if(self.column_panel_2.visible):
      self.graphs_menu_link.icon = "fa:angle-right"
      self.column_panel_2.visible = False
    else:
      self.graphs_menu_link.icon = "fa:angle-down"
      self.column_panel_2.visible = True

  



      

    




