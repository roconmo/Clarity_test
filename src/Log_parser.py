#!/usr/bin/env python3

import argparse
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
    return new_df[(new_df["hostname1"] == hostname.strip())]["hostname2"].values.tolist()


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
    Retrieves a list with the most connected hosts and number of connections
    Args: 
        my_dictionary (dict): Hosts with number of connections in an hour
    Returns:
        list: collection of most connected hosts and number of connections
    """

    if my_dictionary:
        max_key = max(my_dictionary.items(), key=operator.itemgetter(1))[1]
        hostname_list = [host for host,
                     val in my_dictionary.items() if val == max_key]
        return list(hostname_list), max_key
    else:
        return ''


def unlimited_input_parser( path, given_host, given_connected_host, waits=3600):
    """
    Produces lists of hostnames connected and of hostnames that received connections
        from a given_host and a list of the host with most connections
    Args:
        path (str): path to logfile
        given_host (str): name of hostname
        given_connected_host (str): name of hostname
        waits (int); seconds to wait between reports
    
    Every waits param  it will print three csv lines:
        1) list of hostnames connected to a given_host during the last hour
        2) list of hostnames received connections from a given_host
        3) the hostname that generated most connections in the last hour

    """

    while True:
        # get current time in seconds,
        # Note: assumes local time is same in server
        curr_time = int(round(time.time()))

        # read logfile from end until timestamp older than waits param
        list_host_connected = []
        list_host_receive_conections = []
        hostnames = {}
        hostname_list = []

        with get_data(path) as filehandle:
            for cnt, line in enumerate(reversed(list(filehandle))):
                myline = line.split()

                # stop if log entry too old
                log_time = convert_timestamp_to_secs(int(myline[0]))
                age = curr_time - log_time
                if age > waits:
                    break

                # parse log line
                if myline[1] == given_host:
                    if myline[2] not in list_host_connected:
                        list_host_connected.append(myline[2])

                # check hostname that receives connection, add it if new
                if myline[2] == given_connected_host:
                    if myline[1] not in list_host_receive_conections:
                        list_host_receive_conections.append(myline[1])

                # count hostname connections
                hostnames[myline[1]] = hostnames.get(myline[1], 0) + 1
            
            # print report in CSV format
            print("%d,hosts_connected,%s" % (curr_time,",".join(list_host_connected)))
            print("%d,hosts_received_connections,%s" % (curr_time,",".join(list_host_receive_conections)))
            print("%d,most_connected_host,%s" % (curr_time,most_connected_hostname(hostnames)))

        # close file and sleep for waittime
        filehandle.close()
        time.sleep(waits)  
  
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("runmode",
                        help="Parser mode: interval or unlimited")
    parser.add_argument("logfile",
                        help="Path to the logfile")
    parser.add_argument("--init_time",
                        help="Init datetime in Timestamp format [interval]", type=int)
    parser.add_argument("--end_time",
                        help="End datetime in Timestamp format  [interval]", type=int)
    parser.add_argument("--host_conn",
                        help="Host that connects                [interval|unlimited]")
    parser.add_argument("--host_rec_conn",
                        help="Host that receives connections    [unlimited]")

    args = parser.parse_args()

    if not os.path.isfile(args.logfile):
        print("# The path to the log file is not valid")
    else:
        if args.runmode == 'interval':
            if args.logfile and args.init_time and args.end_time and args.host_conn:
                if args.init_time > args.end_time:
                    print("# init_time has to be lower than end_time") 
                else:
                    print("# parsing log connections (interval)")
                    sequence_hostnames = parse_function(
                        args.logfile, args.init_time, args.end_time, args.host_conn)
                    if len(sequence_hostnames) == 0:
                        print("# ERROR: cannot parse ", args.logfile)
                    else:
                        print("# a list of hostnames {}".format(sequence_hostnames))
            else:
                print("# ERROR: need arguments logfile, init_time, end_time and host_conn")
        elif args.runmode == 'unlimited':
            if args.logfile and args.host_rec_conn and args.host_conn:  
                print("# parsing log connections (unlimited)")
                unlimited_input_parser(
                    args.logfile, args.host_conn, args.host_rec_conn)  
            else:
                print("# ERROR: need arguments logfile, host_rec_conn and host_conn")
        else:
            print("# ERROR: only two runmodes supported: interval or unlimited")

if __name__ == "__main__":
    main()

