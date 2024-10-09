#!/usr/bin/env python3
## Script to decode the output of /proc/diskstats in the hope
## the output will provide some insights re: performance analysis
##
## Kostas Peletidis, 2024-10-04
##
#### Documentation/admin-guide/iostats.rst ####
## Field  1 -- # of reads completed (unsigned long)
## Field  2 -- # of reads merged, field 6 -- # of writes merged (unsigned long)
## Field  3 -- # of sectors read (unsigned long)
## Field  4 -- # of milliseconds spent reading (unsigned int)
## Field  5 -- # of writes completed (unsigned long)
## Field  6 -- # of writes merged  (unsigned long)
## Field  7 -- # of sectors written (unsigned long)
## Field  8 -- # of milliseconds spent writing (unsigned int)
## Field  9 -- # of I/Os currently in progress (unsigned int)
## Field 10 -- # of milliseconds spent doing I/Os (unsigned int)
## Field 11 -- weighted # of milliseconds spent doing I/Os (unsigned int)
## Field 12 -- # of discards completed (unsigned long)
## Field 13 -- # of discards merged (unsigned long)
## Field 14 -- # of sectors discarded (unsigned long)
## Field 15 -- # of milliseconds spent discarding (unsigned int)
## Field 16 -- # of flush requests completed
## Field 17 -- # of milliseconds spent flushing
####
import sys
DATA_FILE = '/proc/diskstats'

fnames = ['MajorNum:',
          'MinorNum:',
          'DeviceName:',
          'ReadsCmpltd:',
          'ReadsMerged:',
          'SectorsRead:',
          'Read_ms:',
          'WritesCmpltd:',
          'WritesMerged:',
          'SectorsWritten:',
          'Write_ms:',
          'IOCurr:    ',
          'IO_ms:    ',
          'IO_ms_weighted:',
          'DiscardsCmpltd:',
          'DiscardsMerged:',
          'SectorsDiscrd:',
          'Discard_ms:',
          'FlushCompl:',
          'Flush_ms:']
###
# Function to parse a diskstats line and extract the device name
# and its major and minor numbers.
# Input: stat_line - A list of strings. Each string is a value from
#                    /proc/diskstats or of similar format
# Returns: A 3-tuple (device_name, major_number, minor_number)
###
def get_dev_name(stat_line):
    (major_number, minor_number, device_name) = stat_line[:3]
    return((device_name, major_number, minor_number))


###
## Function to print the device name, major and minor number from a
## 3-tuple of strings/
## Input: dev_info - A 3-tuple of strings
##        (device_name, major_number, minor_number) 
## Returns: N/A
###
def print_dev_name(dev_info):
    print(dev_info[0], '(' + dev_info[1] + ', ' + dev_info[2] + ')')


###
## Function to take counter values and print them together with each
## counter's name, one name:value pair per line.
## The input data is a list of strings.
## Input: counters - A list of strings (counter values)
## Returns N/A
###
def print_dev_counters(counters):
    global fnames

    for field in range(3, (len(counters))):
        print(fnames[field] + '\t' + counters[field])
    print('\n')


### Main function ###
def main():
    show_all = True

    if len(sys.argv) > 1:
        show_all = False

    with open(DATA_FILE, 'r') as fp:
        data = fp.read()

    # Create the list of stats. Each line of stats is a list of values
    lstats = list()
    for line in data.split('\n'):
        if line:
            lstats.append(line.split())

    for line in lstats:
        if (show_all == False) and (line[2] not in sys.argv):
            continue
        dev_info = get_dev_name(line)
        print_dev_name(dev_info)
        print_dev_counters(line)

    sys.exit(0)


if __name__ == "__main__":
    main()

