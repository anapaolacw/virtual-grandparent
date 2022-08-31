
$(document).ready(function() {
  $('#btnDelete').on('click',function(e){
    e.preventDefault();
    console.log(e.target.href);
    confirmNotification("Are you sure to delete the request?", "Delete", "#F08181", e.target.href)
  })

  //Edit help request form
  $('#editForm').on('submit',function(e){
    e.preventDefault();
    var form = $('#editForm');
    var actionUrl = form.attr('action');
    $.ajax({
      type: "POST",
      url: actionUrl,
      data: form.serialize(),
      cache: false,
      success: function(data, textStatus, jqXHR){
        $('#submit').prop('disabled', true);
        Swal.fire({
          titleText: "Success",
          text: "Help request updated correctly",
          type: "success",
          confirmButtonText: "Ok",
          confirmButtonColor: '#98c1d9',
        }).then(data => {
          var getUrl = window.location;
          var redirectUrl = getUrl.protocol + "//" + getUrl.host + "/help-requests";
          window.location.href = redirectUrl;
        })
      },
      error: function() {
        errorNotification("Save failed", "There was an error updating your data");
      }  
   })
  })

  //Offer help button
  $('.btnOfferHelp').on('click',function(e){
    e.preventDefault();
    isVerified = $('#isVerified').text().trim();
    if(isVerified == "True"){
      console.log(e.target.href);
      redirectUrl = e.target.href;
      window.location.href = redirectUrl;
    }else{
      alert(isVerified)
      console.log(e.target.href);
      notification("Account not verified", "To offer help, our team must verify your identity. Please check your email to arrange a meeting.", "info", "Ok")
  
    }
  })

  //Delete offer
  $('#btnDeleteOffer').on('click',function(e){
    e.preventDefault();
    console.log(e.target.href);
    confirmNotification("Are you sure to delete the offer?", "Delete", "#F08181", e.target.href)
  })


  // Sign up form
  $('#signupForm').on('submit',function(e){
    e.preventDefault();
    var form = $('#signupForm');
    var actionUrl = form.attr('action');
    $.ajax({
      type: "POST",
      url: actionUrl,
      data: form.serialize(),
      success: function (data, status, xhr) {
        Swal.fire({
          titleText: "Your account was created",
          text: "A supervisor will contact you to verify your identity and activate your account",
          type: "info",
          confirmButtonText: "Ok",
          confirmButtonColor: '#98c1d9',
        }).then(response => {
          var getUrl = window.location;
          var redirectUrl = getUrl.protocol + "//" + getUrl.host + data;
          window.location.href = redirectUrl;
        })
    },
    error: function (jqXhr, textStatus, errorMessage) {
      console.log('Error' + errorMessage);
    }
   })
  })
});

