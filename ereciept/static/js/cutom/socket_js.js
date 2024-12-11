// const roomName = JSON.parse(document.getElementById('room-name').textContent);
const roomName = 'a'
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);
chatSocket.onopen = function(e) {
    // alert("[open] Connection established");
    // alert("Sending to server");
    var data = {"data" : "My name is John"}
    chatSocket.send(   "My name is John"  );
  };
  
  chatSocket.onmessage = function(event) {
    // alert(`[message] Data received from server: ${event.data}`);
    console.log(event.data)
  }

  chatSocket.onclose = function(event) {
    if (event.wasClean) {
      alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
      // e.g. server process killed or network down
      // event.code is usually 1006 in this case
      alert('[close] Connection died');
    }
  }

  chatSocket.onerror = function(error) {
    alert(`[error] ${error.message}`);
  };
    // document.querySelector('#chat-message-input').focus();
    // document.querySelector('#chat-message-input').onkeyup = function(e) {
    //     if (e.keyCode === 13) {  // enter, return
    //         document.querySelector('#chat-message-submit').click();
    //     }
    // };

    // document.querySelector('#chat-message-submit').onclick = function(e) {
    //     const messageInputDom = document.querySelector('#chat-message-input');
    //     const message = messageInputDom.value;


    //     messageInputDom.value = '';
    // };


    const name = "a"
    const Socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/index/1' 
        
    );


    Socket.onopen = function(e) {  
        Socket.send(   "My name is John"  );

    }
