#!/usr/local/bin/python3
import cgi
import cgitb
from datetime import datetime
import sys
import jinja2
import mysql.connector
import present_search_seq as seq
import present_search_acc as acc
import db_search


# Author: Brian Poon
# Class: AS410.712.82
# Term: Spring 2022
# Assignment: Final Project
# Description: This will run when the submission button is hit 
# on the main page of the search. 

def load_template_acc(pacc_info, pdb_list, pdb_api):

    # Directing the template filepath for template loader
    templateLoader = jinja2.FileSystemLoader(searchpath='./templates')

    # Creating the environment to take the template loader and load
    # a specfic template in the folder.
    env = jinja2.Environment(loader=templateLoader)
    template = env.get_template('result_accession_template.html')
    
    # Macro in Jinja written to pull from another template, but must 
    # add in the ptool_list and ptool_api lists to trigger it. And vice 
    # versa for pdb_list and pdb_api. So those two lists must be added 
    # into the rendering.
    print ("Content-Type: text/html\n\n")
    print(template.render(db_list=pdb_list, db_api=pdb_api,
            seq_info=pacc_info))


def load_template_seq(pseq_info, ptool_list, ptool_api, pdb_list, pdb_api):

    templateLoader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=templateLoader)
    template = env.get_template('result_sequence_template.html')

    aa_dict = (pseq_info[1][0]).copy()
    value_list = list(aa_dict.values())
    aa_list = list(aa_dict.keys())
    
    # Macro in Jinja written to pull from another template, but must 
    # add in the tool_list and tool_api lists to trigger it. So those 
    # two lists must be added into the rendering.
    print ("Content-Type: text/html\n\n")
    print(template.render(tool_list=ptool_list, tool_api=ptool_api,
            db_list=pdb_list, db_api=pdb_api, seq_info=pseq_info,
            value_list=value_list, aa_list=aa_list,))


def selected_tools(form, input_statement):
    # Create a dictionary of all the element IDs for all tools
    tool_id = ['cbx_blast', 'cbx_orffinder', 'cbx_splign', 'cbx_igv']

    selected_options = []

    input_statement = input_statement+';tools='
    
    if len(selected_options)==0:
        selected_options.append("NULL")
    else:
        for i in range(len(tool_id)):
            
            if  form.getvalue(tool_id[i]):
                selected_options.append(tool_id[i])
                input_statement = input_statement+tool_id[i]+'+'
   
    return [selected_options, input_statement]



def selected_dbs(form, input_statement):
    # Create a dictionary of all the element IDs for all databases
    db_id = ['cbx_genbank', 'cbx_ensembl', 'cbx_omim']

    selected_options = []

    input_statement = input_statement+';dbs='
    if len(selected_options)==0:
        selected_options.append("NULL")
    else:
        for i in range(len(db_id)):
            
            if  form.getvalue(db_id[i]):
                selected_options.append(db_id[i])
                input_statement = input_statement + db_id[i]+'+'

    return [selected_options, input_statement]

def main():

    #Debug mode
    #print("Content-Type: text/html\n\n\n\n\n")
    #cgitb.enable()

    # Create the desired connection and cursor.
    conn = mysql.connector.connect(user='bpoon1', password='Testing123',
                                   host='localhost', database='bpoon1', 
                                   get_warnings=True)
    cursor = conn.cursor()
    
    # Create an pointer to the submitted form and get values hidden in HTML
    form = cgi.FieldStorage()
    
    search_type = str(form.getvalue('submit_now_type'))
    ip = str(form.getvalue('user_ip'))    

    # Create serach_input. IP is passed from JSON
    date_time= datetime.now()
    date = str(date_time.date())
    time = str(date_time.time())
    uid = date+'::'+ip+'::'+time

    out_file_path = '/var/www/html/bpoon1/final/data/' + str(date_time) +'-' + ip + '.fasta'
    fileobj = open(out_file_path,'w+' )   # w+ mode creates the file if its not exists

    # Create start of search_input and the list of tools and
    # databases chosen for by user to append to it. Functions will 
    # automatically append to input statement
    input_statement = ''

    func_tools = selected_tools(form, input_statement)
    input_tools = func_tools[0] # Get the list of tools that we're going to use
    input_statement = func_tools[1] # Input statement will add on

    func_dbs = selected_dbs(form, input_statement)
    input_dbs = func_dbs[0]
    input_statement = func_dbs[1]
    
    # Based on whether it is an accession or a sequence it forks.
    if (search_type == "s"):
        
        sequence = form.getvalue('input_sequence')
        fileobj.write(sequence)
        fileobj.close()
        input_statement = ';seq=' + sequence + '\n' +  input_statement
       
        # Begin passing information to sequence python file
        sequence_processed = seq.main(out_file_path)   
        api_tools = seq.get_tools(out_file_path, input_tools, sequence_processed[0])
        api_database = db_search.main(out_file_path, input_dbs, search_type)

        # Nucleotides: seq_type; seq_info{nt_dict{}, total, gc_ratio, pA, pT, pG, pC, pU}
        # Proteins: seq_type; seq_info {aa_dict{}, total, pHydrophobic, pHydrophilic,
        #           pPosCharge, pNegCharge, pPolar, pNonPolar, unique_aa}

        # Send result to sequence template
        load_template_seq(sequence_processed, input_tools, api_tools, input_dbs, api_database)

    if (search_type == "a"):
        accession = form.getvalue('input_accession')
        fileobj.write(accession)
        fileobj.close()
        input_statement = ';acc=' + accession + '\n' + input_statement
       
        # Begin passing information to sequence python file
        acc_processed = acc.main(out_file_path) 
        api_database = db_search.main(out_file_path, input_dbs, search_type)

        # Send result to sequence template
        load_template_acc(acc_processed, input_dbs, api_database) 

    # Need to format date_time to fit SQL datetime format prior to insertion
    date_time = datetime.strftime(date_time,'%m-%d-%y %H:%M:%S')
    
    qry = "INSERT INTO project_mobius VALUES (%s,%s,%s,%s)"  
    cursor.execute(qry, (uid, date_time, search_type, input_statement))
    conn.commit()

    # Print any warnings that might have occurred
    try:
        sys.stdout(cursor.fetchwarnings())
    except:
        pass

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()

