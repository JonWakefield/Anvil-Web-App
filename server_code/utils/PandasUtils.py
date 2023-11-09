

try:
    import anvil.google.auth, anvil.google.drive, anvil.google.mail
    from anvil.google.drive import app_files
    import anvil.users
    import anvil.tables as tables
    import anvil.tables.query as q
    from anvil.tables import app_tables
    import anvil.server

    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn import model_selection
    from sklearn.preprocessing import StandardScaler
    import seaborn as sns
    import ppscore as pps
    import matplotlib.pyplot as plt
    import pandas as pd
    from sqlalchemy import create_engine
    from scipy.stats import chi2
    from sklearn.covariance import MinCovDet
    from scipy.stats import zscore
    from scipy.stats import shapiro
    from scipy.stats import normaltest
    from scipy.stats import anderson
    from PIL import Image
    from pdf2image import convert_from_path
except (ModuleNotFoundError) as merr:
    print("Module not found in PandasUtils.py.\n{merr}")

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

class PandasUtils:
    def __init__(self):
        pass

    # Function to generate synthetic data
    def generate_data(self, num_samples=1000):
        data = {
            'id': range(1, num_samples + 1),
            'user': np.random.randint(1, 100, num_samples),
            'movie': np.random.randint(1, 100, num_samples),
            'rating': np.random.randint(1, 6, num_samples)
        }
        df = pd.DataFrame(data)
        return df

    # Function to extract column names
    def extract_column_names(self, df):
        return list(df.columns)

    # Function to get the number of unique elements in a column
    def get_num_elements_in_column(self, df, column):
        return df[column].nunique()

    # Function to read a CSV file into a DataFrame
    def read_csv2df(self, file_path):
        df = pd.read_csv(file_path)
        return df

    # Function to write a DataFrame to a CSV file
    def write_df2csv(self, df, file_path):
        df.to_csv(file_path, index=False)

    def df2csv_string_list(self, df):
        # Convert DataFrame to CSV string
        csv_string = df.to_csv(index=False)
        # Split the CSV string into a list of lines
        csv_string_list = csv_string.split('\n')
        return csv_string_list

    def pdf2image(self, pdf_path, image_output_path):
        # Convert the PDF to a sequence of PIL Image objects
        images = convert_from_path(pdf_path)

        return images #returns a list of images (1 for each page in pdf)

    # Function to read a SQL database into a DataFrame
    def read_sql2df(self, query, connection_string):
        engine = create_engine(connection_string)
        df = pd.read_sql_query(query, engine)
        return df

    # Function to write a DataFrame to a SQL database
    def write_df2sql(self, df, table_name, connection_string, if_exists='fail'):
        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)

    # Function to print top or tail rows of the dataframe as a list of strings
    def print_rows(self, df, n, top=True):
        df_head_tail = df.head(n) if top else df.tail(n)
        rows_as_strings = df_head_tail.to_string(index=False).split('\n')
        return rows_as_strings

    def compute_mean(self, df, column):
        # Convert the column to numeric, turning badly formed data into NaN
        df[column] = pd.to_numeric(df[column], errors='coerce')
        
        # Compute the mean, automatically ignoring missing values
        mean_value = df[column].mean()

        return mean_value

    def compute_statistics(self, df, column):
        # Convert the column to numeric, turning badly formed data into NaN
        df[column] = pd.to_numeric(df[column], errors='coerce')
        
        # Compute various statistics, automatically ignoring missing values
        mean_value = df[column].mean()
        median_value = df[column].median()
        mode_value = df[column].mode().values[0]  # The mode method returns a series, get the first value
        std_dev = df[column].std()
        min_value = df[column].min()
        max_value = df[column].max()
        quartiles = df[column].quantile([0.25, 0.5, 0.75]).values  # 25th percentile (Q1), median (Q2), 75th percentile (Q3)

        # Format the results as strings
        results = [
            "Mean: {:.2f}".format(mean_value),
            "Median: {:.2f}".format(median_value),
            "Mode: {:.2f}".format(mode_value),
            "Standard Deviation: {:.2f}".format(std_dev),
            "Minimum: {:.2f}".format(minimum),
            "Maximum: {:.2f}".format(maximum),
            "Q1: {:.2f}".format(quartiles[0]),
            "Q2: {:.2f}".format(quartiles[1]),
            "Q3: {:.2f}".format(quartiles[2])
        ]
        
        return results


    # Function to clean data in a dataframe
    def clean_data(self, df, method='option_NAN'):
        if method == 'option_NAN':
            # Replace non-numeric values with NaN in numeric columns
            df = df.apply(pd.to_numeric, errors='coerce')
        elif method == 'option_MEAN':
            # Replace non-numeric values with NaN in numeric columns and then fill NaN with column mean
            df = df.apply(pd.to_numeric, errors='coerce')
            df = df.fillna(df.mean())
        else:
            raise ValueError("method must be either 'option_NAN' or 'option_MEAN'")
        
        return df

    #this is a multivariate method; takes into account covariance between columns (so won't work on single column)
    def replace_outliers_mahalanobis(self, df, replace_option):
        # First, we need to compute the Mahalanobis distance for each point in the dataset
        # This requires a covariance matrix, which should be robust to outliers
        robust_cov = MinCovDet().fit(df)

        # Calculate the Mahalanobis distance
        mahalanobis_distance = robust_cov.mahalanobis(df)

        # Calculate the threshold for the Mahalanobis distance (chi-square distribution)
        threshold = chi2.ppf((1 - 0.001), df=df.shape[1])  # 0.001 is the outlier level, df.shape[1] is the degrees of freedom

        # Identify the outliers
        outliers = np.where(mahalanobis_distance > threshold)

        # Depending on the replace_option, replace the outliers with either NaN or the column mean
        if replace_option.lower() == "replacenan":
            df.iloc[outliers] = np.nan
        elif replace_option.lower() == "replacemean":
            for col in df.columns:
                df.loc[outliers, col] = df[col].mean()

        return df

    #single column outlier replacement (mean or NAN) using Z-score method
    def replace_outliers_zscore(self, df, column, replace_option):
        # Calculate the Z-score of each value in the column
        z_scores = zscore(df[column])
        
        # Identify the outliers
        outliers = np.where(np.abs(z_scores) > 3)  # Threshold = 3 standard deviations

        # Depending on the replace_option, replace the outliers with either NaN or the column mean
        if replace_option.lower() == "replacenan":
            df.loc[outliers, column] = np.nan
        elif replace_option.lower() == "replacemean":
            df.loc[outliers, column] = df[column].mean()

        return df

    #single column outlier replacement (mean or NAN) using IQR method
    def replace_outliers_iqr(self, df, column, replace_option):
        # Calculate Q1 and Q3
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        
        # Calculate the IQR
        IQR = Q3 - Q1
        
        # Define the upper and lower bounds for outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Identify the outliers
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        # Depending on the replace_option, replace the outliers with either NaN or the column mean
        if replace_option.lower() == "replacenan":
            df[column] = df[column].where((df[column] > lower_bound) & (df[column] < upper_bound), np.nan)
        elif replace_option.lower() == "replacemean":
            mean_value = df[column].mean()
            df[column] = df[column].where((df[column] > lower_bound) & (df[column] < upper_bound), mean_value)
        
        return df

    def test_normality_anderson(self, df, column):
        # Perform the Anderson-Darling test for normality
        result = anderson(df[column])

        print('Statistic: %.3f' % result.statistic)

        # interpret
        p = 0.05
        for i in range(len(result.critical_values)):
            sl, cv = result.significance_level[i], result.critical_values[i]
            if result.statistic < cv:
                return 'Sample looks Gaussian at the %.1f%% level (fail to reject H0)' % sl
            else:
                return 'Sample does not look Gaussian at the %.1f%% level (reject H0)' % sl


    def test_normality_shapiro(self, df, column):
        # Perform the Shapiro-Wilk test for normality
        stat, p = shapiro(df[column])
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        
        # interpret
        alpha = 0.05
        if p > alpha:
            return 'Sample looks Gaussian (fail to reject H0)'
        else:
            return 'Sample does not look Gaussian (reject H0)'

    def test_normality_dagostino(self, df, column):
        # Perform the D'Agostino's K-squared test for normality
        stat, p = normaltest(df[column])
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        
        # interpret
        alpha = 0.05
        if p > alpha:
            return 'Sample looks Gaussian (fail to reject H0)'
        else:
            return 'Sample does not look Gaussian (reject H0)'

    #attempts to transform data so that it's normally distributed
    #uses 3 different methods; if this fails, use non-parametric method
    def transform_and_test(self, df, column):
        # Add a constant to the data to ensure it is all positive
        df[column] = df[column] - df[column].min() + 1

        # Try log transformation
        df[column+'_log'] = np.log(df[column])
        stat, p = shapiro(df[column+'_log'])
        if p > 0.05:
            return 'Log transformation made the data normal'
        
        # Try square root transformation
        df[column+'_sqrt'] = np.sqrt(df[column])
        stat, p = shapiro(df[column+'_sqrt'])
        if p > 0.05:
            return 'Square root transformation made the data normal'
        
        # Try Box-Cox transformation
        df[column+'_boxcox'], _ = boxcox(df[column])
        stat, p = shapiro(df[column+'_boxcox'])
        if p > 0.05:
            return 'Box-Cox transformation made the data normal'
        
        return 'None of the transformations made the data normal; use non-parametric method'


        def normalize_column(self, df, column_name):
            # Create a StandardScaler instance
            scaler = StandardScaler()

            # Fit and transform the column
            df[column_name] = scaler.fit_transform(df[[column_name]])

            return df

    def merge_dfs(self, df1, df2, key, how='inner'):  #uses a key; inner is intersection, outer is union, left uses left df etc
        # Merge df1 and df2 on key
        df_merged = pd.merge(df1, df2, on=key, how=how)
        return df_merged
    
    def concat_dfs(self, df1, df2, axis=1):  #axis=0 (concat vertically; should hae same column name; will add more rows at tail); axis=1 concat horizontally (add a new column)
        df_concat = pd.concat(df1, df2, axis)
        return df_concat

    def remove_column(self, df, column_name):
        if column_name in df.columns:
            df = df.drop(columns=column_name)
            return df
        else:
            print("Column not found in the DataFrame")
            return df

    #test for categorical data; if so and >2 <= max; then one-hot encode for later analysis
    def one_hot_encode(self, df, column, max_categories):
        # Check if the number of unique values in the column is within the defined threshold
        if df[column].nunique() > 2 and df[column].nunique() <= max_categories:
            # Get one-hot encoding of column
            one_hot = pd.get_dummies(df[column], prefix=column)
            
            # Drop column as it is now encoded
            df = df.drop(column, axis=1)
            
            # Join the encoded df
            df = df.join(one_hot)
        return df


    def get_histogram(self, column):
        # Check if the column exists in the DataFrame
        if column not in self.df.columns:
            print(f"Column '{column}' does not exist in the DataFrame.")
            return []

        # Get the counts of each category
        category_counts = self.df[column].value_counts()

        # Convert the counts to a list of strings
        histogram_strings = [f"{category}: {count}" for category, count in category_counts.iteritems()]

        return histogram_strings

    # Function to plot a distribution
    def plot_distribution(self, df, column_name):
        sns.displot(df[column_name])
        plt.show()

    # Function to print out a list of strings
    def print_list(self, lst):
        for element in lst:
            print(element)

    #randomState set to fixed number ensures that each time you run this, the split will be the same; supply different # each time
    #if you want it to mix up splits each time
    #passing in values from the 'y' variable, to stratify, ensures an even data-split; very useful for categorical data 
    def create_test_train_df(self, df, test_split_fraction=0.1, categorical_col_name=None, randomState=42):
        catColName = categorical_col_name
        if not categorical_col_name == None:
            df_train, df_test = model_selection.train_test_split(df, test_size=test_split_fraction, random_state=randomState, stratify=df[catColName].values)
        else:
            df_train, df_test = model_selection.train_test_split(df, test_size=test_split_fraction, random_state=randomState)
           
        return df_train, df_test


