#!/usr/bin/python

import os
import sys, getopt
from lib.DecisionTree import DecisionTree

def main(argv):

    ElementNum = 0 
    try:
        opts, args = getopt.getopt(argv,"hn:",["n="])
    except getopt.GetoptError:
        print ("Run.py -n <element number>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("Run.py -n <element number>")
            sys.exit()
        elif opt in ("-n", "--element number"):
            ElementNum = int (arg);


    Dtree = DecisionTree (ElementNum)
    Dtree.BuildTree ()

if __name__ == "__main__":
   main(sys.argv[1:])
