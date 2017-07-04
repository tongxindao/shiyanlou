#! /usr/bin/env python3
import os
import sys

def parse_file(path):
    """
    Analisys text file,return space, tab, row and so on.
    :arg path: parse text file path
    :return: include count space, tab, row and so on for tuple
    """
    fd = open(path)
    i = 0
    spaces = 0
    tabs = 0
    for i,line in enumerate(fd):
        spaces += line.count(' ')
        tabs += line.count('\t')
    # Now,close you opened text file
    fd.close()
    # return tuple
    return spaces, tabs, i + 1

def main(path):
    """
    this function is print parse text file result
    :arg path: request text file's path
    :return: if this file exist,return True,else False
    """
    if os.path.exists(path):
        spaces, tabs, lines = parse_file(path)
        print("Spaces {}. tabs {}. lines {}".format(spaces, tabs, lines))
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        sys.exit(-1)
    sys.exit(0)
