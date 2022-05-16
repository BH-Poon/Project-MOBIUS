//Validation function to check that something has been inputted.
function validateSubmitNow() {

    var accession = $('#input_accession').val();
    var sequence = $('#input_sequence').val();

    var checkboxes = document.querySelectorAll('input[name^="cbx_"]');
    var checked = false;
    for (var checkbox of checkboxes) {
        if (checkbox.checked) {
            checked = true;
        }
    }
    
    if (checked == false) {
        window.alert("Please check at least one option!");
        return false;
    }

    if (accession == "" && sequence == "") {
        window.alert("Please add parameters for search!");
        return false;

    } else if (!sequence.startsWith(">") && accession == "") {
        window.alert("Please insert sequence in FASTA format!");
        return false;

    } else {
        return true;

    }

}



// run our javascript once the page is ready
$(document).ready(function () {
    
    //Adding event listeners to buttons to toggle, clear the input of the other type, and identify current type.
    document.getElementById('btn_accession').addEventListener('click', (e) => {
        $('#input_accession, #label_input_accession').show();
        $('#input_sequence, #label_input_sequence, #options_tools').hide();
        $('#input_sequence').val(null);
        $('#submit_now_type').val(String("a"));
    });
    document.getElementById('btn_sequence').addEventListener('click', (e) => {
        $('#input_accession, #label_input_accession').hide();
        $('#input_sequence, #label_input_sequence, #options_tools').show();
        $('#input_accession').val(null);
        $('#submit_now_type').val(String("s"));
    });

    //Adding event listener to btn_submit_now
    document.getElementById('btn_submit_now').addEventListener('click', (e) => {
        
        if (validateSubmitNow()) {
            //If validation is good, then pass onto CGI

            var ip = String($('#user_ip').val());
            var type = String($('#submit_now_type').val());
            
            const specialChars = /[`!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?~]/;
            const numChar = /[0-9]/;


            var lines = String($('#input_sequence').val());
            var lines = lines.split(/\n/);
            for (var i = 1; i < lines.length; i++) {
                if (specialChars.test(lines[i])){
                    window.alert('Special characters detected. Please check sequence!');
                    return false
                }
                if (numChar.test(lines[i])) {
                    window.alert('Numerical characters detected. Please check sequence!');
                    return false
                }
            }

            console.log('Validation passed...' + ip +
                ' for ' + type +'\n');

            return true
            
        } else {
            //If validation is bad, then do nothing
            void(0);
        }

    });


    //Hide the input field and label for accessions at the start.
    var sTemp = String("s");
    $('#input_accession, #label_input_accession').hide();
    $('#submit_now_type').val(sTemp);

    //Put in the results from historical_search.cgi
   // $('#div_table_load').load("./historical_search.cgi"); 
    $.ajax({
        url: './historical_search.cgi',
        method: 'GET',
        async: false,
        dataType: 'html',
        success: function (data) {
           document.getElementById("div_table_load").innerHTML = data;
        }
    });
    
    //Get user IP for later use.
    $.getJSON('https://api.ipify.org?format=jsonp&callback=?', function (data) {

        ipify_JSON = JSON.parse(JSON.stringify(data, null, 2));
        var user_ip_ipify = String(ipify_JSON.ip);
        $('#user_ip').val(user_ip_ipify);
    });

    





    /**
     * sends a request to the specified url from a form. this will change the window location.
     * @param {string} path the path to send the post request to
     * @param {object} params the parameters to add to the url
     * @param {string} [method=post] the method to use on the form
     */
/*
    function post(path, params, method = 'post') {

        // The rest of this code assumes you are not using a library.
        // ItD can be made less verbose if you use one.
        const form = document.createElement('form');
        form.method = method;
        form.action = path;

        for (const key in params) {
            if (params.hasOwnProperty(key)) {
                const hiddenField = document.createElement('input');
                hiddenField.type = 'hidden';
                hiddenField.name = key;
                hiddenField.value = params[key];

                form.appendChild(hiddenField);
            }
        }

        document.body.appendChild(form);
        form.submit();
    }

*/




});