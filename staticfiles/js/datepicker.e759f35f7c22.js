$(document).ready(function() {
    $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd' });

    // Authomatically add - on date
    var input = document.getElementById("id_dateOfBirth");
    input.addEventListener("input", function() {
      if(input.value.length === 4 || input.value.length == 7) {
        input.value += "-";
      }
    })

    //Validate phone input
    $('#id_phoneNumber').keypress(function(e) {
        var a = [];
        var k = e.which;

        for (i = 48; i < 58; i++)
            a.push(i);

        if (!(a.indexOf(k)>=0))
            e.preventDefault();
    });
});

