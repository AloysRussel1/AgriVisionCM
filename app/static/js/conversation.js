document.addEventListener("DOMContentLoaded", function () {
    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

    socket.on("connect", function () {
        console.log("✅ Connecté à SocketIO !");
        socket.emit("join_room", {
            user1: currentUserId,
            user2: sellerId
        });
    });

    document.getElementById("send-btn").addEventListener("click", function () {
        console.log("📩 Bouton cliqué !");
        sendMessage();
    });

    document.getElementById("message-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            console.log("⏎ Touche Enter détectée !");
            sendMessage();
        }
    });

    function sendMessage() {
        var messageInput = document.getElementById("message-input");
        var message = messageInput.value.trim();

        if (!message) {
            console.log("⚠️ Message vide, envoi annulé.");
            return;
        }

        console.log("📤 Envoi du message :", message);

        socket.emit("send_message", {
            sender_id: currentUserId,
            receiver_id: sellerId,
            message: message
        });

        // Ajouter immédiatement le message envoyé
        var chatBox = document.getElementById("chat-box");
        var messageDiv = document.createElement("div");
        messageDiv.classList.add("message", "sent");
        messageDiv.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(messageDiv);

        chatBox.scrollTop = chatBox.scrollHeight;
        messageInput.value = ""; // Effacer l'input après envoi
    }

    socket.on("receive_message", function (data) {
        console.log("📨 Message reçu :", data);

        if (data.sender_id !== currentUserId) {
            var chatBox = document.getElementById("chat-box");
            var messageDiv = document.createElement("div");
            messageDiv.classList.add("message", "received");
            messageDiv.innerHTML = `<p>${data.message}</p>`;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });
});
