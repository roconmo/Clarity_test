def test_data_columns(path):
    """Function to test if the data has the correct number of columns"""
    df = pd.read_csv(mypath, sep=" ", header=None)
    len(df.columns)
    assert (len(df.columns) == 3), "The file seems to be wrong. The function expects 3 columns"

def test_path_exists(path):
      """Function to check if the path exists"""
    assert (os.path.exists(mypath) == True), "The provided path doesn't exist"

def test_hostname1_exists(df, hostname1):
     """Function to check if the path exists"""
    assert (((df[1] == hostname)).any()), "The provided hostname1 doesn't exist"

def test_hostname2_exists(df, hostname2):
     """Function to check if the hostname2 exist in the file"""
    assert (((df[2] == hostname)).any()), "The provided hostname2 doesn't exist"

def test_check_results(path):
     """Function to check  the results given some params"""
    expected_output = ['Genysis', 'Arriana', 'Porcha']
    mypath = "C:/Users/rosal/Documents/python/Clarity/data/input-file-10000.txt"
    init_datetime = 1565647204351
    end_datetime = 1565733598341
    hostname = "Loreto    "
    test_output = parse_function(path, init_datetime, end_datetime, hostname)
    assert (test_output == expected_output), "The results are wrong, please make sure you are using the correct file"
