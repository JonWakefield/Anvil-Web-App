"""
    Author: Jon Wakefield
    Date: 07/20/2023
    Description: 
        - JSON utilily functions used to convert data into a json dictionary
        - See convert_to_json_string_example() for example usage.


"""




import json

def convert_to_json_string(keys: list, values: list) -> str:
    """
        Convert list to JSON data type
        data: list holding the VALUES
        *keys: Key names

        The number of keys == len(data)
    """
    # Initlize our temp dict:
    python_dict = {}

    # First check len(data) and keys are equal:
    if(len(values) != len(keys)):
        print("Number of keys != number of values... quiting")
        return
    
    # Second, create a python dict using the input parameters:
    for index, key in enumerate(keys):
        python_dict[str(key)] = values[index]


    # Last, convert python dict to JSON string:
    json_string = json.dumps(python_dict)

    return json_string



def convert_to_json_string_example():
    """ Functions shows how to use convert_to_json_string() function"""

    # First, set up some synthic data:
    # For example, this could be data retrieved from a database
    synthetic_db_data = ['55', 'cold', 12.3, False, '45.0']

    # Next create a list containing the key names:
    key_names = ["CPU Temp", "Weather", "data", "status", "gain"]


    # Next call the function:
    # NOTE: the len(key_names) must equal len(synthetic_db_data)
    returned_json_string = convert_to_json_string(key_names, synthetic_db_data)

    # Print result to show it worked:
    print(returned_json_string)    


# convert_to_json_string_example()