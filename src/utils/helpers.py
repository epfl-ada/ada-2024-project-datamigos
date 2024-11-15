import datetime
import ast
import pandas as pd
import numpy as np


def convert_to_datetime(date_str):
    """
    Convert a string representing a date into a `datetime` object.

    Arguments:
        date_str : A string representing a date

    Returns:
        A `datetime` object corresponding to the input date string if successfully parsed or None.

    Exceptions:
        The function handles `ValueError` and `TypeError` exceptions to ensure robustness
        against unsupported date formats and None input.

    """
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        try:
            return datetime.datetime.strptime(date_str, '%Y')
        except (ValueError, TypeError):
            try:
                return datetime.datetime.strptime(date_str, '%Y-%m')
            except (ValueError, TypeError):
                return None
            

def extract_list(row, type):
    '''
    Extract the list of values from a dictionary
    
    Arguments:
        row: the row of the dataframe
        type: the type of the column to explode

    Return: 
        List of the values of in dictionary
    '''
    try:
        values_dict = ast.literal_eval(row[type])
        values_list = list(values_dict.values())
        return values_list
    except:
        return np.nan
    
def preprocess_movie_data(df_movie):
    """
    Preprocesses a DataFrame of movie data by cleaning and standardizing key columns.

    Arguments:
        df_movie: A DataFrame containing movie data

    Returns:
        A DataFrame with the following preprocessing steps applied:
            - Rows with missing 'title' values are removed.
            - 'title' values are converted to lowercase and stripped of leading/trailing whitespace.
            - 'release_date' is converted to datetime format; non-convertible dates are set to NaT.
            - Values of 0.0 in 'revenue' and 'runtime' are replaced with NaN, indicating missing data.
    """
    # Drop rows with missing 'title'
    df_movie = df_movie.dropna(subset=['title'])
    
    # Convert 'title' to lowercase and stripping whitespace
    #df_movie.loc[:, 'title'] = df_movie['title'].str.lower().str.strip()
    
    # Convert 'release_date' to datetime
    df_movie.loc[:, 'release_date'] = pd.to_datetime(
        df_movie['release_date'].astype(str).apply(convert_to_datetime), errors='coerce'
    )
    
    # Replace 0.0 with NaN in 'revenue' and 'runtime'
    df_movie.loc[df_movie['revenue'] == 0.0, 'revenue'] = np.nan
    df_movie.loc[df_movie['runtime'] == 0.0, 'runtime'] = np.nan
    
    return df_movie

def get_plot_summary(tconst):
    try:
        movie = ia.get_movie(int(str(tconst)[2:]))
        # Retrieve the plot, if available, or return None
        plot = movie.get("plot")
        if plot:
            return plot[0]  # return the first plot summary
        else:
            return None
    except Exception as e:
        return None