$(document).ready(function() {
    $('#send-btn').click(function() {
        var userMessage = $('#user-input').val().trim();
        if (userMessage !== '') {
            appendUserMessage(userMessage);
            getUserResponse(userMessage);
            $('#user-input').val('');
        }
    });

    function appendUserMessage(message) {
        $('#chat-message').append('<div class="user-message"><p>You: ' + message + '</p></div>');
        scrollToBottom();
    }

    function appendBotMessage(message) {
        $('#chat-message').append('<div class="bot-message"><p>Bot: ' + message + '</p></div>');
        scrollToBottom();
    }

    function getUserResponse(message) {
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'message': message }),
            success: function(response) {
                appendBotMessage(response.response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }

    function scrollToBottom() {
        var chatBox = document.getElementById('chat-box');
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
