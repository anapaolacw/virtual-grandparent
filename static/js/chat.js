$(document).ready(function() {
    // Clicking enter on message input
    $('#message').keypress(function (e) {
        if (e.which == 13) {
          $('#chatForm').submit();
          return false;    //<---- Add this line
        }
      });
      
    $(document).on('submit', '#chatForm', function(e){
        e.preventDefault();
        var form = $('#chatForm');
        var actionUrl = form.attr('action');
        $.ajax({
            type:'POST',
            url: actionUrl,
            data: {
                contact_id: $('#contact_id').text(),
                message: $('#message').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                // alert(data)
            }
        });
        document.getElementById('message').value='';
    })
    setInterval(function(){
        var getMessagesUrl = "/chats/getMessages/" +$('#chat_id').text()
        $.ajax({
            type: 'GET',
            url: getMessagesUrl,
            success: function(response){
                $("#chat-messages").empty();
                for(var key in response.messages){
                    var extraClass="";
                    if(response.messages[key].isOwnerMessage){
                        extraClass="own-message";
                    }
                    var temp="<div class='message-container "+extraClass+"'>"+
                                "<p class='font-semibold'>"+response.messages[key].senderName+"</p>"+
                                "<p>"+response.messages[key].content+"</p>"+
                                "<span class='time-left'>"+response.messages[key].time+"</span>"+
                            "</div>";   
                    $("#chat-messages").append(temp);
                }
            },
            error: function(response){
                console.log("An error ocurred")
            }
        });
    }, 1000);
})