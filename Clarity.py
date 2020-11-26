#!/usr/bin/env python3

import pandas as pd
from os import listdir

def parse_function(file_name, init_datetime, end_datetime, hostname):
    """
    Gets a list of hostnames connected to a given host during the given period
    Args:
        file_name (str): the file of the file to be proceseed
        init_datetime (int): init_datetime in timestamp units
        init_datetime (int): end_datetime in timestamp units
        hostname (str): Hostname

    Returns:
        List: a list of hostnames connected to the given host during the given period
    """


    try:
        filehandle = open(file_name)
    except OSError as error:
        print("# ERROR: cannot open/read file:", file_name, error)
        return

    d = []
    while True:
        line = filehandle.readline()
        if not line:
            break
        myline = line.split()
        if int(myline[0]) >= init_datetime and int(myline[0]) <= end_datetime:
            d.append(
                {
                    'unix_timestamp': myline[0],
                    'hostname1': myline[1].strip(),
                    'hostname2': myline[2].strip()
                }
            )

    filehandle.close()
    new_df = pd.DataFrame(d)
    return new_df[(new_df["hostname1"]==hostname.strip())]["hostname2"].values.tolist()
