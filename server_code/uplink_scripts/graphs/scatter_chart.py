"""
    NOTE: NOT AN ACTIVE MODULE
    Author: JW
    Date: 07/26/2023
    Module Name: scatter_chart.py

    Description:
        This Python script defines the `ScatterChart` class, which is responsible for creating scatter plots using the seaborn and matplotlib 
        libraries. These scatter plots can be customized with various parameters within the class.

    Class:
    - `ScatterChart`: A subclass of `ChartCreator`, designed for creating scatter plots. 
    It allows customization of chart settings, data points, labels, and more.

    Attributes and Methods:
    - The `ScatterChart` class inherits attributes and methods from the `ChartCreator` class, providing chart customization features.
    - `create_scatter_chart()`: Generates a scatter plot using sample data for demonstration purposes. 
        Customize the sample data and other plot properties as needed.

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


# class ScatterChart():
#     def __init__(self, chart_settings: tuple):



#     def create_scatter_chart(self):
#         """"""

#         # Sample data for the scatter plot
#         x_values = [1, 2, 3, 4, 5]
#         y_values = [10, 15, 8, 12, 20]

#         # Create the scatter plot
#         sns.scatterplot(x=x_values, y=y_values, color=self.stem_color, label=self.y1_title)


#         plt.xlabel(self.x_title, fontsize=self.xy_font_size, color=self.xy_font_color)
#         plt.ylabel(self.y1_title, fontsize=self.xy_font_size, color=self.xy_font_color)

#         if self.title is not None:
#             plt.title(self.title)

#         if self.legend is not None:
#             plt.legend()

#         return anvil.mpl_util.plot_image()

        