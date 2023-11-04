// Connction to the web socket
var socket = io.connect(
  "https://" + document.location.hostname + ":" + location.port
);

// Confirms connection to the web socket
socket.on("connect", function () {
  console.log("connected");
});

// Updaates the user's name, score and high score
socket.on("update", function (msg) {
  document.getElementById("user-name").innerHTML = msg.user;
  document.getElementById("score-value").innerHTML = msg.score.toString();
  document.getElementById("high-score-value").innerHTML =
    msg.highscore.toString();
});

// Updates the country flag and clears the answer labels of previous answers
socket.on("update_country", function (msg) {
  document.getElementById("answer-label").innerHTML = "";
  document.getElementById("answer-key").innerHTML = "";
  document.getElementById("country-flag").src = msg.flag;
});

// Updates the answer label with the correct answer and
// changes the colour of the label to green if the answer is correct
// or red if the answer is wrong
socket.on("result", function (msg) {
  if (msg.result) {
    document.getElementById("answer").style.color = "green";
    document.getElementById("answer-label").innerHTML = "Correct! It is ";
  } else {
    document.getElementById("answer").style.color = "red";
    document.getElementById("answer-label").innerHTML = "Wrong! It is ";
  }
  document.getElementById("answer-key").innerHTML = msg.answer;
});

// Function to send the user's answer to the server
function send_answer() {
  var answer = document.getElementById("guess-input").value;
  if (answer == "") {
    return;
  }
  document.getElementById("guess-input").value = "";
  socket.emit("answer", { answer: answer });
}
document.getElementById("send-button").addEventListener("click", send_answer); // Send button
document
  .getElementById("guess-input")
  .addEventListener("keyup", function (event) {
    // Enter key
    if (event.key === "Enter") {
      event.preventDefault(); // Cancel the default action, if needed
      send_answer();
    }
  });

// Logs out the user and returns to the login page
function logout() {
  socket.emit("end");
  window.location.href = "/logout";
}
document.getElementById("logout-button").addEventListener("click", logout);

// Ends the round and starts a new round
function end() {
  socket.emit("end");
  window.location.href = "/";
  socket.emit("connect");
}
document.getElementById("end-button").addEventListener("click", end);
