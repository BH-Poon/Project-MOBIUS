===== ABOUT THE PROJECT =====

This project originally started with the goal of connecting different sources of data and tools to a single functioning center. Think of the tool Galaxy in that it is the ultimate toolshed (and forum, too). Ideally, MOBIUS would take in data fed from the databases and reroute them to separate tools or databases for query. Galaxy has somewhat of a feature similar to this, but not directly from the database. Now I see why. There are so many different outputs that the databases can give, not to include some that have extremely strict inputs options. Nevertheless, the delivery of the product was also an issue. How does one wait for BLAST to load when it takes about 5 minutes? The solution was to make the page load that particular container every minute. In hindsight, running BLAST on this server would have probably shortened the time, but it would also result in lots of data increase. 


===== GENERAL WALKTHROUGH ON MOBIUS =====

== IF THIS IS NEWLY ADDED ONTO THE SERVER ==
Please be sure to set the permissions of the templates of the CGI, HTML, and Python files to allow access. This can be done with 'chmod 757' in the command line of the server. There are many issues that will occur if this is not done. Alternatively, it might just be safer set all files with 'chmod 757' to avoid debugging possible issues. 

== FOR SEQUENCES ==
Only sequences that are in the FASTA format can be used. Sequences also MUST include the FASTA header. Currently, only one sequence can be searched at a time, but the current ideology is that multiple FASTA sequences can be searched. However, this would make it very troubling for the result to be displayed in a palatable format. There are also thoughts about allowing a sequence to be uploaded, which is not very complicated to deal with, but needs much more controls to ensure it does not crash the program.

== FOR ACCESSIONS ==
Accessions can be used for searching databases only and mulitple accessions can be used at once in the search. However, the output has only been limited to five reuslts maximum per database during development. Again, the challenge here is to decide how to display the results in a palatable format for the user. Future works on this is to allow the choices to be selected, then funneled through to the sequence search with tools available for use. 


===== DETAILED WALKTHROUGH ON MOBIUS =====

== FOR SEQUENCES ==

1. The sequence panel is already visible to the user. Copy and paste the entire FASTA sequence into the textarea for sequences. There are also validation controls in the JavaScript that ensure a FASTA header is present.

2. Select the tools that you would like to use, then select the database that you would like to use. Keep in mind that for the databases, Ensembl has specific genomes that can be searched using its REST API. Currently, only the Human hg38 genome is added into MOBIUS. Future thoughts is to use a contoller just for Ensembl search in order to branch out to multiple genomes available and feed back only the ones that had results. 

3. There is JavaScript validation control in the background to ensure that at least one tool or database is selected. Additionally, there are validations to check the sequence submitted, except for the first line that is the header, for any abnormal characters that are not found in neither nucleotide nor protein sequences. 

4. Click 'Submit' to start!

== FOR ACCESSIONS ==

1. Click the 'Accessions' above the input area for sequences. The container for Accessions will show itself and the container for Sequences will be hidden.

2. Input the accessions to search. Separate multiple accessions with a comma. For the Ensembl database, it does have requirements for accessions. Their own Ensembl accessions are much more preferred, so use the Ensembl accessions that start with 'ENS' if possible. The search is set up for use with external accessions, so that should not be an issue. However, the genome that can be searched (as described in the previous section) is still an issue. 

3. Select the databases to search.

4. Click 'Submit' to Start!

== FOR HISTORICAL ==

1. This is currently in development. Future plans include the ability for a popup to come out and modify the historical search if desired. This way, any new updates in the search can be an option for the user. 

2. Once completed, one will be able to select a historical search in the table by checking the checkbox. Ideally an option would appear for selecting the search parameters and displaying the information from the previous search. 

3. Click 'Submit' to start search using the historical search.

===== DEMO DATA =====

1. Only the demo files for protein and nucleotide sequences are available.

2. For protein sequences it is "FASTA_protein_sample.fasta" and for nucleotide sequences, it is "FASTA_nucleotide_sample.fasta".

2. They can be found in the folder ./reference_data


===== FUTURE PROJECTIONS =====

This was a truly herculean project. From the start, it seemed very simple, but over time it showed just how much effort needed to be involved on the frontend and backend. The project evolved to be more modular in form, sort of a "when it comes it comes" attitude in connecting with the various external sources. This means that, ultimately with more time, there would be a main container page the user sees and operates from. On the backend, JavaScript would take care of all the event actions as well as load relevent data that was returned since the user has entered the page. Unfortunately, the only time that was availble left was for BLAST to be connected as a tool. Much time has been used in trying to connect the pages and sections together. 