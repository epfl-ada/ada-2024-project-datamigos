import datetime
import ast
import re
import pandas as pd
import numpy as np

def assign_side(movies_df, countries, relevance_nb=10, relevance_diff=10, threshold=19):
    """
    Assigns a Cold War side (Western, Eastern, or None) to each country based on the prevalence of films 
    aligned with each side in a dataset.

    Parameters:
        movies_df: A dataframe containing movie data. Must include the following columns:
            - `countries`: A list of strings representing the countries producing each film.
            - `cold_war_side`: A string representing the Cold War alignment of the film ('Western', 'Eastern', or 'None').
        relevance_nb: The minimum number of films required for a country to be assigned either 'Western', 'Eastern' or 'None'.
                      If a country's total count of films is less than this value, it is assigned 'Lack of data'.
                      Defaults to 10.
        relevance_diff: The minimum number of films required for a country to be assigned either 'Western' or 'Eastern'.
                      If a country's total count of 'Western' or 'Eastern' films is less than this value, it is assigned 'None'.
                      Defaults to 10.
        countries: A list of country names for which the Cold War side alignment needs to be determined.
        threshold: The minimum percentage difference between the number of Western and Eastern aligned films 
                   required to classify a country as either 'Western' or 'Eastern'. Defaults to 19%.

    Returns:
        A dictionary where the keys are country names and the values are their assigned Cold War side.

    Notes:
        - If a country has no films associated with a Cold War side, it is assigned to 'None'.
        - The function calculates the percentage difference between the number of Western and Eastern aligned films 
          for each country and compares it to the threshold to determine the alignment.
        """
    country_cold_war_side = {}

    for country in countries:
        # Get the 'cold_war_side' counts for the country in `movies`
        sides = movies_df.loc[movies_df['countries'].apply(lambda x: country in x), 'cold_war_side'].values
        west_count = (sides == 'Western').sum()
        east_count = (sides == 'Eastern').sum()
        total_count = len(sides)

        total_count_without_none = west_count + east_count
        if total_count < relevance_nb:
            country_cold_war_side[country] = 'Lack of data'
        elif total_count_without_none < relevance_diff and total_count >= relevance_nb:
            country_cold_war_side[country] = 'None'
        else:
            # Calculate the percentage difference
            percentage_difference = abs(west_count - east_count) / total_count_without_none * 100
            
            # Assign the corresponding side to the country
            if percentage_difference < threshold or west_count == east_count:
                country_cold_war_side[country] = 'None'
            elif west_count > east_count:
                country_cold_war_side[country] = 'Western'
            elif west_count < east_count:
                country_cold_war_side[country] = 'Eastern'
    
    return country_cold_war_side

def convert_csv(df):
    for col in df.columns:
        try:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        except:
            pass
    return df


def clean_column_values(value):
    '''
    Clean the value of a column by removing special characters and turn it into a list of strings.

    Arguments:
        value (str): the value to clean 
    
    Return:
        the cleaned value (list(str))
    '''
    if isinstance(value, float):
        return np.nan
    else:
        # Remove leading and trailing whitespaces
        value = value.strip()
        # Remove all special characters
        value = re.sub(r'[[\]"\']+', '', value)
        # Remove the word "language" from the string
        pattern = re.compile(r'\b(\w+)language\b')
        value = pattern.sub(r'\1', value)
        return [item.strip() for item in value.split(",")]

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
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        try:
            return datetime.datetime.strptime(date_str, "%Y")
        except (ValueError, TypeError):
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m")
            except (ValueError, TypeError):
                return None


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
    # df_movie.loc[:, 'title'] = df_movie['title'].str.lower().str.strip()

    # Convert 'release_date' to datetime
    df_movie.loc[:, 'release_date'] = pd.to_datetime(
        df_movie['release_date'].astype(str).apply(convert_to_datetime), errors='coerce'
    )

    # Replace 0.0 with NaN in 'revenue' and 'runtime'
    df_movie.loc[df_movie['revenue'] == 0.0, 'revenue'] = np.nan
    df_movie.loc[df_movie['runtime'] == 0.0, 'runtime'] = np.nan

    return df_movie
