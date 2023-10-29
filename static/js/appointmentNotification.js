const socket = new WebSocket("ws://localhost:8000/ws/book-appointment/");

socket.onopen = function(e) {
    socket.send("check if lawyer");
};