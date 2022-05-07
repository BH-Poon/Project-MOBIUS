// this function executes our search via an AJAX call
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './historical_search.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}


// this processes a passed JSON structure representing gene matches and draws it
//  to the result table
function processJSON( data ) {
    // set the span that lists the match count
    $('#match_count').text( data.match_count );
    
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
    
        // create a row and append it to the body of the table
        $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
        
        // add the locus column
        $('<td/>', { "text" : item.locus_id } ).appendTo('#' + this_row_id);
        
        // add the product column
        $('<td/>', { "text" : item.product } ).appendTo('#' + this_row_id);

    });
    
    // now show the result section that was previously hidden
    $('#results').show();
}

//Validation function to check that something has been inputted.
function validateSubmitNow() {

    var accession = String(document.getElementById('input_accession').value);
    var sequence = String(document.getElementsByTagName('input_sequence').value);

    if (accession === "" && sequence === "") {
        window.alert("Please add parameters for search!");
        return false;

    } else if (!sequence.startsWith(">") && accession === "") {
        window.alert("Please insert sequence in FASTA format!");
        return false;

    } else {
        return true;  

    }
    
}


// run our javascript once the page is ready
$(document).ready(function() {
    // define what should happen when a user clicks submit on our search form
    $('#submit').click( function() {
        runSearch();
        return false;  // prevents 'normal' form submission
    });

    //Adding event listeners to buttons to toggle, clear the input of the other type, and identify current type.
    document.getElementById('btn_accession').addEventListener('click', (e) => {
        $('#input_accession, #label_input_accession').show();
        $('#input_sequence, #label_input_sequence, #option_tools').hide();
        document.getElementById('input_sequence').value = null;
        $('#submit_now_type').value = "s";

    });

    document.getElementById('btn_sequence').addEventListener('click', (e) => {
        $('#input_accession, #label_input_accession').hide();
        $('#input_sequence, #label_input_sequence, #option_tools').show();
        document.getElementById('input_accession').value = null;
        $('#submit_now_type').value = "a";

    });

    //Hide the input field and label for accessions at the start.
    $('#input_accession, #label_input_accession').hide();
    $('#submit_now_type').value = "s";

    // Use AJAX to call for the CGI for historical search and include into Home. 
    $.ajax({
        url: './historical_search.cgi',
        method: 'get',
        dataType: 'html',
        data:   $_SERVER["REMOTE_ADDR"],
        contentType: 'text/html',
        success: $(function() {
            $('#div_table_load').load("table_template.html")
        }),
        error:$(function() {
            document.window.alert("Error retrieving historical search!")
        })
    });
});

