#!/usr/bin/env/ python3

import sys

print("sys\'s arg count: {0}".format(len(sys.argv)))

if __name__ == "__main__":
    for arg in sys.argv:
        print("sys\'s arg is: {0}".format(arg))