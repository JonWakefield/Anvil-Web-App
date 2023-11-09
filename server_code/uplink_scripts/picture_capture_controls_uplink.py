"""

Author: JW
Date: 07/26/2023
Module Name: picture_capture_controls_uplink.py

Description:
    This Python script is part of an image processing and classification application. 
    It provides various functions for interacting with images, databases, and user stacks. 
    The script includes functionalities such as simulating image classification, checking classification progress, and updating image labels in a database. 
    It is designed to work with Anvil, tkinter, multiprocessing, and PIL (Python Imaging Library) libraries.

Functions:
- `open_file_explorer`: Opens a file explorer dialog for selecting directories.
- `classify_images_simulate`: Simulates image classification and stores results in a database.
- `start_classifier_build`: Initiates the image classification process, handling new or existing image stacks.
- `check_classifier_progress`: Monitors the progress of image classification and retrieves completed labels and images.
- `submit_labels_to_db`: Handles the submission of labels to a database, updates labels, and moves files based on labels.

For detailed information on each function's purpose and usage, please refer to the function definitions and comments within the script.

"""
from time import sleep
import random
import json
import uuid
import multiprocessing
from PIL import Image
import anvil.media
import os 
import io
import shutil

# Uplink imports:
try:
    import utils.mySQL_utils as localSQL
    from uplink_scripts.stack import Stack
# Local host imports
except (ModuleNotFoundError) as mod_err:
    print("Trying local host imports in picture_capture_controls.py")
    from ..utils import mySQL_utils as localSQL
    from .stack import Stack



# NOTE: When running from a docker container, we will be unable to import tkinter:
try:
    import tkinter as tk
    from tkinter import filedialog
except(ImportError) as err:
    print("Unable to import tkinter")
    




# Set up our stack:
image_stack = Stack()

def open_file_explorer():
    """
        Opens a file explorer navigator for the user to select the source and / or destination directory.

        Returns str(file_path)
        *Depending on when function is called, file_path could be either the source or destination dir.
    """
    try:
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askdirectory()

        if not file_path:
            file_path = "N/A"

        root.destroy()

        return file_path
    except (Exception) as err:
        print("tikinter not installed...returning empty path")
        return ""


def classify_images_simulate(image_full_path, img_name_list, job_id):
    """ Test function to simulate classify_images()
        1. sleep 5 seconds 
        2. randomly pick a class
        3. write result and job id to data-table
    """

    labels = ["Cotton", "Plastic", "HID", "Tray", "Other"]
    cnx = localSQL.sql_connect()

    for index, img in enumerate(image_full_path):
        # 1 sleep
        sleep(10)
        # 2 randomly select a label
        rand = random.randint(0, 4)
        label = labels[rand] 
        # write label & job_id to data-table:
        img_name = img_name_list[index]
        
        insert_query = f"INSERT INTO anvil_imgProcessor (job_id, img_name, img_label) VALUES ('{job_id}','{img_name}','{label}')"

        localSQL.sql_insert(cnx, insert_query)

    # Close db connection
    localSQL.sql_closeConnection(cnx)
    print("Finished classyfing")




