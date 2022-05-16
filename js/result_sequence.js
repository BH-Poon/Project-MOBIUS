// Run the JavaScript once the page is ready
$(document).ready(function() {
    
    if ($('#seq_type').val() == 'PROTEIN') {
        $('#section_nucleotide').hide();
        $('#secction_protein').show();
    
    } else if ($('#seq_type').val() == ('DNA' || 'RNA')) {
        $('#section_nucleotide').show();
        $('#secction_protein').hide();
        if ($('#seq_type').val() == 'DNA') {
            $('#t_label').show();
            $('#u_label').hide();
        } else {
            $('#t_label').hide();
            $('#u_label').show(); 
        }
    }

    
   function loadBlast() {
       $('#tools_container').load('./templates/result_blast_print.html');
       $('#db_container').load('./templates/result_db_print.html');

   }

    setInterval(loadBlast, 1000);


});
    
