"""
    NOTE: NOT AN ACTIVE MODULE

    Author: JW
    Date: 07/26/2023
    Module Name: timeline_chart.py

    Description:
        - This Python script defines the `TimelineChart` class, 
            which is responsible for creating timeline charts using the matplotlib library. 
            The timeline charts show data points over a specified time range, with options for customization.

    Class:
    - `TimelineChart`: A subclass of `ChartCreator`, designed for creating timeline charts. 
        It allows customization of chart settings, time intervals, data points, labels, and more.

    Attributes and Methods:
    - The `TimelineChart` class inherits attributes and methods from the `ChartCreator` class, providing chart customization features.
    - `generate_times(start_time, end_time)`: Generates a list of timestamps within a specified time range.
    - `get_time_range()`: Determines the time range based on the selected chart type (1-4) and returns the start and end times.
    - `create_timeline_chart()`: Generates a timeline chart with vertical stems representing data points over time. Customize the chart appearance and data points as needed.

"""

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
# try:
#     from utils import mySQL_utils as localSQL

# # Local host imports:
# except (ModuleNotFoundError) as err:
#     print("Trying local server imports in bar_chart.py")
#     from ...utils import mySQL_utils as localSQL


# class TimelineChart():
#     def __init__(self, chart_settings: tuple):
  

#         # additional timeline Chart settings here:
#         # ... 
#         # ...


#     def generate_times(self, start_time, end_time):
#         """ Generate days (hours) between start and end times"""

#         time_list = []
#         current_time = start_time

#         # hours between conditional
#         if (self.time_range == 4):

#             curent_datetime = datetime.combine(datetime.today(), start_time)
#             end_datetime = datetime.combine(datetime.today(), end_time)

#             while curent_datetime >= end_datetime:
#                 time_list.append(curent_datetime)
#                 curent_datetime -= timedelta(hours=1)
                
#         # Days between conditional
#         else:
#             while current_time <= end_time:
#                 time_list.append(current_time)
#                 current_time += timedelta(days=1)


#         return time_list


#     def get_time_range(self):
#         """ time range is depended upon the chart type (1-4)
            
#             Time interval Codes:
#             1. start of season (Oct. 15)
#             2. 30 days
#             3. 7 days
#             4. 12 hours

#         """

#         # Start of season
#         if self.time_range == 1:
            
#             # Get todays date
#             today = datetime.today().date()

#             # Get start of season date:
#             start_of_season = '2023-10-15'
#             return start_of_season, today
        
#         # Last 30 days:
#         elif self.time_range == 2:
#             # get todays date:
#             today = datetime.today().date()
#             # Get 30 days before:
#             start_date = today - timedelta(days=30)
#             return start_date, today
        
#         # Last 7 days:
#         elif self.time_range == 3:
#             # get todays date:
#             today = datetime.today().date()
#             # Get 7 days before:
#             start_date = today - timedelta(days=7)
#             return start_date, today

#         # Last 12 hours:
#         elif self.time_range == 4:
#             current_time = datetime.now().time()
#             # Get 12 hours ago:
#             start_time = (datetime.combine(datetime.today(), current_time) - timedelta(hours=12)).time()

#             return start_time, current_time



#     def create_timeline_chart(self):
#         """"""
       

#         start_time, end_time = self.get_time_range()
#         # Convert strings to datetime object
#         # start_time = datetime.strptime(start_time, '%Y-%m-%d')
#         # end_time = datetime.strptime(end_time, '%Y-%m-%d')

#         # Generate the list of dates
#         times_between = self.generate_times(start_time, end_time) 


#         # Ex. Data Representing number of plastics spotted on each day
#         # query will need modification but good start:
#         # select_query = f"SELECT {y1_data_column} FROM ginStands WHERE day BETWEEN '{start_time}' AND '{end_time}';"
#         ex_data = [3, 5, 1, 3, 6, 2, 2, 3, 5, 5, 4,] * 3 # One for each day

#         # not needed for production:
#         if self.time_range == 2:
#             self.data = ex_data[0:31]
#         elif self.time_range == 3:
#             self.data = ex_data[0:8] 
#         elif self.time_range == 4:
#             self.data = ex_data[0:13]


#         # Creates stem length in a pattern (better for strings)
#         # if(use_levels):
#         #     levels = np.tile([-5, 5, -3, 3, -1, 1],
#         #                     int(np.ceil(len(times_between)/6)))[:len(times_between)]
#         # else:
#         #     # Creates stem length == magnitude of int (better for nums)
#         #     levels = ex_data # set levels equal to data points

#         levels = self.data # set levels equal to data points

#         if(self.figsize == 'large'):
#             self.figsize = (8.8, 4)
#         elif(self.figsize == 'medium'):
#             self.figsize = (6.6, 3)
#         elif(self.figsize == 'small'):
#             self.figsize = (4.4, 2)

#         fig, ax = plt.subplots(figsize=self.figsize, layout="constrained")

#         if self.title is not None:
#             ax.set(title=self.title)

#         # NOTE: think we will want try / except statement here:
#         ax.vlines(times_between, 0, levels, color=self.stem_color) # The vertical stems.
#         ax.plot(times_between, np.zeros_like(times_between), self.marker_shape,
#                 color=self.line_color, markerfacecolor='r') # Baseline and markers on it.
        
#         for d, l, r in zip(times_between, levels, self.data):
#             ax.annotate(r, xy=(d, l),
#                         xytext=(-5, np.sign(l)*3), textcoords="offset points",
#                         horizontalalignment="right",
#                         verticalalignment="bottom" if l > 0 else "top")
            

#         # Based on days requested determine interval:    
#         if (self.time_range == 4):
#             ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
#             ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#         else:
#             ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
#             ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
            

#         plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

#         # remove y-axis and spines
#         ax.yaxis.set_visible(True)
#         ax.spines[["left", "top", "right"]].set_visible(self.outside_border)

#         ax.margins(y=0.1)
#         # plt.show()
        
#         return anvil.mpl_util.plot_image()
