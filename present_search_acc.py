#!/usr/local/bin/python3

import re
import db_search

# Author: Brian Poon
# Class: AS410.712.82
# Term: Spring 2022
# Assignment: Final Project
# Description: Script is used for getting data using 
# the selected tools and databases. 

  
def breakdown_acc(file_path):
    
    # Read each accession
    with open(file_path, 'r') as file:
        line = file.readlines()
        acc_format = re.sub(r'\n|,', ' ', line)

    return acc_format
                
def main(file_path):

    #Use search input to break down the info needed for summary page
    #Determine protein or nucleotide to show which section to use

    #Use db_options to connect to API for DBs
    #Use tool_options to connect to API for tools
    #Print page at very last with all of the outputs

    # Set the necessary information for protein, DNA, and RNA
   
    acc_list = breakdown_acc(file_path)

    return acc_list


if __name__ == '__main__':
    main()