def start_classifier_build(json_data):
    """
        json_data: {image_path, num_images}
    """


    # convert json dict to python dict
    python_dict_classifier = json.loads(json_data)
    
    # Unpack the dictionary:
    page_num = python_dict_classifier.get("page_num")
    user_id = python_dict_classifier.get("user_id")
    num_images = python_dict_classifier.get("num_images")
    file_path = python_dict_classifier.get("file_path_src")

    # IF user wants to grab previous images (back_button press or jump_to_page) -> "pop" images from stack, ELSE get new images
    try:
        # Try getting images from the users stack using page_num as the list index.
        labels, img_names, images, update_database = image_stack.pop(user_id, page_num)
        
        # If the number of images retrieved == to number of images user currently wants to retrieve, return the images:
        if (int(num_images) == len(img_names)):
            print(f"Retrieved previous images for page {page_num}")
            return images, labels, img_names, update_database
        # If the user changed the number of images to display on each page -> reset stack and grab new images.
        else:
            print(f"Number of images changed... reseting users stack")
            # TODO: If user changed the number of images to grab, reset the users stack:
            image_stack.reset_stack(user_id)
    # If we get a KeyError or IndexError -> grab new images from directory.
    except (KeyError, IndexError) as err:
        print(f"{err}: Grabbing new images for page {page_num}")

    # Set up a job ID:
    job_id = str(uuid.uuid4())

    job_id = job_id.replace("-", "")

    try:
        # NOTE: with large n we may want to only a subset of all images 
        all_files_in_dir = os.listdir(file_path)
        # Filter to select only image files:
        all_images = [file for file in all_files_in_dir if file.endswith(".jpg") or file.endswith(".png")]
    except (Exception) as e:
        print("Could not access directory")
        return None

    num_images_found = len(all_images)

    # Check to make sure images were found in the directory:
    if(num_images_found == 0):
        print("Dir does not contain any images")
        return None, None, None, None
    # If for whatever reason the directory has < 10 images -> grab all found images
    if(num_images_found < int(num_images)):
        # Randomly select n images:
        rand_n_imgs = random.sample(all_images, int(num_images_found))
        # now that we've selected our images, lets move them to a seperate folder such that they are not re-used
    else:
        # Randomly select n images:
        rand_n_imgs = random.sample(all_images, int(num_images))
        # now that we've selected our images, lets move them to a seperate folder such that they are not re-used


    #Establish Connection to the Databse:
    cnx = localSQL.sql_connect()
    
    # Write job ID to anvil_img_Classifier data-table:
    insert_query = f"INSERT INTO anvil_imgProcessor (job_id) VALUES ('{job_id}')"

    localSQL.sql_insert(cnx, insert_query)

    #Close connection to the database:
    localSQL.sql_closeConnection(cnx)

    imgs_full_path, img_name_list  = [], []

    # Loop accomplishes two things:
    # 1) Creates the full image path for each randomly selected image
    # 2) Reads in the image and converts to anvil.BlobMedia
    for image in rand_n_imgs:

        # Get the full image path
        img_full_path = file_path + "/" + image
        
        # Keep track of all the img paths
        imgs_full_path.append(img_full_path)
        img_name_list.append(image)


    ##############
    # NOTE: SPAWN new process here:
    #classify_images(imgs_full_path, job_id)
    ##############
    process = multiprocessing.Process(target=classify_images_simulate, args=(imgs_full_path, img_name_list, job_id))
    # Start the process
    process.start()


    return job_id




