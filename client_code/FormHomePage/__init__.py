from ._anvil_designer import FormHomePageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from HashRouting import routing
from .. import Globals
from anvil.js import window
from datetime import datetime
import calendar

@routing.route('', full_width_row=True) 
class FormHomePage(FormHomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.username = Globals.user['username']
    self.email = Globals.user['email']
    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin']
    self.gin_location = Globals.user['gin_location']
    self.num_gin_stands = Globals.user['num_gin_stands']

    self.active_gin_location = self.gin_location[self.gin_name]
    self.active_num_gin_stands = self.num_gin_stands[self.gin_name]

    # Get the current time
    current_time = datetime.now()

    # Extract the day and month
    current_day = current_time.day
    current_month = current_time.month
    month = month_number_to_word(current_month)
    
    # Format the current time in 12-hour format (AM/PM)
    formatted_time = current_time.strftime("%I:%M %p")

    # time = formatted_time + ", " + str(month) + " " + str(current_day)
    time = str(month) + " " + str(current_day) + ", " + formatted_time

    self.welcome_label.text = f"Welcome, {self.username} to VISN Viewer!"
    self.date_label.text = f" {time}"
    self.role_label.text = f" {self.role}"
    self.gin_access_label.text = f" {self.gin_name}"
    self.location_label.text = f" {self.active_gin_location}"
    self.num_stands_label.text = f" {self.active_num_gin_stands}"



# Define a function to convert month number to word
def month_number_to_word(month_number):
    if 1 <= month_number <= 12:
        return calendar.month_name[month_number]
    else:
        return "Invalid month number"
      

