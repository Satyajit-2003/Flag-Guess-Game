var socket = io.connect("http://" + document.domain + ":" + location.port);

document.getElementById("send-button").addEventListener("click", function () {
  var message = document.getElementById("message-input").value;
  socket.emit("message_from_client", message);
  document.getElementById("message-input").value = "";
});

socket.on("message_from_server", function (data) {
  document.getElementById("message-display").textContent = data;
//   socket.emit("message_from_client", data);
});
