

// ...and take over its submit event.

$("#user-input-form").on("submit", function(e) {
  
  e.preventDefault()
  console.log(e)
  chatinput =  document.getElementById("chatinput").value;
  document.getElementById("chatinput").value = ""
  document.getElementById("chat_content").innerHTML += 
        `<div class="chat-message-group writer-user">
            <div class="chat-messages">
                <div class="message">`+chatinput+`</div>
                <div class="from">Sat 04:55</div>
            </div>
        </div>`
  const XHR = new XMLHttpRequest();
  
  XHR.addEventListener( "load", function(event) {
    console.log(event)
    res=event.target.responseText
    message = res.slice(18, res.length-3)
    document.getElementById("chat_content").innerHTML += `<div class="chat-message-group">
    <div class="chat-thumb">
      <figure class="image is-32x32">
        <img src="static/images/user-512.webp">
      </figure>
    </div>
    <div class="chat-messages">
      <div class="message">`+message+`</div>
      <div class="from">Sat 04:55</div>
    </div>
  </div>`
    });

// Define what happens in case of error
    XHR.addEventListener( "error", function( event ) {
        alert( event );
    });
  XHR.open( "POST", "http://127.0.0.1:3000/message" );
  XHR.setRequestHeader('Content-type', 'application/json')
  XHR.setRequestHeader("Access-Control-Allow-Origin", "*")
  XHR.send('{"user_response":"'+chatinput+'"}')
});