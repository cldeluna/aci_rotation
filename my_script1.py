#!/usr/bin/python -tt
# my_script1
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/11/16  12:20 PM"
__copyright__ = "Copyright (c) 2015 Claudia"
__license__ = "Python"


def newfunction():


# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '\nUsage:python my_script1 <Argument 1>\nExample: python my_script1 "/fill in"\n\nNote: Fill in.\n\n'
        sys.exit()
    else:
        main()
