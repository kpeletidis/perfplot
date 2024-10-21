#!/usr/bin/env python3
## Script to compare two lines of /proc/diskstats and display
## the differences as percentages.
##
## Kostas Peletidis, 2024-10-14
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

fnames = ['MajorNum:\t',
          'MinorNum:\t',
          'DeviceName:\t',
          'ReadsCmpltd:\t',
          'ReadsMerged:\t',
          'SectorsRead:\t',
          'Read_ms:\t',
          'WritesCmpltd:\t',
          'WritesMerged:\t',
          'SectorsWritten:\t',
          'Write_ms:\t',
          'IOCurr:\t\t',
          'IO_ms:\t\t',
          'IO_ms_weighted:\t',
          'DiscardsCmpltd:\t',
          'DiscardsMerged:\t',
          'SectorsDiscrd:\t',
          'Discard_ms:\t',
          'FlushCompl:\t',
          'Flush_ms:\t']
###
# Function to print a brief description of usage
###
def show_usage():
    print(f'Usage: {sys.argv[0]} <file_1> <file_2>')
    print('\nWhere file_1 and file_2 are data files in the format of'\
            ' /proc/diskstats')


###
# Function to calculate the difference of two numbers as a percentage
# rounded to two decimal places.
# Input: old - First value to compare (float)
#        new - Second value to compare (float)
# Returns: perc - Percentage difference (float)
###
def diff_percentage(old, new):
    perc = float()
    if old != 0:
        perc = round((((new-old)*100)/old), 2)
    else:
        return None
    
    return perc


###
# Function that parses a diskstats line and returns the device name.
# Input: stat_line - A list of strings. Each string is a value from
#                    /proc/diskstats or of similar format
# Returns: dev_name - A string
###
def get_dev_name(stat_line):
    dev_name = stat_line[2]
    return(dev_name)


###
# Function to read diskstats data from a file into a list.
# The list contains lists of strings (the values), one per line.
## Input: infile - Input file with diskstats data
## Returns: data - A list of lists of strings
###
def read_data(infile):
    data = list()

    ##TODO: handle exceptions
    with open(infile, 'r') as fp:
        temp = fp.read()

    for line in temp.split('\n'):
        if line:
            data.append(line.split())

    return data


### Main function ###
def main():

    if len(sys.argv) != 3:
        show_usage()
        sys.exit(1)

    data1 = read_data(sys.argv[1])
    data2 = read_data(sys.argv[2])

    header_out = str()
    data_out = list()
    for (v1, v2) in zip(data1, data2):
        name1 = get_dev_name(v1)
        name2 = get_dev_name(v2)
        header_out = '\n\t\t\t' + name1.rjust(10) + '\t' + name2.rjust(10)\
                    + '\t' + '%'.rjust(3)
        print(header_out)

        for (f, left, right) in zip(fnames[3:], v1[3:], v2[3:]):
            rleft = left.rjust(10)
            rright = right.rjust(10)
            if float(left) != 0:
                dp = str(diff_percentage(float(left), float(right)))
            else:
                dp = '-'
            tmp_str = f + '\t' + rleft + '\t' + rright + '\t' + dp
            #print(tmp_str)
            #print(f, '\t', rleft, '\t', rright, '\t', dp)
            data_out.append(tmp_str)
        
        for line in data_out:
            print(line)
        data_out = []

    sys.exit(0)


if __name__ == "__main__":
    main()

