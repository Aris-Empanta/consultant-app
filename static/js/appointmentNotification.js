// Change it and make it dynamic
const socket = new WebSocket("ws://localhost:8000/ws/book-appointment/");

socket.onopen = () => {
    console.log('connection established')
}

socket.onmessage = function(e) {
    console.log(e.data)
};

// Event handler for connection errors
socket.onerror = function (error) {
    console.error("WebSocket error:", error);
};