import os.path
import pandas as pd

def test_data_columns(path):
    """Function to test if the data has the correct number of columns"""
    df = pd.read_csv(path, sep=" ", header=None)
    len(df.columns)
    assert (len(df.columns) == 3), "The file seems to be wrong. The function expects 3 columns"

test_data_columns(os.path.dirname(__file__))