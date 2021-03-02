$(document).ready(function() {


    // $("div.card-header:contains(title_name)").hide();

    $("#user-input-form").on("submit", function(e) {
        e.preventDefault()
            // console.log(e)


        chatinput = document.getElementById("chatinput").value;
        document.getElementById("chatinput").value = ""
        document.getElementById("chat_content").innerHTML +=
            `<div class="chat-message-group writer-user">
                <div class="chat-messages">
                    <div class="message">` + chatinput + `</div>
                    <div class="from">Sat 04:55</div>
                </div>
            </div>`
        console.log(chatinput)
        var formData = {
            'user_response': chatinput
        }

        $.ajax({
            type: 'post',
            url: '/message',
            data: formData,
            cache: false,
            success: function(response_string) {
                console.log(response_string.response)
                document.getElementById("chat_content").innerHTML += `<div class="chat-message-group">
                <div class="chat-thumb">
                <figure class="image is-32x32">
                    <img src="static/images/user-512.webp">
                </figure>
                </div>
                <div class="chat-messages">
                <div class="message">` + response_string.response + `</div>
                <div class="from">Sat 04:55</div>
                </div>
                </div>`
                var $chat_window = $('#scrol_id');
                $chat_window.scrollTop($chat_window[0].scrollHeight);

            }

        });


    });


})

function toggleChat() {

    var chat_minimize = document.getElementById("chatbox-area");
    if (chat_minimize.style.display === "none") {
        chat_minimize.style.display = "block";
    } else {
        chat_minimize.style.display = "none";
    }

}