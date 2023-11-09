"""
    Author: Jon Wakefield
    Date: 10/31/2023
    Module Name: bar_chart.py

    Description:
        - Fetches data from SQL table and constructs a bar chart using data & user provided chart settings.
        - NOTE: Currently is the only type of chart that can be viewed by the client

"""

import anvil.mpl_util
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # NOTE prevents: RuntimeError: main thread is not in main loop (NEEDED FOR UPLINK)
import numpy as np

# Uplink imports:
try:
    from utils import mySQL_utils as localSQL

# Local host imports:
except (ModuleNotFoundError) as err:
    print("Trying local server imports in bar_chart.py")
    from ...utils import mySQL_utils as localSQL


class BarChart():
    def __init__(self, chart_settings: tuple):
        """
            - Called from graphs_uplink.retrieve_chart
            - sets up chart settings using arg `chart_settings` from data-table

            - chart_settings (tuple): Tuple containing users chart settings from table `user_graph_settings`
        """

       # Unpack settings:
        self.data_source = chart_settings[1] # table to get datafrom
        self.chart_type = chart_settings[2] # 
        self.chart_scale = chart_settings[3] #
        self.x_title = chart_settings[4]
        self.y1_title = chart_settings[5]
        self.y2_title = chart_settings[6]
        self.y1_data_column = chart_settings[7]
        self.y2_data_column = chart_settings[8]
        self.xy_font_color = chart_settings[9]
        self.xy_font_size = chart_settings[10]
        self.title = chart_settings[11] 
        self.title_color = chart_settings[12]
        self.column_colors = chart_settings[13]
        self.legend = chart_settings[14]
        self.gin_name = chart_settings[15]
        self.num_gin_stands = chart_settings[16]

        # Barchart settings here:
        # self.horizontal = chart_settings.get('horizontal') #bool
        # self.grouped = chart_settings.get('grouped') #bool
        # self.stacked = chart_settings.get('stacked') #bool
        # self.column_labels = chart_settings.get('column-labels') #bool


    def stacked_bar_chart(self):
        """
            Method Description:
                - Creates a stacked bar chart
                - NOTE: Method is currently not in use
        """

        # Get stacked Data:
        # ... 
        # ...

        # Example Data:
        stacked_data = [[10,12,13,9],[6,2,1,4],[1,1,4,2]]

        x_axis_pos = np.arange(len(stacked_data[0]))
        bottom_stack = np.zeros(len(stacked_data[0]))

        # iterate through retrieved data and create the stacked bar graph:
        for idx, data in enumerate(stacked_data):
            plt.bar(x_axis_pos, data, bottom=bottom_stack, label=f'{self.legend}')
            bottom_stack += data

        # For labeled bar charts:
        if(self.column_labels):
            plt.xticks(x_axis_pos, self.y1_data_column)  

        plt.xlabel(self.x_title, fontsize=self.xy_font_size, color=self.xy_font_color)
        plt.ylabel(self.y1_title, fontsize=self.xy_font_size, color=self.xy_font_color)

        if self.legend:
            plt.legend()

        if self.title is not None:
            plt.title(self.title)

        # 5. Return chart
        return anvil.mpl_util.plot_image()


    def grouped_bar_chart(self):
        """
            Method Description:
                - Creates a grouped bar chart
                - NOTE: Method is currently not in use
        """

        # retrieve data for all variables:
        # num_groups = len(values)
        # num_columns = len(columns)
        # stacked_data = []

        # # get each value from db:
        # for i in range(num_groups):
        #     # retrieve data from db:
        #     # data = retrieve_data(values[i])
        #     # stacked_data.append(data)
        #     pass
        # stacked_data = [[4,3,5,3], [8,9,4,10]]

        # bar_width = 0.30
        # x_axis_pos = np.arange(num_columns)

        # for i in range(num_groups):
        #     plt.bar(x_axis_pos + i * bar_width, stacked_data[i], width=bar_width, label=f'{legend[i]}')

        # plt.xticks(x_axis_pos + bar_width * (num_groups - 1) / 2, columns) 

        # For labeled bar charts:
        # if(self.column_labels):
        #     plt.xticks(x_axis_pos, self.y1_data_column)  

        # plt.xlabel(self.x_title, fontsize=self.xy_font_size, color=self.xy_font_color)
        # plt.ylabel(self.y1_title, fontsize=self.xy_font_size, color=self.xy_font_color)

        # if self.legend:
        #     plt.legend()

        # if self.title is not None:
        #     plt.title(self.title)



        return anvil.mpl_util.plot_image()

    def horizontal_bar_chart(self):
        """
            Method Description:
                - Creates a horizontal bar chart
                - NOTE: Method is currently not in use
        """

        #
        # data = retrieve_data(values)
        # Sample data for the horizontal bar chart
        # dummy_values = [10, 13, 12, 8]

        # # Create horizontal chart:
        # plt.barh(columns, dummy_values, color=column_color, label=legend)

        # # For labeled bar charts:
        # if(self.column_labels):
        #     plt.xticks(x_axis_pos, self.y1_data_column)  

        # plt.xlabel(self.x_title, fontsize=self.xy_font_size, color=self.xy_font_color)
        # plt.ylabel(self.y1_title, fontsize=self.xy_font_size, color=self.xy_font_color)

        # if self.legend:
        #     plt.legend()

        # if self.title is not None:
        #     plt.title(self.title)

        return anvil.mpl_util.plot_image()

    def bar_chart_events(self, chart_data):
        """
            Method Description:
            - Called from self.create_bar_chart after chart data has been retrieved
            - Creates the bar chart & converts to anvil media

        """

        # Max number of columns possible
        max_columns = ['gs1', 'gs2', 'gs3', 'gs4', 'gs5', 'gs6', 'All Stands']

        # create index for each gin_stand
        values = [0] * self.num_gin_stands 

        # loop through chart_data counting num_plastic_events at each gin_stand_num
        for i in range(len(chart_data)):
            # Get row data
            row = chart_data[i]

            # increment plastic detection at gin_stand
            values[row[0]-1] += 1 # row[0] => gin_stand_num


        # Get all events
        sum_events = sum(values)
        
        # Determine how many columns we need (how many gin stands at the selected gin)
        columns = max_columns[:self.num_gin_stands]


        # append `All stands` column:
        if len(columns) > 1:
            columns.append("All Stands")
            values.append(sum_events)

        # Column colors:
        column_colors = plt.cm.rainbow(np.linspace(0, 1, len(columns)))

        plt.bar(columns, values, color=column_colors)

        # # For labeled bar charts:
        for i in range(len(columns)):
            plt.text(columns[i], values[i], str(values[i]), ha='center', va='bottom', fontsize=self.xy_font_size)

        # For labeled bar charts:
        plt.xlabel("Gin Stand Num.", fontsize=self.xy_font_size, color=self.xy_font_color)
        plt.ylabel(self.y1_title, fontsize=self.xy_font_size, color=self.xy_font_color)

        # if self.legend:
        #     plt.legend()

        if self.title is not None:
            plt.title(f"{self.gin_name} {self.title} {self.chart_type}")

        # Set background color:

        # Convert to anvil.media for easy displaying
        return anvil.mpl_util.plot_image()


    def retrieve_chart_data(self):
        """
            Method Description:
                - Called from self.create_bar_chart
                - Retrieves data for `self.gin_name` FROM table `plastic_events` to build chart
        """

        # Get an int representation of our time range
        formated_time_range = format_chart_type(self.chart_type)

        try:
            # connect to database
            cnx = localSQL.sql_connect()

            # if formated_time_range == "*" -> select all gin from current season
            if(formated_time_range == "*"):
                select_query = f"SELECT gin_stand_num, UTC FROM plastic_events WHERE gin_name = '{self.gin_name}'"
            # Else -> get date range
            else:
                select_query = f"SELECT gin_stand_num, UTC FROM plastic_events WHERE gin_name = '{self.gin_name}' AND UTC >= DATE_SUB(CURDATE(), INTERVAL {formated_time_range} DAY)"

            # Perform SQL select:
            retrieved_data = localSQL.sql_select(cnx, select_query)

            # Inform user if we found any data in their selected time range (prevents returning an empty chart)
            if retrieved_data:
                print(f"found data in time range")
                return retrieved_data
            else:
                print("No data found in time range")
                return False
            
        except( Exception) as err:
            print(f"encountered error in bar_chart.py in retrieve_chart_data: \n{err}")

        finally:
            localSQL.sql_closeConnection(cnx)



    def bar_chart_cluster(self, chart_data):
        """"""

        event_timestamps = []

        # Get event event times:
        for i in range(len(chart_data)):
            row = chart_data[i]
            event_timestamps.append(row[1])

        hours = [event_timestamp.hour for event_timestamp in event_timestamps]

        # Get event count:
        return


    def create_bar_chart(self):
        """
            Method Description:
                - Called from graphs_uplink.retrieve_chart
                - Fetches data from table & Creates a bar chart using user provided settings (see __init__)
        """

        # Get our data:
        chart_data = self.retrieve_chart_data()

        # If no data found in time-frame:
        if not chart_data:
            return False

        # Create the chart
        chart_anvil_media = self.bar_chart_events(chart_data)

        # # Create a stacked bar chart:
        # if(self.stacked):
        #     chart = self.stacked_bar_chart()              
            
        # # Create a grouped bar chart:
        # elif(self.grouped):
        #     chart = self.grouped_bar_chart()
            
        # # Create a horizontal bar chart:
        # elif(self.horizontal):
        #     chart = self.horizontal_bar_chart()

        # # Create a regular bar chart:
        # else:
        #     chart = self.bar_chart()

        return chart_anvil_media
           
           


def format_chart_type(unformated_time: str) -> int:
    """
        Function Description:
            - Called from bar_chart.retrieve_chart_data
            - Converts string representation of time-range to integer format
            - integer format (number of days) is needed for sql select query

        Input Args:
            - unformated_time (str): string form representing # of days

        Output Args:
            - (int): int value representing number of days/
    """

    if(unformated_time == "Daily Total" ):
        return 1
    elif(unformated_time == "3 Day Total" or unformated_time == "Event Cluster"):

        return 3
    elif(unformated_time == "7 Day Total"):

        return 7
    elif(unformated_time == "30 Day Total"):

        return 30
    elif(unformated_time == "Season Total"):

        return "*"
    else:
        print("unrecognized time format!")
        return None
