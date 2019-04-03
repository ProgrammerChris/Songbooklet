$(document).ready(function()    {

    // When enter pressed, downloadbutton clicked
    $('#bookletname').keypress(function(e){
        if(e.keyCode==13)
        $('#downloadbutton').click();
      });

    
    // When downloadbutton pressed, send chosen songs to server for merging.
    $('#downloadbutton').click(function()  {
        let data = {};
        let filename = document.getElementById('bookletname').value;

        if (filename != '')   {
            data['filename'] = filename
        } else {
            data['filename'] = 'ditthefte';
        }

        console.log(data['filename'])

        data['songs'] = sessionStorage.getItem('chosensongs');

        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            url: "/download",
            dataType: 'text',
            success: function() {
                // On success, download the file
                window.location.href = "/download/" + data['filename'];

            },
            error: function(error)   {
                alert("Oops, something went wrong! Please supply the following error message to the maintainer of this site.\n" + error);
            }
        });
    });

});