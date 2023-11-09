from ._anvil_designer import FormPicCapControlsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import plotly.graph_objects as go
import json
import anvil.image
from HashRouting import routing
from anvil_extras import augment, popover


@routing.route('picture-capture-controls')
class FormPicCapControls(FormPicCapControlsTemplate):
  def __init__(self, data=None ,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.role = Globals.user['role']
    
    # Indicates we need to UPDATE rows in db not ADD new rows
    self.update_database = False

    # Set the starting page number:
    self.page_number = 1
    self.num_images_changed = -1
    self.num_images = 0

    # File path to user specified image directory
    self.file_path_src = ""
    self.file_path_dst = ""
    self.processed_sub_folders = False # Radio button user choice

    self.MAX_LENGTH = 50 # value should be same as on Uplink code
    self.furthest_page = 0

    self.img_label_dict = None
    self.modified_img_label_dict = None
    self.img_name_list = None
    self.retrieved_image_list = None

    # Create some text hover-over for improved UI
    self.helper_link_1.popover(content='Note: Must have access to the local machine to use the file navigator.', placement="right")
    self.helper_link_2.popover(content='Creates a folder in source directory to house processed images', placement="right")
    self.helper_link_3.popover(content='Creates sub-folders for each class inside of the destination directory', placement="right")

   

  def rb_auto_dir_clicked(self, **event_args):
    """Display different flow panels based on which radio button is active"""
    self.flow_panel_1.visible = True
    self.flow_panel_11.visible = False

  def rb_file_explorer_clicked(self, **event_args):
    """Display different flow panels based on which radio button is active"""
    self.flow_panel_1.visible = False
    self.flow_panel_11.visible = True


  def check_box_src_as_dst_change(self, **event_args):
    """This method is called when the checkbox with text:
          "Use same source directory for destination"
          Is checked or unchecked.

        If checked -> remove "Open File Explorer" button
        IF checked -> src directory will be used as the destination directory (processed_images folder will be created inside) 
    """
    
    if (self.check_box_src_as_dst.checked):
      self.flow_panel_10.visible = False
      # Create our dst path based on user src path:
      self.file_path_dst = self.file_path_src + "/processed_images"
    else:
      self.flow_panel_10.visible = True

  def check_box_dst_sub_folders_change(self, **event_args):
    """This method is called when this checkbox with text:
          "Create sub-folder for each class"
        sets self.processed_sub_folders True / False  
    """

    if (self.check_box_dst_sub_folders.checked):
      self.processed_sub_folders = True
    else:
      self.processed_sub_folders = False
      

  def button_file_explorer_src_click(self, **event_args):
    """ Image Source Directory:
        When this button is pressed, we want to open a file explorer such that the 
        user can navigate to and select their desired path
        **WILL ONLY WORK IF USER IS ON THE LOCAL MACHINE,, FILE EXPLORER WILL OPEN ON ANVIL.UPLINK SIDE**
    """

    # Call anvil uplink function and return the source file path (type str)
    try:
      self.file_path_src = anvil.server.call("open_file_explorer")
      self.tb_file_path_src.text = self.file_path_src
    except (Exception) as e:
      print(e)
    return

  def button_file_explorer_dst_click(self, **event_args):
    """ Image Destination Directory:
        When this button is pressed, we want to open a file explorer such that the 
        user can navigate to and select their desired path
        **WILL ONLY WORK IF USER IS ON THE LOCAL MACHINE,, FILE EXPLORER WILL OPEN ON ANVIL.UPLINK SIDE**
    """
    # Call anvil uplink function and return the dst file path (type str)
    try:
      self.file_path_dst = anvil.server.call("open_file_explorer")
      self.tb_file_path_dst.text = self.file_path_dst
    except (Exception) as e:
      print(e)
    return
   
  def display_images(self):
    """"""

    # Remove any canvas' or radiobuttons:
    self.canvas_colpan.clear()

    #--- Class Variables --- #
    #
    self.radiobut_dict = {}
    # Keep track of our canvas':
    self.canvas_list = []

    # Radiobutton dictionary key indexing:
    num_list = [x for x in range(self.num_images)]
    
    # Loop through all retrieved images and display them along with img_label radio buttons 
    for i in range(len(self.retrieved_image_list)):

      # Keep track of our radio buttons so we can modify them later
      radiobut_list = []

      # Get our ith radiobutton dict key
      rb_index = num_list[0]
      del num_list[0] # remove the first element after retrieving it

      # Get the name of img (EX. img_2022-10-16_17:55:13.png)
      img_name = self.img_name_list[i]
      # Get the label assigned to the image via the JOINT classifier
      img_label = self.img_label_dict[img_name]
      
      #Set up components for each image. Each image needs a row of radio buttons & a spacer, all placed in a column panel.
      self.spacer = Spacer(width=50)
      # Set up radio_buttons
      self.rb_class_cotton = RadioButton(text="Cotton", group_name=f"img_label{i}")
      self.rb_class_tray = RadioButton(text="Tray (90% Empty)", group_name=f"img_label{i}")
      self.rb_class_plastic = RadioButton(text="Plastic", group_name=f"img_label{i}")
      self.rb_class_hid = RadioButton(text="HID", group_name=f"img_label{i}")
      self.rb_class_other = RadioButton(text="Other / Unknown", group_name=f"img_label{i}")

      # Set-up colpan to hold the canvas
      colpan_canvas = ColumnPanel(spacing_above='Large', spacing_below='Large')
      # Set-up colpan to hold the spacer
      spacer_colpan = ColumnPanel(spacing_below="Small")
      # Set spacer height
      spacer_space = Spacer(height=50)
      spacer_colpan.add_component(spacer_space)
      
      # Set-up a flowpanel to hold our radio buttons
      flowpan_rb = FlowPanel(spacing_above='None', spacing_below='Large', border='solid')

      # Identify which radio button should be selected based on JOINT classifier prediction
      if(img_label == "Cotton"):
        self.rb_class_cotton.selected = True
      elif(img_label == "Tray"):
        self.rb_class_tray.selected = True
      elif(img_label == "Plastic"):
        self.rb_class_plastic.selected = True
      elif(img_label == "HID"):
        self.rb_class_hid.selected = True
      else:
        self.rb_class_other.selected = True

      # Add all of our radio buttons to our list so we can modify them later on:
      radiobut_list += [self.rb_class_cotton, 
                  self.rb_class_hid, 
                  self.rb_class_other, 
                  self.rb_class_plastic, 
                  self.rb_class_tray]

      # Add our radiobuttons to a dictionary for storage, using the rb_index as our keys (0,1,2,3...)
      self.radiobut_dict[rb_index] = radiobut_list
      
      # Create a new Canvas component for each image:
      self.canvas = Canvas(width=960, height=735) # Height > image_height (image: 960x720)
      
      # Retrieve our image from our image list 
      self.image = self.retrieved_image_list[i]

      # Add the "reset" event handler to each Canvas (this allows us to display the image, else nothing would be displayed)
      self.canvas.add_event_handler('reset', self.canvas_reset)

      # Add each canvas to our list for later access:
      self.canvas_list.append(self.canvas) # JW_Note: Do we want to do this?

      # add our canvas to our colpan
      colpan_canvas.add_component(self.canvas)
      
      # Add all of our radio buttons to our flowpanel
      flowpan_rb.add_component(self.spacer)
      flowpan_rb.add_component(self.rb_class_cotton)
      flowpan_rb.add_component(self.rb_class_tray)
      flowpan_rb.add_component(self.rb_class_hid)
      flowpan_rb.add_component(self.rb_class_plastic)
      flowpan_rb.add_component(self.rb_class_other)
      
      # add our components to the page:
      # self.canvas_colpan --> colpan initlized on load up
      self.canvas_colpan.add_component(colpan_canvas)
      self.canvas_colpan.add_component(flowpan_rb)      
      self.canvas_colpan.add_component(spacer_colpan)


    print(f"original labels: {self.img_label_dict}")

    # Update the page number:
    if self.page_number == 0:
      self.page_number = 1
      self.furthest_page = 1
    self.page_number_text_box.text = self.page_number 
    # self.submitted_button.visible = False
    # self.update_database = False
    # self.num_images_changed = self.num_images
    

  

  def canvas_reset(self, **event_args):
    """This method is called when the canvas is reset and cleared, such as when the window resizes, or the canvas is added to a form.
        Allows for the canvas to display our image, else it would be blank.
    """
    # Draw (display) our image:
    self.canvas.draw_image(self.image)

  def submit_changes_button_click(self, **event_args):
    """This method is called when the submit changes button is pressed
       When pressed, the images (names, and labels) are stored in a database via Anvil Uplink
       
       Function  Outline:
       1. Loop through images and store img name (key) & img label (value) in modified_img_label dict
          1a. img label could be same as JOINT prediction or changed.
          
       2. Check if user wants to ADD img names to database or UPDATE existing rows
        2a. Add: if new images & first time pressing submit_changes button
        2b. Update: If previous images(from back button) OR / AND if user presses submit_changes button > 1

       Variable Statements:
       self.modified_img_label_dict -> Keys: image names, Values: Labels assigned after user inspection
    """

    # Reset the dict on each press of button:
    self.modified_img_label_dict = {}

    # Iterate through each image checking if the labels were changed
    for i in range(len(self.retrieved_image_list)):
      radiobut_list = self.radiobut_dict[i]
      # Check which radio button is selected:
      # 0: Cotton radio button
      if(radiobut_list[0].selected): 
        self.modified_img_label_dict[self.img_name_list[i]] = "Cotton"
      # 1: HID radio button
      elif(radiobut_list[1].selected):
        self.modified_img_label_dict[self.img_name_list[i]] = "HID"
      # 2: Other Radio button
      elif(radiobut_list[2].selected):
        self.modified_img_label_dict[self.img_name_list[i]] = "Other"
      # 3: Plastic radio button
      elif(radiobut_list[3].selected):
        self.modified_img_label_dict[self.img_name_list[i]] = "Plastic"
      # 4: Tray radio button
      elif(radiobut_list[4].selected):
        self.modified_img_label_dict[self.img_name_list[i]] = "Tray"
      
    # Display updated img name & labels key-value pairs (debug tool)
    print(f"modified labels: {self.modified_img_label_dict}")

    
    # Use self.update_database to determine if we are updating the database or adding to the database.
    if not self.update_database:
      # If we enter this conditional, we are ADDING rows to our database
      print("original")
      # Now return the modified and original img:label dict back via uplink
      json_data = json.dumps({
            'selected_folder': "dir",
            'page_num': self.page_number,
            'user_id': self.user_id,
            'file_path_src': self.file_path_src,
            'file_path_dst': self.file_path_dst,
            'proc_sub_folders': self.processed_sub_folders,
            'original_labels': self.img_label_dict,
            'modified_labels': self.modified_img_label_dict,
          })
  
      # Call anvil uplink function to store img info in database & sort images
      anvil.server.call("submit_labels_to_db", json_data)
      self.update_database = True
    else:
      # If we enter this conditional, we are UPDATING rows to our database
      print("updating images database")
      
      # Now return the modified and original img:label dict back via uplink
      json_data = json.dumps({
            'selected_folder': "update",
            'page_num': self.page_number,
            'user_id': self.user_id,
            'file_path_src': self.file_path_src,
            'file_path_dst': self.file_path_dst,
            'original_labels': self.img_label_dict,
            'modified_labels': self.modified_img_label_dict,
          })
  
      # Call anvil uplink function to update img info in database & sort images
      anvil.server.call("submit_labels_to_db", json_data)

    self.submitted_button.visible = True

  
  def next_images_click(self, **event_args):
    """On -> right arrow button press, grab self.num_images new images

       Function  Outline:
       1. Check if user has already pressed "submit_changes_button" if not, submit the changes now (see submit_changes_button_click())
       2. Retrieve num_images new images
       3. Follow grab_images_button_directory_click method for displaying new images and image labels (radio buttons)
       
       Variable Statements:
         
    """

    # Remove any canvas' or radiobuttons:
    self.canvas_colpan.clear()
    
    # Get user inputted num of images to display
    self.num_images = self.num_pics_take_box.text

       
    # First check if user pressed "Submit changes button"
    # If they didn't, do it for them now:
    # TODO: This conditional won't work... Need better check
    if not self.submitted_button.visible:
      # Submit the changes here:
      self.modified_img_label_dict = {}

      # Iterate through each image checking if the labels were changed
      for i in range(len(self.retrieved_image_list)):
        radiobut_list = self.radiobut_dict[i]
        if(radiobut_list[0].selected):
          self.modified_img_label_dict[self.img_name_list[i]] = "Cotton"
        elif(radiobut_list[1].selected):
          self.modified_img_label_dict[self.img_name_list[i]] = "HID"
        elif(radiobut_list[2].selected):
          self.modified_img_label_dict[self.img_name_list[i]] = "Other"
        elif(radiobut_list[3].selected):
          self.modified_img_label_dict[self.img_name_list[i]] = "Plastic"
        elif(radiobut_list[4].selected):
          self.modified_img_label_dict[self.img_name_list[i]] = "Tray"

      print(f"modified labels: {self.modified_img_label_dict}")

    
      # TODO: Modify this with updated back-button process
      if not self.update_database:
        # If we enter this conditional, we are ADDING rows to our database
        print("original")
        # Now return the modified and original img:label dict back via uplink
        json_data = json.dumps({
              'selected_folder': "dir",
              'page_num': self.page_number,
              'user_id': self.user_id,
              'file_path_src': self.file_path_src,
              'file_path_dst': self.file_path_dst,
              'proc_sub_folders': self.processed_sub_folders,
              'original_labels': self.img_label_dict,
              'modified_labels': self.modified_img_label_dict,
            })
    
        # Call anvil uplink function to store img info in database & sort images
        anvil.server.call("submit_labels_to_db", json_data)
        self.update_database = True
      else:
        # If we enter this conditional, we are UPDATING rows to our database
        print("updating images database")
      
        # Now return the modified and original img:label dict back via uplink
        json_data = json.dumps({
            'selected_folder': "update",
            'page_num': self.page_number,
            'user_id': self.user_id,
            'file_path_src': self.file_path_src,
            'file_path_dst': self.file_path_dst,
            'original_labels': self.img_label_dict,
            'modified_labels': self.modified_img_label_dict,
          })
  
        # Call anvil uplink function to update img info in database & sort images
        anvil.server.call("submit_labels_to_db", json_data)
  
    # ---------------------------------------
    # HERE: Retrieve num_images new images

    # Update the page number:
    self.page_number += 1

    self.submitted_button.visible = False
    self.page_number_text_box.text = self.page_number
  
    # Start up a new classifier:
    self.start_classifier_button_click()

  
  def prev_images_click(self, **event_args):
    """
       This method is called when the back arrow button is pressed
       This method will retrieve num_images previous images
       Allows user to modify previously assigned labels should they need updating

       Function Outline:
       1. Determine if we can retrieve previous page images.
          1a. If on page 1 -> no previous images can be returned.
          1b. If MAX_LENGTH (maximum number of pages we store for the user) is reached, inform user they can not go back any further
       2. Convert data to JSON and pass to get_classifier_images via uplink
       3. Set self.update_database flag HIGH (indicating the next "submit changes" button press will need to update rows not ADD rows.)
       4. Loop through and display images and radio buttons (same process as grab_images_button_directory_click client function) 

       Variable Statements:
       self.page_number: the current page number.
       self.MAX_LENGTH: maximum length of the "stack" that stores the previous images.
    """
    
    # Update page number:
    self.page_number -= 1
    if (self.page_number <= 0):
      self.page_number = 1
      return
    elif(int(self.page_number) <= (self.furthest_page - self.MAX_LENGTH)):
      noti = Notification(f"Unable to navigate to page.\nMax length exceeded")
      noti.show()
      self.page_number += 1
      return
    
    # Call start_classifier_button_click to retrieve previous images
    self.start_classifier_button_click()
    

  def jump_to_page_num(self, **event_args):
    """
       This method is called when user presses "jump to page" link.
       This method will retrieve num_images previous images from selected (prev) page number
       Allows user to modify previously assigned labels should they need updating

       Function Outline:
       1. Check the entered number is valid:
          1a. If entered number is less than 0 -> INVALID 
          1b. If MAX_LENGTH (maximum number of pages we store for the user) is reached, inform user they can not go back any further
      2. Confirm the selected_page_number is < the furthest page number the user has been to.
      3. Convert data to JSON for easy passing to uplink function. Retrieve prev images and labels.
      4. Loop through and display images and radio buttons (same process as grab_images_button_directory_click client function) 

       Variable Statements:
       selected_page_number: the user entered page number in the self.page_number_text_box field
       valid_page_bool: checks if the user entered number (selected_page_number) is a page # the user has already visited (must be true)

    """

    

    selected_page_number = self.page_number_text_box.text
    if(int(selected_page_number) <= 0):
      noti = Notification(f"Page number {selected_page_number} is not a valid number")
      noti.show()
      self.page_number_text_box.text = self.page_number
      return
    elif(int(selected_page_number) <= (self.page_number - self.MAX_LENGTH)):
      noti = Notification(f"Unable to navigate to page.\nMax length exceeded")
      noti.show()
      self.page_number_text_box.text = self.page_number
      return
      

    valid_page_bool = int(selected_page_number) <= int(self.furthest_page)
    
    if not valid_page_bool:
      noti = Notification(f"Page number {selected_page_number} is not valid.\nMust first visit the page to jump to it.")
      noti.show()
      self.page_number_text_box.text = self.page_number
      return

    self.page_number = int(selected_page_number)
    json_data = json.dumps({
          'user_id': self.user_id,
          'num_images': self.num_images,
          'page_num': self.page_number
    })
    # Retrieve the specified page numbers images...
    self.submitted_button.visible = False
    self.page_number_text_box.text = self.page_number
    self.start_classifier_button_click()

  def start_classifier_button_click(self, **event_args):
    """Method is called when the user wants to start the image retriaval process
    
    """
    

    # Number of images user wants to retrieve:
    self.num_images = self.num_pics_take_box.text
    
    # Convert everything to json for reliable passing to anvil.uplink
    json_data = json.dumps({
          'page_num': self.page_number,
          'user_id': self.user_id,
          'file_path_src': self.file_path_src,
          'num_images': self.num_images,
        })

      
    # IF we are on a new page, "start" the classifier an grab new images
    if self.page_number > self.furthest_page:
      #Update the furthest page:
      self.furthest_page = self.page_number
      noti = Notification(f"Grabbing new images for page {self.page_number}")
      noti.show()
      self.job_id = anvil.server.call("start_classifier_build", json_data)
      # Start timer & pass num images & img src path to Uplink:
      self.chk_classifier_timer.interval = 5 # Set it to 5 seconds # Every n seoncds chk_classifier_timer_tick() is called
    # ELSE if we are on an already visted page, grabbed the previously displayed images
    else:
      noti = Notification(f"Grabbing previously retrieved images for page {self.page_number}")
      noti.show()
      self.retrieved_image_list, self.img_label_dict, self.img_name_list, self.update_database = anvil.server.call("start_classifier_build", json_data)
      self.display_images()
      
      

  def chk_classifier_timer_tick(self, **event_args):
    """ Method is called every self.chk_classifier_timer.interval seconds
    """

    
    
    # Convert everything to json for reliable passing to anvil.uplink
    json_data = json.dumps({
            'user_id': self.user_id,
            'job_id': self.job_id,
            'file_path_src': self.file_path_src,
            'num_images': self.num_images,
    })

    
    self.done_classifing, pct_ready, self.img_label_dict, self.img_name_list, self.retrieved_image_list = anvil.server.call("check_classifier_progress", json_data)

    if self.done_classifing:
      noti = Notification(f"Finished classifing images for job {self.job_id}")
      noti.show()
      # Set timer interval to 0 once classifier is finished
      self.chk_classifier_timer.interval = 0
      # Display images here:
      print(self.img_label_dict)
      print(self.img_name_list)
      # Display images:
      self.display_images()
      self.update_database = False
      
      
    else:
      noti = Notification(f"{pct_ready}% images finished for job {self.job_id}")
      noti.show()
    
