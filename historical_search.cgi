#!/usr/local/bin/python3

import cgitb
import jinja2
import mysql.connector

# Author: Brian Poon
# Class: AS410.712.82
# Term: Spring 2022
# Assignment: Final Project
# Description: CGI to pull data from SQL server at the 
# loading of a page. After which, it will load the template 
# HTML and JS that runs the CGI will load it into the HTML page.


def load_template(results):

    # Directing the template filepath for template loader
    templateLoader = jinja2.FileSystemLoader(searchpath='./templates')

    # Creating the environment to take the template loader and load
    # a specfic template in the folder.
    env = jinja2.Environment(loader=templateLoader)
    template = env.get_template('table_template.html')

    # Counter for entries and associated index that will limit
    # results to 10 entries
    entry_counter = 0
    index = []

    # This list will contain the UID from project_mobius.
    uid = []

    # This list will contain the date and time separated from 
    # date_time in project_mobius.
    date = []
    time = []

    # This list will contain the search_type and search_input 
    # columns from project_mobius.
    search_type = []
    search_input = []

    while True:

        index.append(entry_counter)
        uid.append(results['uid'][entry_counter])
        search_type.append(results['search_type'][entry_counter])
        search_input.append(results['search_input'][entry_counter])

        a = results['date_time'][entry_counter]
        b = a[0:x+1:1]  # Substring standard without regex
        c = a[x+1:y+1:1]

        date.append(b)
        time.append(c)

        if (entry_counter == 9):
            break

        entry_counter = entry_counter + 1

    # Send the information to HTML by referencing the variables
    # to pass between CGI and HTML.
    print("Content-Type: text/html\n\n")
    print(template.render(search_input=search_input, index_num=index,
                          date=date, time=time, search_type=search_type,
                          uid=uid))


def main():

    # Create the desired connection and cursor.
    conn = mysql.connector.connect(user='bpoon1', password='Testing123',
                                   host='localhost', database='bpoon1')
    cursor = conn.cursor()

    # To help with troubleshooting passing of values
    cgitb.enable(display=0, logdir="/path/to/logdir")

    qry = "SELECT * FROM project_mobius"

    cursor.execute(qry)

    # Declare an empty dictionary to start with.
    results = {'uid': list(), 'date_time': list(),
               'search_type': list(), 'search_input': list()}

    # Use For loop to add values from SQL results to dictionary using
    # featureprop_id as the key because that is the UID in featureprop table.
    for (uid, date_time, search_type, search_input) in cursor:

        # Convert the encoding to utf-8 and type convert numerical values
        # to int, which makes things easier later.
        date_time = str(date_time, encoding='utf-8')
        results['uid'].append(uid)
        results['date_time'].append(date_time)
        results['search_type'].append(search_type)
        results['search_input'].append(search_input)

    conn.close()

    load_template(results)


if __name__ == '__main__':
    main()
