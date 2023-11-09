from ._anvil_designer import FormGinMonitoringTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from HashRouting import routing
import json
import anvil.image
from math import ceil
import random
from anvil.js import window
from .. import Globals
from ..FormEnlargedImage import FormEnlargedImage

@routing.route('gin-monitor', full_width_row=True)
class FormGinMonitoring(FormGinMonitoringTemplate):
  def __init__(self, data=None ,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Set timer interval length
    self.timer_get_image_ages.interval = 10 #In production change to 30-60secs   

    # Unpack user info:
    self.username = Globals.user['username']
    self.role = Globals.user['role']
    self.gin_name = Globals.user['active_gin'] 
    self.all_gin_stands = Globals.user['num_gin_stands']

    # Get gin specific # gin stands
    self.num_gin_stands = self.all_gin_stands[self.gin_name]

    self.gin_label.text = f"{self.gin_name} Gin Activity Monitor"

    # Get devices inner height and width:
    deviceHeight = window.innerHeight
    deviceWidth = window.innerWidth


    # Change the size of the images displayed depending on device size:
    if(deviceWidth >= 1620):
      self.imageSize = (480,360)
      imageWidth = 480
      imageHeight = 360
    else:
      self.imageSize = (320,240)
      imageWidth = 320
      imageHeight = 240
    

    # Keep track of our imageComponents' (we will need this when we update the image inside of the ImageComponent):
    self.imageComp_list = []
    self.image_list = []
    # Keep track of our labels:
    self.gin_label_list = []

    # Call uplink function to get imagesAge:
    data_ages = json.dumps({
          'gin_name': self.gin_name,
          'num_gin_stands': self.num_gin_stands
    })
  
    # call uplink function to get image ages:
    try:
      returned_data = anvil.server.call("get_image_ages", data_ages)
    except (Exception) as err:
      alert("Could not connect to Uplink\nRefresh to Try again")
      print(err)
      return

    # unpack json:
    returned_data_dict = json.loads(returned_data)
      
    # Unpack retrieved data:
    img_time_taken = returned_data_dict['img_time_taken']
    file_paths_list = returned_data_dict['file_paths']
    age_list = returned_data_dict['image_ages']
    HID_status_list = returned_data_dict['HID_status']
    
    # Setup prev_image_ages list to keep track of changes in data-table
    self.prev_image_ages = img_time_taken

    self.prev_image_ages = [None] * self.num_gin_stands
    
    # Loop through and retrieve each image, and setup each image component
    for i in range(self.num_gin_stands):

      # Setup data for image retrieval
      data_image = json.dumps({
          'file_path': file_paths_list[i],
          'image_size': self.imageSize,
      })
      # Retrieve an image:
      returned_img_data = anvil.server.call("get_plastic_image", data_image)
     
      # Unpack retrieved data:
      plastic_image = returned_img_data['image']
      # Get HID Status for ith image:
      HID_status = HID_status_list[i]

      
      # if i % 3 -> create a new row:
      # NOTE: this needs to be changed (# of images per row should be based on screen size)
      if (i % 3 == 0):
        # Each ROW of images is contained inside of a flow panel
        row_flow_panel = FlowPanel(align="center", spacing="tiny")

      # Each image is contained inside of a column panel:
      img_panel = ColumnPanel(width=imageWidth)
      
      # Create an Anvil Image Component to house retrieved image:
      self.imageComp = Image(height=imageHeight, display_mode="original_size", source=plastic_image)
      # self.imageComp.add_event_handler('mouse_up', self.image_click_event)

      # Determine color of border:
      self.update_image_border(self.imageComp, int(age_list[i]))

      # Store images in list:
      self.image_list.append(plastic_image)

      # Store Image Components in list:
      self.imageComp_list.append(self.imageComp)

      # Determine which label to apply based on HID status (T/F)
      if HID_status:
        gin_label = Label(text=f"Gin Stand {i+1}: Age {age_list[i]} Mins\tHID:", icon="fa:check", icon_align="right", align="left", font="Q", font_size=17, spacing_above="None", spacing_below="None")
      else:
        gin_label = Label(text=f"Gin Stand {i+1}: Age {age_list[i]} Mins\tHID:", icon="fa:times", icon_align="right", align="left", font="Q", font_size=17, spacing_above="None", spacing_below="None")

      # Store gin_label:
      self.gin_label_list.append(gin_label)

      # Create a spacer component to add extra spacing:
      col_spacer = Spacer(width=40)

      # Put Anvil Image Component into image column panel:
      img_panel.add_component(self.imageComp)

      # Put label into image column panel:
      img_panel.add_component(gin_label)

      # Add column panel to the rows flow panel:
      row_flow_panel.add_component(img_panel)

      # Add some spacing between images:
      row_flow_panel.add_component(col_spacer)

      # Want to add row when i ='s 2, 5, 8 ??????
      if ((i == 2) or (i == 5) or (i == 8) or (i == (self.num_gin_stands-1))):
        # Every n'th image -> add row_panel to gin_monitor_panel, then on next loop create new row_panel
        self.gin_monitor_panel.add_component(row_flow_panel, full_width_row=True)

  def timer_get_image_ages_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""

    print("Getting image times...")

    # supress the spinning wheel:
    with anvil.server.no_loading_indicator:
      
      # Call uplink function to get image ages:
      data_ages = json.dumps({
          'gin_name': self.gin_name,
          'num_gin_stands': self.num_gin_stands
      })
  
      # call uplink function to get image ages:
      returned_data = anvil.server.call("get_image_ages", data_ages)

      # unpack json
      returned_data_dict = json.loads(returned_data)
      
      # Unpack retrieved data:
      img_time_taken_list = returned_data_dict['img_time_taken']
      file_paths_list = returned_data_dict['file_paths']
      age_list = returned_data_dict['image_ages']
      HID_status_list = returned_data_dict['HID_status']
      
      print("comparing new ages to prev ages...")
      for i in range(self.num_gin_stands):
        gin_num = i+1
        
        # Check if the new imageAge is different than the prev_imageAge:
        if(self.prev_image_ages[i] != img_time_taken_list[i]):
          print("New image age different than prev. age... retrieving new image")

          # If different -> Grab new image for gin stand i
          self.getPlasticImage(gin_num, age_list[i], file_paths_list[i], HID_status_list[i])
          # Update prev image list with new image
          self.prev_image_ages[i] = img_time_taken_list[i]
        else:
          # Update label and image border:
          label = self.gin_label_list[i]
          imageComp = self.imageComp_list[i]
          label.text = f" Gin Stand {gin_num}: Age {age_list[i]} Minutes\tHID:"
          gin_age = int(age_list[i])
          # Update the border color for each gin:
          self.update_image_border(imageComp, gin_age)
          

  def getPlasticImage(self, gin_stand_num, image_age, file_path, HID_status, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""

    print("Getting a plastic image:")
    # supress the spinning wheel:
    with anvil.server.no_loading_indicator:
      
      # Call uplink function to retrieve new image:
      data_image = json.dumps({
          'file_path': file_path,
          'image_size': self.imageSize,
      })
      
      # Retrieve image:
      returned_data_dict = anvil.server.call("get_plastic_image", data_image)

      # Update the information for the returned gin stand data:
      image = returned_data_dict['image']  

      # Get the ginStands corresponding image & label component:
      imageComp = self.imageComp_list[int(gin_stand_num)-1]
      label = self.gin_label_list[int(gin_stand_num)-1]
      
      # Update our stored image list:
      self.image_list[int(gin_stand_num)-1] = image
      
      # display the retrieved image:
      imageComp.source = image
      
      # Check on HID status:
      if HID_status:
        label.text = f"Gin Stand {gin_stand_num}: Age {image_age} Mins\t\tHID:"
        label.icon = "fa:check"
        # label.foreground = "blue"
      else:
        label.text = f"Gin Stand {gin_stand_num}: Age {image_age} Mins\t\tHID:"
        label.icon = "fa:times"
        # label.foreground = "red"
  
      self.update_image_border(imageComp, int(image_age))
  

  def update_image_border(self, imageComp, age):
    """Update the color of the border around the Image Component depending on time"""

    # For production Times:
    if (age <= 5):
        imageComp.role = "gin-monitor-red"
    elif((age > 5) and (age <= 20)):
        imageComp.role = "gin-monitor-yellow"
    else:
        imageComp.role = "gin-monitor-green"

    # # For Development Times:
    # if (age <= 2):
    #     imageComp.role = "gin-monitor-red"
    # elif((age > 2) and (age <= 4)):
    #     imageComp.role = "gin-monitor-yellow"
    # else:
    #     imageComp.role = "gin-monitor-green"

  def image_click_event(self, **event_args):
    """ Function is called when an image component is clicked"""

    EnlargedImageForm = FormEnlargedImage(image=self.image_list[1])

    alert(
      content=EnlargedImageForm,
      title="Enlarged Plastic Image",
      large=True
    )

  # DEV FUNCTION:
  def _simulate_entries_timer_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    print("Simulating table entries...")
    anvil.server.call("_simulate_events", self.gin_name)




    

    
    