$(document).ready(function() {
    $(document).on('submit', '#chatForm', function(e){
        e.preventDefault();
        var form = $('#chatForm');
        var actionUrl = form.attr('action');
        alert(actionUrl)
        console.log("Action url ")
        console.log(actionUrl)
        $.ajax({
            type:'POST',
            url: actionUrl,
            data: {
                chat_id: $('#chat_id').text(),
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
        console.log(getMessagesUrl)
        $.ajax({
            type: 'GET',
            url: getMessagesUrl,
            success: function(response){
                console.log(response);
                $("#chat-messages").empty();
                for(var key in response.messages){
                    console.log("key")
                    console.log(key)
                    var temp=" <div class='chat-container darker'> <p class='font-semibold'>"+response.messages[key].senderName+"</p><p>"+response.messages[key].content+"</p><span class='time-left'>"+response.messages[key].time+"</span></div>";                    
                    $("#chat-messages").append(temp);
                }
                console.log("updated")
            },
            error: function(response){
                alert("An error ocurred")
            }
        });
    }, 1000);
})