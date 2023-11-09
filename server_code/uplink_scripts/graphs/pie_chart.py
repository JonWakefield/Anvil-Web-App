"""
    NOTE: NOT AN ACTIVE MODULE
    
    Author: JW
    Date: 07/26/2023
    Module Name: pie_chart.py

    Description:
        This Python script defines the `PieChart` class, 
        which is responsible for creating pie charts using the matplotlib library and displaying 
        them using Anvil's integration with Matplotlib. 
        The pie chart's appearance and data can be customized by adjusting various parameters within the class.

    Class:
    - `PieChart`: A subclass of `ChartCreator`, designed specifically for creating pie charts. 
    It allows customization of chart settings, category colors, axis properties, values, and categories.

    Attributes:
    - `category_colors`: Defines the colors to be used for different categories in the pie chart.
    - `axis_property`: Specifies the aspect ratio of the pie chart.
    - `values`: List of numerical values for each category in the pie chart.
    - `categories`: List of category labels corresponding to the values.

    Methods:
    - `create_pie_chart()`: Generates the pie chart based on the provided data and settings. It returns the pie chart as an Anvil plot image.

    For detailed information on using the `PieChart` class and its available customization options, please refer to the class definition and comments within the script.
"""

# import anvil.mpl_util
# import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib
# matplotlib.use('Agg') # NOTE prevents: RuntimeError: main thread is not in main loop (NEEDED FOR UPLINK)
# import json
# import seaborn as sns
# import datetime
# import numpy as np
# from datetime import datetime, timedelta
# import matplotlib.dates as mdates


# Uplink imports:
try:
    from utils import mySQL_utils as localSQL

# Local host imports:
except (ModuleNotFoundError) as err:
    print("Trying local server imports in bar_chart.py")
    from ...utils import mySQL_utils as localSQL



# class PieChart():
#     def __init__(self, chart_settings: tuple):

#         self.category_colors = "default"
#         """ 
#             Could offer a few options:
#             - default
#             - monotone
#             - bright 
#         """

#         self.axis_property = "equal"
#         """
#             Possible Options:
#             - equal, 
#             - tight, 
#             - scaled, 
#             - image
#         """

#         self.values = [4.223, 3.522, 5.123, 5.567, 7.443]
#         self.categories = ['gs1', 'gs2', 'gs3', 'gs4', 'gs5']



#     def create_pie_chart(self):
#         """"""

#         # Create the pie chart
#         plt.pie(self.values, labels=self.categories, colors=self.category_colors, autopct='%1.1f%%', startangle=90)

#         # Customize the chart
#         plt.axis(self.axis_property)  # Equal aspect ratio ensures that the pie is drawn as a circle

#         # Custoize chart
#         if self.title is not None:
#             plt.title(self.title)

#         if self.legend is not None:
#             plt.legend()

#         return anvil.mpl_util.plot_image()

