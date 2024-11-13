import datetime
import ast


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
        return list(values_dict.values())
    except:
        return []