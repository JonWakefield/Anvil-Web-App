# Form handles routing errors when user navigates to page that doesn't exist
# example: https://pides-node-viewer.anvil.app/#page_doesnt_exist
from ._anvil_designer import FormRoutingErrorTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from HashRouting import routing

@routing.error_form
class FormRoutingError(FormRoutingErrorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
