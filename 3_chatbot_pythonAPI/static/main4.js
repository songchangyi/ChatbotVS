$(document).ready(function() {
  console.log("ready!");

  $('#try-again').hide();

  // on form submission ...
  $('form').on('submit', function() {

    console.log("the form has been submitted");

    // grab values
    valueOne = $('input[name="location"]').val();
    console.log(valueOne)

    $.ajax({
      type: "POST",
      url: "/",
      data : { 'first': valueOne,'second': '' },
      success: function(results) {
        $('#results').html('<b>User :</b>' + valueOne + '<br>' + '<b>ChatbotVS :</b>' + results)
          //return the specifique response format     
      },
      error: function(error) {
        console.log(error)
      }
    });
  });

  $('#try-again').on('click', function(){
    $('input').val('').show();
    $('#try-again').hide();
    $('#results').html('');
  });

});
