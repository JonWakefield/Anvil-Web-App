import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
"""
    Author: Jonathan Wakefield
    Date: 5/20/2023
    Description: Create a image "stack" for each user. This allows a user to retrieve previous images (back arrow, or jump_to_page) buttons
                - NOTE: techincally, not a stack as we do not want to "pop" images, rather we want to re-call them 


"""

class Stack:
    def __init__(self):
        """
            4 stacks for each user X:
                1. Classifier labels stack:
                    dict(list(dict))
                2. User Labels stack:
                    dict(list(dict))
                3. Img name stack:
                    dict(list(list))
                4. image stack:
                    dict(list(list))
        """
        self.classifierLabs_stack = {}
        self.userLabs_stack = {}
        self.imgName_stack = {}
        self.img_stack = {}
        self.index_subtractor = {} #keeps track of proper list index when MAX_HEIGHT is exceeded



    def init_user(self, 
                  user_id, 
                  classifier_labels=None, 
                  img_names=None, 
                  images=None, 
                  user_labels=None):
        """ Set-up a new image stack for a new user"""

        # Set-up a key-value pair relationship for the new user:
        if classifier_labels is not None:
            self.classifierLabs_stack[user_id] = [classifier_labels]
            self.imgName_stack[user_id] = [img_names]
            self.img_stack[user_id] = [images]   
            self.index_subtractor[user_id] = 1 # Always starts at 1 

            # print stacks for debug purposes:
            print(self.classifierLabs_stack[user_id])
            print(self.imgName_stack[user_id])
            print(self.img_stack[user_id])

            print(len(self.classifierLabs_stack[user_id]))
            print(len(self.imgName_stack[user_id]))
            print(len(self.img_stack[user_id]))

        # With current approach user_labels wont be init at same time as user init
        if user_labels is not None:
            self.userLabs_stack[user_id] = [user_labels]   

            # print stacks for debug purposes:
            print(self.classifierLabs_stack[user_id])
            print(self.userLabs_stack[user_id])
            print(self.imgName_stack[user_id])
            print(self.img_stack[user_id])

            print(len(self.classifierLabs_stack[user_id]))
            print(len(self.userLabs_stack[user_id]))
            print(len(self.imgName_stack[user_id]))
            print(len(self.img_stack[user_id]))


        
        


    def update_stack(self,
                     user_id,
                     page_num,
                     classifier_labels=None, 
                     img_names=None, 
                     images=None, 
                     user_labels=None):
        """
            Update the user_id's stack at the specified index:

        """
        index = page_num - self.index_subtractor[user_id]

        if user_labels is not None:
            #Update the user labels stack with new changes:
            userlabels_temp = self.userLabs_stack[user_id]

            userlabels_temp[index] = user_labels




        # print stacks for debug purposes:
        print(self.classifierLabs_stack[user_id])
        print(self.userLabs_stack[user_id])
        print(self.imgName_stack[user_id])
        print(self.img_stack[user_id])

        print(len(self.classifierLabs_stack[user_id]))
        print(len(self.userLabs_stack[user_id]))
        print(len(self.imgName_stack[user_id]))
        print(len(self.img_stack[user_id])) 


    def push(self, 
             user_id, 
             classifier_labels=None, 
             img_names=None, 
             images=None, 
             user_labels=None):
        """
            Current Approach to function calls:
                1. When images are first retrieved from directory,
                    arguments passed in: {classifier_labels, img_names, images}

                2. When images are being submitted after user has corrected / modified any labels
                    arguments passed in: {user_labels}
        """

        
        if classifier_labels is not None:
            print("Adding classifier labels, img names, and images to stack...")
            # Add values to the stack for the user
            clabels_temp = self.classifierLabs_stack[user_id]
            img_names_temp = self.imgName_stack[user_id]
            images_temp = self.img_stack[user_id]

            # Push the new values:
            clabels_temp.append(classifier_labels)
            img_names_temp.append(img_names)
            images_temp.append(images)

            # Add the new list with current values back to the stack dict:
            self.classifierLabs_stack[user_id] = clabels_temp
            self.imgName_stack[user_id] = img_names_temp
            self.img_stack[user_id] = images_temp

        if user_labels is not None:
            print("Adding user modified labels to stack...")
            # Add values to the stack for the user
            userlabels_temp = self.userLabs_stack[user_id]

            # Push the new values:
            userlabels_temp.append(user_labels)

            # Add the new list with current values back to the stack dict:
            self.userLabs_stack[user_id] = userlabels_temp

        
        # print stacks for debug purposes:
        print(self.classifierLabs_stack[user_id])
        print(self.userLabs_stack[user_id])
        print(self.imgName_stack[user_id])
        print(self.img_stack[user_id])

        print(len(self.classifierLabs_stack[user_id]))
        print(len(self.userLabs_stack[user_id]))
        print(len(self.imgName_stack[user_id]))
        print(len(self.img_stack[user_id]))


    def is_empty(self, user_id):
        # 
        images_temp = self.img_stack[user_id]
        return len(images_temp) == 0
    

    def pop(self, user_id, page_num):
        """
            Modified version of a typical "pop"
            Not removing last added, rather grabing from an index

            NOTE: I dont think we need the original label anymore, should already be stored in the database
        """

        index = page_num - self.index_subtractor[user_id]
        has_user_labels = False

        try:
            labels_temp = self.userLabs_stack[user_id]
            labels = labels_temp[index]
            img_names_temp = self.imgName_stack[user_id]
            images_temp = self.img_stack[user_id]
            img_names = img_names_temp[index]
            images = images_temp[index]
            has_user_labels = True
        except (IndexError):
            # Get the current values:
            labels_temp = self.classifierLabs_stack[user_id]
            img_names_temp = self.imgName_stack[user_id]
            images_temp = self.img_stack[user_id]

            img_names = img_names_temp[index]
            images = images_temp[index]
            labels = labels_temp[index]

            has_user_labels = False


        return labels, img_names, images, has_user_labels        

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty. Cannot peek an empty stack.")
        return self.stack[-1]

    def delete_element(self, user_id):
        """"""

        # Get the lists (stack) associated for the correct user
        clabels_temp = self.classifierLabs_stack[user_id]
        img_names_temp = self.imgName_stack[user_id]
        images_temp = self.img_stack[user_id]
        userlabels_temp = self.userLabs_stack[user_id]

        # Delete the first element
        del clabels_temp[0]
        del img_names_temp[0]
        del images_temp[0]
        del userlabels_temp[0]

        # Update our index_subtractor:
        self.index_subtractor[user_id] += 1


    def size(self, user_id):
        """"""
        img_names_list = self.imgName_stack[user_id]
        return len(img_names_list)

    def reset_stack(self, user_id):
        """"""
        # Reset the users data back to user:
        self.classifierLabs_stack[user_id] = []
        self.userLabs_stack[user_id] = []
        self.imgName_stack[user_id] = []
        self.img_stack[user_id] = []

        print(self.classifierLabs_stack[user_id])
        print(self.userLabs_stack[user_id])
        print(self.imgName_stack[user_id])
        print(self.img_stack[user_id])

        print(len(self.classifierLabs_stack[user_id]))
        print(len(self.userLabs_stack[user_id]))
        print(len(self.imgName_stack[user_id]))
        print(len(self.img_stack[user_id]))

        return