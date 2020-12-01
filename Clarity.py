#!/usr/bin/env python3 
import pandas as pd
import os
from os import listdir
import time
from datetime import datetime
import operator

def get_data(path):
    """
    Function that retrieves a TextIOWrapper
    Args:
        path: an aboslute path
    Return: 
        TextIOWrapper with all the text file data
    """
    try:
        filehandle = open(path)
        return filehandle
    except OSError as error:
        print("# ERROR: cannot open/read file:", file_name, error)
        return "" 
		
def parse_function(path, init_datetime, end_datetime, hostname):
    """
    Retrieves a list of hostnames connected to a given host during the given period
    Args:
        file_name (str): the name of the file to be proceseed
        init_datetime (int): init_datetime in timestamp units
        init_datetime (int): end_datetime in timestamp units
        hostname (str): Hostname to look for in the given period
    
    Returns:
        List: a list of hostnames connected to the given host during the given period
    """
    with get_data(path) as filehandle:
        #filehandle = get_data(path)
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

        new_df = pd.DataFrame(d)
    return new_df[(new_df["hostname1"]==hostname.strip())]["hostname2"].values.tolist()

def convert_timestamp_to_secs(timestamp):
    """
    Functions that convert a 13 characters timestamp to seconds from epoch
    Args:
        timestamp (int): The timestamp to be converted
    Returns:
        int: Seconds since epoch
    """
    dt = datetime.fromtimestamp(timestamp / 1000)
    formatted_time = dt.isoformat(sep=' ', timespec='milliseconds')
    d = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S.%f')
    return round(time.mktime(d.timetuple()))
	
def most_connected_hostname(my_dictionary):
    """
    Retrieves a list with the most connected hosts
    Args: 
        my_dictionary (dict): collection of hosts with the number of connections in 60 minutes
    Returns:
        list: collection of mos connected hosts
    """
    max_key = max(my_dictionary.items(), key=operator.itemgetter(1))[1]
    hostname_list = [host for host, val in my_dictionary.items() if val == max_key]
    return list(hostname_list)

def collect_input(path, given_host, given_connected_host):
    """
    Retrieves a list of hostnames connected and that received connections from a given_host and a list of the host with most connections 
    Args:
        path (str): absolute path
        given_host (str): 
        given_connected_host (str): 
    Returns:
        list: list of hostnames connected to a given_host during the last hour
        list: list of hostnames received connections from a given_host
        list: the hostname that generated most connections in the last hour
        
    """
    list_host_connected = []
    list_host_receive_conections = []
    hostnames = {}
    hostname_list = []
    one_hour_secs = 3600
    
    with get_data(mypath) as filehandle:
        for cnt, line in enumerate(reversed(list(filehandle))):
            if cnt == 0: starting_point = convert_timestamp_to_secs(int(line.split()[0]))
            myline = line.split()
            time_in_secs = starting_point - convert_timestamp_to_secs(int(myline[0]))
            
            if time_in_secs >= one_hour_secs:
                break
            if myline[1] == given_host:
                if myline[2] not in list_host_connected:
                    list_host_connected.append(myline[2])
					
            #check if hostname receives connection from a given host exists in the list, if not, we add it
            if myline[2] == given_connected_host:
                if myline[1] not in list_host_receive_conections:
                    list_host_receive_conections.append(myline[1])
            #fill a dictionary counting the hostnames connections
            hostnames[myline[1]] = hostnames.get(myline[1], 0) + 1
    
    return list_host_connected, list_host_receive_conections, most_connected_hostname(hostnames)
