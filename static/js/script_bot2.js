function time_date() {
    var date_now = new Date();

    var minutes = date_now.getMinutes()
    var hours = date_now.getHours()
    var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var dayName = days[date_now.getDay()];
    var time_stamp = dayName + " " + hours + ":" + minutes
    return time_stamp
}

function chat_function2() {

    var time_stamp = time_date()
    chatinput = document.getElementById("chatinput").value;
    document.getElementById("chatinput").value = ""
    document.getElementById("chat_content").innerHTML +=
        `<div class="chat-bubble user">` + chatinput + `</div>
        <div class="chat-bubble user from bg-remove">` + time_stamp + `</div>
        <div class="chat-bubble bot typing">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
            <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
            </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
        </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
        </circle></svg>
        </div>`
        // $(".typing").style.display = 'none';

    //  + `</div> <div class="from">` + time_stamp + `</div>`
    console.log(chatinput)
    var formData = {
        'user_query': chatinput
    }

    $.ajax({
        type: 'POST',
        url: '/message',
        data: formData,
        cache: false,
        success: function(response_string) {
            console.log(response_string.response)
                // document.getElementById("typing").style.display = 'none';

            $('.typing').addClass('hide');
            // $('.chat-body').removeClass('hide');
            document.getElementById("chat_content").innerHTML +=
                `<div class="chat-bubble bot">` + response_string.response + `</div>`

            var $chat_window = $('#chat_content');
            $chat_window.scrollTop($chat_window[0].scrollHeight);

        }

    });

}
$(document).ready(function() {
    // document.getElementById("chat_content").innerHTML +=
    //     `<div class="chat-start"> Monday, 1:27 PM </div>`


    // $("div.card-header:contains(title_name)").hide();
    $("#user-input-form").on("submit", function(e) {
        e.preventDefault()
            // console.log(e)

        var time_stamp = time_date()
        chatinput = document.getElementById("chatinput").value;
        document.getElementById("chatinput").value = ""
        document.getElementById("chat_content").innerHTML +=
            `<div class="chat-bubble user">` + chatinput + `</div>
                <div class="user-time">` + time_stamp + `</div>
                <div class="chat-bubble bot typing">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                    <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
                    </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
                    <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
                </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
                    <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
                </circle></svg>
                </div>`
            // $(".typing").style.display = 'none';

        //  + `</div> <div class="from">` + time_stamp + `</div>`
        console.log(chatinput)
        var formData = {
            'user_query': chatinput
        }

        $.ajax({
            type: 'POST',
            url: '/message',
            data: formData,
            cache: false,
            success: function(response_string) {
                console.log(response_string.response)
                    // document.getElementById("typing").style.display = 'none';

                $('.typing').addClass('hide');
                // $('.chat-body').removeClass('hide');

                var time_stamp = time_date()
                document.getElementById("chat_content").innerHTML +=
                    `<div class="chat-bubble bot">` + response_string.response + `</div>
                    <div class=".bot-time" style = "font-size : xxx-small">` + time_stamp + `</div>`

                var $chat_window = $('#chat_content');
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