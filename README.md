#### Clarity - Backend code challenge

These scripts can be used to parse log files.

The main functions are:
- function parse_function: Given a host and a period of time,  the function returns a list of the hosts connnected to this host in a given period of time [L27](https://github.com/roconmo/Log_parser/blob/fc2dd50bd274def22c62210c1f071bdf19ed6ba1/src/Log_parser.py#L27).
- function unlimited_input_parser: The idea of this function is to run every hour. The log is processed from the back because I assume that the timestamp is synchronized with the server time. This 
function has an optiomal param called wait, by default indicates 3600 seconds and it is running indefinitibly until the script is stopped [L92](https://github.com/roconmo/Log_parser/blob/fc2dd50bd274def22c62210c1f071bdf19ed6ba1/src/Log_parser.py#L92):

In order to control the arguments, the user has to indicate **interval** to run the parse_function() and **unlimited** to run the unlimited_input_parser(). 

There are 6 args:

    * runmode: interval to run the parse_funciton or unlimited for the unlimites_input_parser.

    * logfile: path to the log file.

    * --init_time: begin of the period. 

    * --end_time: end of the period.

    * --host_conn: the name of the host connected to a given host. The second column represents this host.

    * --host_rec_conn: the name of host that receives a connection. The third column of the log represents this host.
    
I've made an assumption: local time is same in server.

Examples to run the scripts in python:
``` 
$ python3 src/Log_parser.py -h

$ python3 src/Log_parser.py interval src/data/input-file-10000.txt --end_time 1565647204351 --init_time 1565733598341 --host_conn Loreto 

$ python3 src/Log_parser.py unlimited src/data/input-file-10000.txt --host_conn Cherena --host_rec_conn Olvin 
```

To run the tests ``` $ python3 tests/tests.py ```

The test check the help, a bad logfile, wrong dates and the parse_function with some params.
Also, I run the script with Travis CI: [![Build Status](https://travis-ci.com/roconmo/Log_parser.svg?branch=main)](https://travis-ci.com/roconmo/Log_parser)
