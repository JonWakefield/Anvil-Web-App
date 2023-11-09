from ._anvil_designer import FormLandingPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..SignInModal import SignInModal
from ..RequestAccessModal import RequestAccessModal

class FormLandingPage(FormLandingPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def log_in_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    sign_in_modal = SignInModal()
    alert(
      content=sign_in_modal,
      title="User Login",
      large=False,
      buttons=[])
      # role="login")
      # buttons=["Log In"])

  def request_access_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    request_acc_modal = RequestAccessModal()
    alert(
      content=request_acc_modal,
      title="Acess Request",
      large=True,
      buttons=[])
      # role="login")
      # buttons=["Log In"])


