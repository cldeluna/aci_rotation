#!/usr/bin/python -tt
# ver_check
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/14/16  8:46 AM"
__copyright__ = "Copyright (c) 2015 Claudia"
__license__ = "Python"

import sys


def main():


# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '\nUsage:python ver_check <Argument 1>\nExample: python ver_check "/fill in"\n\nNote: Fill in.\n\n'
        sys.exit()
    else:
        main()
