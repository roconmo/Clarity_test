#!/usr/bin/env python3

# Tests the main script with several inputs

import os.path
import errno
import subprocess

src_dir = os.path.join( os.path.dirname(os.path.abspath(__file__)), '../src/')
main_script = os.path.join( src_dir, 'Log_parser.py')
sample_log = os.path.join( src_dir, 'data/input-file-10000.txt');

tests = {
    'help' : main_script + ' -h',
    'badlog' : main_script + 
        ' interval input-file-10000.txt --init_time 1 --end_time 2 --host_conn Loreto',
    'badtimes' : main_script + ' interval ' + sample_log + 
        ' --init_time 2 --end_time 1 --host_conn Loreto',
    'interval' : main_script + ' interval ' + sample_log + 
        ' --init_time 1565647204351 --end_time 1565733598341 --host_conn Loreto',

    # not a good idea for a test, as it only terminates when killed
    #'unlimited' : main_script + ' unlimited ' + sample_log + 
    #    ' --host_conn Cherena --host_rec_conn Olvin'
}

for name in tests:
    cmd = 'python ' + tests[name]
    print("### ", name)
    try:
        osresponse = subprocess.check_call(cmd.split())
    except subprocess.CalledProcessError as err:
        print("# ERROR: failed test", name, cmd, err.returncode)

