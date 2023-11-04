var socket = io.connect("https://" + document.location.hostname + ":" + location.port);

socket.on("connect", function() {
    console.log("connected");
});

socket.on("update", function(msg) {
    document.getElementById("user-name").innerHTML = msg.user;
    document.getElementById("score-value").innerHTML = msg.score.toString();   
    document.getElementById("high-score-value").innerHTML = msg.highscore.toString();
});

socket.on("update_country", function(msg) {
    document.getElementById("answer-label").innerHTML = "";
    document.getElementById("answer-key").innerHTML = "";
    document.getElementById("country-flag").src = msg.flag;
});

socket.on("result", function(msg) {
    if (msg.result){
        document.getElementById("answer").style.color = "green";
        document.getElementById("answer-label").innerHTML = "Correct! It is ";
    } else {
        document.getElementById("answer").style.color = "red";
        document.getElementById("answer-label").innerHTML = "Wrong! It is ";
    }
    document.getElementById("answer-key").innerHTML = msg.answer;
});

function send_answer() {
    var answer = document.getElementById("guess-input").value;
    if (answer == "") {
        return;
    }
    document.getElementById("guess-input").value = "";
    socket.emit("answer", {"answer": answer});
}
document.getElementById("send-button").addEventListener("click", send_answer);
document.getElementById("guess-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        send_answer();
    }
});

function logout() {
    socket.emit("end");
    window.location.href = "/logout";
}
document.getElementById("logout-button").addEventListener("click", logout);

function end(){
    socket.emit("end");
    window.location.href = "/";
    socket.emit("connect");
}
document.getElementById("end-button").addEventListener("click", end);
