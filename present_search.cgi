#!/usr/local/bin/python3

import cgi
import cgitb
from datetime import datetime
import os
import sys
from tokenize import String
import jinja2
import mysql.connector

# Author: Brian Poon
# Class: AS410.712.82
# Term: Spring 2022
# Assignment: Final Project
# Description: This will run when the submission button is hit 
# on the main page of the search. 

def load_template():
    # Delcaring the FASTA file to be used and opening the file, which
    # must be in the same directory as this script given the filepath.
    file_fasta = './data/e_coli_k12_dh10b.faa'
    open_fasta = open(file_fasta)

    # Directing the template filepath for template loader
    templateLoader = jinja2.FileSystemLoader(searchpath='./templates')

    # Creating the environment to take the template loader and load
    # a specfic template in the folder.
    env = jinja2.Environment(loader=templateLoader)
    template = env.get_template('unit04.html')

    # Counter for entries that will limit results to 20 entries 
    # from the FASTA file.
    entry_counter = 0

    # This list will contain the index of records or rows in the HTML
    # that will be displayed. 
    index_num = []

    # This list will contain the ID of the genes in the FASTA file.
    gene_id = {}

    # This list will contain the sequence lengths for the FASTA entry.
    sequence_length = {}

    # This list will contain the remaining header information.
    header_info = {}

    # This Boolean will help determine when the reading starts
    start_key = False

    for line in open_fasta:

        # Identify lines that the record will begin at.
        if line.startswith('>'):
            start_key = True
            
            # Once the entry hits the maximum desired, break the loop.
            if entry_counter == 20:
                break
            
            # Start the record based on index = 1
            entry_counter = entry_counter + 1
            index_num.append(entry_counter)

            # Initiate 0 in list of length based on record number.
            sequence_length[entry_counter] = 0
            
            # Remove the newline and '>' character. Extract the header 
            # information with rsplit.
            line = line.rstrip('\n').rstrip('>')
            header = line.rsplit('|')

            # Rejoin the information for just the gene that's split 
            # and insert into the list according to the entry counter.
            gene = '|'.join([header[i] for i in [0,1,2,3]])
            gene_id[entry_counter] = gene

            # Get header information, strip the whitespace on the left,
            # and insert into header_info list according to entry counter.
            info = header[4].lstrip()
            header_info[entry_counter] = info

            # This will ensure that headers are not going to be counted 
            # in counting total length below.
            continue

        # Begin processing the length of sequence.
        if start_key == True:
            line = line.rstrip('\n')
            line_sum = len(line)
            current = sequence_length.get(entry_counter)
            sequence_length.update({entry_counter : current + line_sum})

    # Good habits of closing the file at the end.
    open_fasta.close

    # Send the information to HTML by referencing the variables 
    # to pass between CGI and HTML.
    print("Content-Type: text/html\n\n")
    print(template.render(geneID=gene_id, rec = index_num, 
        seq_len=sequence_length, header=header_info))


def main():

    # Create the desired connection and cursor.
    conn = mysql.connector.connect(user='bpoon1', password='Testing123',
                                   host='localhost', database='bpoon1')
    cursor = conn.cursor()

    # To help with troubleshooting passing of values
    cgitb.enable(display=0, logdir="/path/to/logdir")

    # Create a dictionary of all the element IDs for tools and databases
    tool_id = ['cbx_blast', 'cbx_orffinder', 'cbx_splign', 'cbx_igv']
    db_id = ['cbx_genbank', 'cbx_ensembl', 'cbx_omim']

    # Create an pointer to the submitted form and get values
    form = cgi.FieldStorage()
    search_type = form.getvalue('submit_now_type')

    # Create empty list of tools and databases chosen for. Also create
    # other starting variables that would be used. UID will be the IP
    # address obtaind by REMOTE_ADDR in the format date::IP::time
    input_tools = []
    input_db = []
    input_statement = '++tools++'
    date_time= datetime().now()  
    uid = str(date_time.date())+'::'+os.environ["REMOTE_ADDR"]+'::'+str(date_time.time())

    for i in range(len(tool_id)):
        
        a = form.getvalue(tool_id[i])
        
        if a == True:
            input_tools.append(tool_id[i])
            input_statement = input_statement + tool_id[i]+'+'

    input_statement = input_statement + '++db++'
    for i in range(len(db_id)):

        a = form.getvalue(db_id[i])

        if a == True:
            input_db.append(db_id[i])
            input_statement = input_statement + db_id[i]+'+'

    # Based on whether it is an accession or a sequence it forks.
    if (search_type == "s"):
        sequence = form.getvalue('input_sequence')
        input_statement = input_statement + '++seq++' + sequence
    
    if (search_type == "a"):
        accession = form.getvalue('input_accession')
        input_statement = input_statement + '++acc++' + accession
    
    q_uid = '%'+uid+'%'
    q_date_time = '%'+date_time+'%'
    q_search_type = '%'+search_type+'%'
    q_search_input = '%'+input_statement+'%'

    qry_st1 = "INSERT INTO project_mobius"
    qry_st2 = "VALUES (%s,%s,%s,%s)"

if __name__ == '__main__':
    ip = sys.argv[1]
    main()
