# Clarity_test
Clarity - Backend code challenge

These scripts can be used to parse log files.

function parse_function: receives a host name and the function returns a list of the hosts connnected to this host in a given period of time.

There are 5 params:
    --path: 
    --init_time
    --end_time
    --host_conn
    --host_rec_conn

Example: $ python Log_parser.py --path C:/Users/rosal/Documents/python/Clarity/Git/Clarity_test/src/data/input-file-10000.txt --init_time 1565647204351 --end_time 1565733598341 --host_conn Loreto --host_rec_conn Genysis

