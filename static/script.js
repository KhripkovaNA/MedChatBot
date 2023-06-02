document.getElementById("user-input").addEventListener("submit", sendMessage);

function sendMessage(event) {
    event.preventDefault();
    var userInput = document.getElementById("user-message").value;

    if (userInput.trim() === "") {
        return;
    }

    var messageContainer = document.createElement("div");
    messageContainer.className = "message-container user";
    messageContainer.innerHTML = "<div class='message-box user-message'>You: " + userInput + "</div>";

    document.querySelector(".chat-messages").appendChild(messageContainer);
    document.getElementById("user-message").value = "";

    fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        var botResponse = data[0].text;
        var messageContainer = document.createElement("div");
        messageContainer.className = "message-container bot";
        messageContainer.innerHTML = "<div class='message-box bot-message'><span class='label'>Bot:</span> " + botResponse + "</div>";

        document.querySelector(".chat-messages").appendChild(messageContainer);
    });
}
