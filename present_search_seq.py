#!/usr/local/bin/python3

import re
from Bio.Blast import NCBIWWW, NCBIXML
from io import StringIO, TextIOWrapper

# Author: Brian Poon
# Class: AS410.712.82
# Term: Spring 2022
# Assignment: Final Project
# Description: Script is used for getting data using 
# the selected tools and databases. 

def blast(file_path, seq_type):

    sequence = open(file_path).read()

    E_VALUE_THRESH = 1e-20 

    if seq_type == 'PROTEIN':
        result_blast = NCBIWWW.qblast("blastp", "refseq_protein", sequence, threshold=E_VALUE_THRESH, hitlist_size=50,)
    if seq_type == 'RNA':
        result_blast = NCBIWWW.qblast("blastn", "refseq_rna", sequence, threshold=E_VALUE_THRESH, hitlist_size=50) 
    if seq_type == 'DNA':
        result_blast = NCBIWWW.qblast("blastn", "refseq_genomes", sequence, threshold=E_VALUE_THRESH, hitlist_size=50, )

    with open('./reference_data/result_blast_run.xml', 'r+') as save_file:
        
        save_file.write(StringIO.getvalue(result_blast))
    
        with open('./templates/result_blast_print.html', 'a') as print_file:
            
            for record in NCBIXML.parse(save_file):     
                if record.alignments: 
                    print_file.write("\n" + "<p> query: %s" % record.query[:100])
                    
                    for align in record.alignments: 
                        for hsp in align.hsps: 
                            if hsp.expect < E_VALUE_THRESH: 
                                print_file.write("\n\t"+ "match: %s " % align.title[:100])
                    
                    print_file.write('</p>')
        print_file.close()

    # No returns. Will have JS for file repeatedly check for uploading the file

def get_tools(file_path, tool_options, seq_type):

    # Check here to connect to the tools desired
    # ['cbx_blast', 'cbx_orffinder', 'cbx_splign', 'cbx_igv']

    # Clear out all the old tempaltes first
    with open('./templates/result_blast_print.html', 'r+') as f:
        f.truncate(0)
        f.close()

    # Use API here to connect to the tools desired
    for tools in tool_options:
        if tools == 'cbx_blast':
            with open('./templates/result_blast_print.html', 'r+') as f:
                f.write("<h1 style='text-align: centered;'> Getting BLAST Now... </h1>\n\n")
                f.write("<h3 style='text-align: centered;'> It can take a while, but this page is loading every minute! </h1>\n\n")
                f.close()
                
            blast(file_path, seq_type)

def breakdown_seq_aa(file_path, aa_list):

    # Generate an empty dictionary of keys using aa_list
    aa_dict = {}
    for i in aa_list:
        aa_dict[i] = 0
    
    # Boolean for unique amino acid
    unique_aa = False
    
    # Regex pattern for trimming newline
    regex = '\n'

    # Do the same separation again
    with open(file_path) as file:
        line = file.readline() 

        for line in file:
            if line[0]=='>':
                pass
            
            else:
                line = re.sub(regex, '', line)
                for char in enumerate(line):

                    if char[1] in aa_dict:
                        a = aa_dict.get(char[1])
                        a = a + 1
                        aa_dict.update({char[1] : a})
                    else:
                        unique_aa = True
    
    # Got all the counts in the sequence for each now sum it
    sub_count = aa_dict.values()
    total = sum(sub_count)

    # Get the % HYDROPHOBIC
    a = sum([aa_dict.get('A'), aa_dict.get('I'), aa_dict.get('L'),
        aa_dict.get('M'), aa_dict.get('F'), aa_dict.get('V'), 
        aa_dict.get('P'), aa_dict.get('G')])  
    pHydrophobic = round((a/total*100),2)

    # Get the % HYDROPHILLIC
    a = sum([aa_dict.get('R'), aa_dict.get('N'), aa_dict.get('D'),
        aa_dict.get('Q'), aa_dict.get('E'), aa_dict.get('K')])    
    pHydrophilic = round((a/total*100),2)

    # Get the % POSITIVE CHARGED
    a = sum([aa_dict.get('R'), aa_dict.get('H'), aa_dict.get('K')])    
    pPosCharge = round((a/total*100),2)

    # Get the % NEGATIVE CHARGED
    a = sum([aa_dict.get('D'), aa_dict.get('E')])    
    pNegCharge = round((a/total*100),2)

    # Get the % POLAR
    a = sum([aa_dict.get('R'), aa_dict.get('N'), aa_dict.get('D'),
        aa_dict.get('Q'), aa_dict.get('E'), aa_dict.get('H'),
        aa_dict.get('K'), aa_dict.get('S'), aa_dict.get('T'),
        aa_dict.get('Y')])    
    pPolar = round((a/total*100),2)

    # Get the % NON-POLAR
    a = sum([aa_dict.get('A'), aa_dict.get('C'), aa_dict.get('G'),  
        aa_dict.get('I'), aa_dict.get('L'), aa_dict.get('M'),
        aa_dict.get('F'), aa_dict.get('P'), aa_dict.get('W'),
        aa_dict.get('V')])    
    pNonPolar = round((a/total*100),2)

    return (aa_dict, total, pHydrophobic, pHydrophilic, pPosCharge,
            pNegCharge, pPolar, pNonPolar, unique_aa)


