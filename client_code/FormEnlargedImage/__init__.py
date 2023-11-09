from ._anvil_designer import FormEnlargedImageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import anvil.image

class FormEnlargedImage(FormEnlargedImageTemplate):
  def __init__(self, image, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

    self.image_comp.source = image

    