def check_classifier_progress(json_data):
    """
        This function will be called every n seconds once timer reaches 0...
        1. Every n seconds go out and check database to see how many images / n are ready
            1a. if > n images are done, return % finished and update progress bar.
            1b. if n images are done retrieve labels, set flag HIGH indiciating we are ready to display the images to the user

    """

    MAX_STACK_HEIGHT = 50 # Starting with 50, could be increased... (100*num_images) = # of elem ents in each stack

    # convert json dict to python dict
    python_dict_classifier = json.loads(json_data)
    
    # Unpack the dictionary:
    user_id = python_dict_classifier.get("user_id")
    num_images = python_dict_classifier.get("num_images")
    job_id = python_dict_classifier.get("job_id")
    file_path = python_dict_classifier.get("file_path_src")


    # Check database using job_id to see how many images are ready.
    # Establish Connection to the Databse:
    cnx = localSQL.sql_connect()
    # Create a cursor
    cursor = cnx.cursor()

    search_query = f"SELECT * FROM anvil_imgProcessor WHERE job_id = ('{job_id}')"

    cursor.execute(search_query)
    rows = cursor.fetchall()

    # Close the connection
    cnx.close()

    num_rows_ready = len(rows)
    print(num_rows_ready)

    img_labels_list, img_name_list, img_list = [], [], []
    img_labels_dict = {}

    if(num_rows_ready == (num_images + 1)):
        done_classifying = True # Set our flag to true
        pct_ready = 1
        # Once images are done get the assigned labels:
        for row in rows:
            # Get the assigned label for each image:
            img_labels_list.append(row[-1])
            img_name_list.append(row[-2])

        # Delete the first element of each list (first element has NULL label and img name values)
        del img_labels_list[0]
        del img_name_list[0]

        # Store key-value pair (img_name: label) in dict data-structure
        for i in range(len(img_name_list)):
            img_labels_dict[img_name_list[i]] = img_labels_list[i]

            # Using the image name and file path, import the image to type anvil.BlobMedia
            # Get the full image path
            img_full_path = file_path + "/" + img_name_list[i]

            # Retrieve our image using PIL
            pil_img = Image.open(img_full_path)

            # resize image to 1280 x 960
            resized_image = pil_img.resize((960,720))

            bs = io.BytesIO()
            # Convert to bytes:
            resized_image.save(bs, format="png")

            # Conver to type anvil.BlobMedia so that we can display it for the client
            anvil_image = anvil.BlobMedia("image/png", bs.getvalue(), name="cotton") 
            img_list.append(anvil_image)
         
        print(img_labels_list)
        print(img_labels_dict)

        # Set-up the "stack" here:
        # Pythonic: If user does not have a stack created, create one
        try:
            print(f"Adding images for user {user_id} to stack...")
            image_stack.push(user_id, 
                             img_labels_dict, 
                             img_name_list,
                             img_list)
        except (KeyError) as ke:
            print("No ID found!")
            print(f"Creating stack for user: {user_id} ")
            image_stack.init_user(user_id, 
                                  img_labels_dict, 
                                  img_name_list,
                                  img_list)
        
        #Check length of stack if stack is > max_len --> start removing elements
        try:
            stack_height = image_stack.size(user_id)
            if(stack_height > MAX_STACK_HEIGHT):
                print(f"Users stack reached max height of {MAX_STACK_HEIGHT}, Removing first element...")
                # Delete first [0] from stack
                image_stack.delete_element(user_id)
        except (KeyError) as err:
            print(f"Unable to get height of users stack: {err}")    

        return [done_classifying, pct_ready, img_labels_dict, img_name_list, img_list]
    else:
        done_classifying = False
        pct_ready = ((num_rows_ready - 1) / (num_images)) * 100

        return [done_classifying, pct_ready, False, False, False]