def breakdown_seq_nt(file_path, nt_list):
    
    # Get the length, G/C ratio, and percentages
    nt_dict = { 'A' : 0,
                'T' : 0,
                'G' : 0,
                'C' : 0,
                'U' : 0,                
                }
    
    with open(file_path) as file:
        line = file.readline() 

        for line in file:
            if line[0]=='>':
                pass
            
            else:
                for char in enumerate(line):
                    if char[1] in nt_dict:

                        a = nt_dict.get(char[1])
                        a = a + 1
                        nt_dict.update({char[1] : a})
            
    
    # Got all the counts in the sequence for each now sum it
    sub_count = nt_dict.values()
    total = sum(sub_count)

    # Get the G/C ratio
    gc_ratio = (nt_dict.get('G')+nt_dict.get('C'))/total
    gc_ratio = round((gc_ratio*100), 2)

    # Get the %A, %T, %G, %C, and %U
    pA = round((nt_dict.get('A')/total*100), 2)
    pT = round((nt_dict.get('T')/total*100), 2)
    pG = round((nt_dict.get('G')/total*100), 2)
    pC = round((nt_dict.get('C')/total*100), 2)
    pU = round((nt_dict.get('U')/total*100), 2)


    return (nt_dict, total, gc_ratio, pA, pT, pG, pC, pU)


def seq_check(file_path, unique_aa_list):

    type = ''
    with open(file_path) as file:
        line = file.readline() 

        for line in file:
            if line[0]=='>':
                pass
            for char in line:
                
                if (char in unique_aa_list):
                    type = 'PROTEIN'
                    
                elif (char == 'U'):
                    type = 'RNA'

            # Checked everything in sequence
            if type =='':
                type = 'DNA'

    return type
                
def main(file_path):

    #Use search input to break down the info needed for summary page
    #Determine protein or nucleotide to show which section to use

    #Use db_options to connect to API for DBs
    #Use tool_options to connect to API for tools
    #Print page at very last with all of the outputs

    # Set the necessary information for protein, DNA, and RNA
    aa_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 
                'U', 'V', 'W', 'X', 'Y', 'Z']
    
    nt_list = ['A','T','G','C','U']

    unique_aa_list = ['B', 'D', 'E', 'F', 'H', 'I', 
                    'K', 'L', 'M', 'N', 'P', 'Q', 'R', 
                    'S', 'V', 'W', 'X', 'Y', 'Z']

    seq_type = seq_check(file_path, unique_aa_list)

    if seq_type == ('DNA' or 'RNA'):
        seq_info = breakdown_seq_nt(file_path, nt_list)
    
    if seq_type == ('PROTEIN'):
        seq_info = breakdown_seq_aa(file_path, aa_list)

    return seq_type, seq_info


if __name__ == '__main__':
    main()