def submit_labels_to_db(json_data):
    """ 
        Retrieves images from src directory, runs through classifier, adds images to users stack, and returns images and labels.

        Function Outline:
        1. Unpack JSON data
        2. Determine if retreiving previously used images, or grabing new images from directory.
            Using a Try / Except statement, that returns a IndexError if the index (page_num) is not valid (aka grab new images then)
        3. Access the source directory (file_path) and randomly selected num_images_to_get from directory.
        4. Convert each image to type Anvil.BlobMedia so that we can display them in a Canvas component.
            4a. TEMPORARY: assign image a "dummy" label of either HID or Cotton
            4b. TODO: ADD in classifers to replace "dummy" labels
        5. Check if user already has a stack made for them, if not create one using user_id
            5a. Add images to already made or newly created user stack
        6. Check if MAX_STACK_HEIGHT has been exceeded, if so remove first entry from stack.
        6. Return the images (img_list), img_labels (img_label_dict), img names (img_name_list), and update_database BOOLEAN indicator 


    """

    

    #Extract our json data into a python dict
    python_dict = json.loads(json_data)

    processed_dir = python_dict.get("file_path_dst")
    #processed_dir = "/home/pi/Desktop/Jon_workspace/Anvil/processed_images" # NOTE: ONLY USED FOR TESTING (REMOVE FOR DEPLOYMENT)

    # Create the destination directory if it doesn't exist
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)


    keys_list = []
    

    # Unpack the dict:
    classifier_labels = python_dict.get("original_labels")
    #human modified labels
    modified_labels = python_dict.get("modified_labels")
    selected_folder = python_dict.get("selected_folder")
    page_num = python_dict.get("page_num")
    user_id = python_dict.get("user_id")
    use_sub_folders = python_dict.get("proc_sub_folders")


    #If user manually specified the path, enter:
    if(selected_folder == "dir"):

        # Add the user modified labels to their stack:
        try:
            print(f"Adding modified labels for user {user_id} to stack...")
            image_stack.push(user_id, 
                             user_labels=modified_labels)
        except (KeyError) as ke:
            print("No ID found!")
            print(f"Creating modified labels stack for user: {user_id} ")
            image_stack.init_user(user_id, 
                                  user_labels=modified_labels)

        file_path = python_dict.get("file_path_src")
        #file_path = "/home/pi/Desktop/Jon_workspace/Anvil/Cotton" # NOTE: ONLY USED FOR TESTING (REMOVE FOR DEPLOYMENT)

        # Check if we need to set up sub-folders:
        if(use_sub_folders):
            print("Setting up sub folders")
            # Set-up sub-folders for the processed images
            proc_cotton_dir = processed_dir + "/cotton"
            proc_tray_dir = processed_dir + "/tray"
            proc_plastic_dir = processed_dir + "/plastic"
            proc_hid_dir = processed_dir + "/HID"
            proc_other_dir = processed_dir + "/other"
            proc_mislabeled_dir = processed_dir + "/mislabeled"

            # Create the destination directory if it doesn't exist
            if not os.path.exists(proc_cotton_dir):
                os.makedirs(proc_cotton_dir)
            if not os.path.exists(proc_tray_dir):
                os.makedirs(proc_tray_dir)
            if not os.path.exists(proc_plastic_dir):
                os.makedirs(proc_plastic_dir)
            if not os.path.exists(proc_hid_dir):
                os.makedirs(proc_hid_dir)
            if not os.path.exists(proc_other_dir):
                os.makedirs(proc_other_dir)
            if not os.path.exists(proc_mislabeled_dir):
                os.makedirs(proc_mislabeled_dir)
            

        # get all the keys (image names)
        for key in classifier_labels:
            keys_list.append(key)

        # Next, Establish Connection to the Databse:
        cnx = localSQL.sql_connect()

        # Loop through each key(image name) and add to correct db column
        for key in range(len(keys_list)):
            image_name = keys_list[key]
            orginal_label = classifier_labels[keys_list[key]]
            corrected_label = modified_labels[keys_list[key]]

            # Get our source path (used with moving the image):
            source_path = os.path.join(file_path, image_name)
            # Get our processed img path:
            dest_path = os.path.join(processed_dir, image_name)

            if(orginal_label == corrected_label):
                correctP = True
                # Add to to columns: Correct_column, JOINT, and Path
                add_query = f"INSERT INTO anvil_imgClassification ({corrected_label}, JOINT, Path) VALUES ('{str(keys_list[key])}', '{str(orginal_label)}' ,'{str(source_path)}')"
                localSQL.sql_insert(cnx, add_query)
            else:
                # If the classifier got the prediction wrong, add img file name to GotWrong column and correct column in database
                correctP = False
                # Add to to columns: GotWrong, Correct_column, JOINT, and Path
                gotWrong_query = f"INSERT INTO anvil_imgClassification (GotWrong, {corrected_label}, JOINT, Path) VALUES ('{str(keys_list[key])}', '{str(keys_list[key])}', '{str(orginal_label)}' , '{str(source_path)}')"
                localSQL.sql_insert(cnx, gotWrong_query)


            #Lastly, move image to new processed directory:
            try:
                if(use_sub_folders):
                    if(corrected_label == "Cotton"):
                        shutil.copy(source_path, proc_cotton_dir)
                    elif(corrected_label == "Plastic" ):
                        shutil.copy(source_path, proc_plastic_dir)
                    elif(corrected_label == "HID" ):
                        shutil.copy(source_path, proc_hid_dir)
                    elif(corrected_label == "Tray" ):
                        shutil.copy(source_path, proc_tray_dir)
                    elif(corrected_label == "Other" ):
                        shutil.copy(source_path, proc_other_dir)

                    # Check if we also need to move file to the GotWrong fodler:
                    if(correctP):
                        # Delete the file from the src directory
                        if os.path.exists(source_path):
                            os.remove(source_path)
                    else:
                        # move file to the GotWrong folder:
                        shutil.move(source_path, proc_mislabeled_dir)
                else:
                    shutil.move(source_path, dest_path)
            except (FileNotFoundError) as e_file:
                return


        #Close connection to the database:
        localSQL.sql_closeConnection(cnx)            

        return

    
    elif(selected_folder == "update"):
        
        # Need to update modified labels stack:
        print(f"Updating modified labels from page {page_num} for user {user_id}")
        image_stack.update_stack(user_id, page_num, user_labels=modified_labels)

        # Names of table columns, will be iterated over
        column_names = ["Cotton","Plastic", "HID", "Tray", "Other"]

        print("Updating database...")

        # Search through CSV and find the lines that need to be altered:

        # get all the keys
        for key in classifier_labels:
            keys_list.append(key)

        # Next, Establish Connection to the Databse:
        cnx = localSQL.sql_connect()
        # Create a cursor
        cursor = cnx.cursor()

        for key in range(len(keys_list)):
            image_name = keys_list[key]
            corrected_label = modified_labels[keys_list[key]]

            #Iterate over the possible column (labels) in the table:
            for column in column_names:
                #Search for img name in each column to get the row:
                search_query = f"SELECT * FROM anvil_imgClassification WHERE {column} = ('{str(keys_list[key])}')"

                cursor.execute(search_query)
                result = cursor.fetchone()
                try:
                    cnx.commit()
                except (Exception) as err:
                    pass

                # RESULT RETURNED FORMAT: (row_number(id), user_id, Cotton, Plastic, Tray, HID, Other, GotWrong, PATH, JOINT) of type tuple
                if result:

                    if corrected_label == column:
                        print(f"No need to update img {image_name} found in {column} with label {corrected_label}, breaking out...")
                        break

                    # print(f"result value returned: {result}")
                    # print(f"Image name {str(keys_list[key])}")
                    
                    # Get row number:
                    row_number = str(result[0])
                    # print(f"column value: {row_number}")
                    # Get JOINT value:
                    joint_value = str(result[-1])
                    # Set row value in previous column and GotWrong column to None:
                    update_query = "UPDATE anvil_imgClassification SET %s = NULL, GotWrong = NULL WHERE id = %s"%(column, row_number)
                    cursor.execute(update_query)
                    cnx.commit()

                    # check if joint == new_label
                    if(joint_value == corrected_label):
                        print("Joint == Correct!")
                        # Add img name to the corrected_label colum in row_number:
                        update_query = f"UPDATE anvil_imgClassification SET {str(corrected_label)} = '{str(keys_list[key])}' WHERE id = '{row_number}'"
                        cursor.execute(update_query)
                        cnx.commit()
                    else:
                        update_query =f"UPDATE anvil_imgClassification SET {str(corrected_label)} = '{str(keys_list[key])}', GotWrong = '{str(keys_list[key])}' WHERE id = '{row_number}'"
                        cursor.execute(update_query)
                        cnx.commit()

                    # print("breaking..")
                    break
                    
                else:
                    print(f"result not found in column {column}")

             
    #Close connection to the database:
    cnx.close()

    return