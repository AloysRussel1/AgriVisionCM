console.log("📜 Script conversation.js chargé !");

document.addEventListener("DOMContentLoaded", function () {
    console.log("📝 DOM entièrement chargé !");

    // Vérification de SocketIO
    if (typeof io === "undefined") {
        console.error("❌ SocketIO n'est pas chargé ! Vérifiez la balise script SocketIO.");
        return;
    }

    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);
    console.log("🔌 Tentative de connexion à SocketIO...");

    socket.on("connect", function () {
        console.log("✅ Connecté à SocketIO !");
        socket.emit("join_room", {
            user1: currentUserId,
            user2: sellerId
        });
        console.log("🚪 Émission de join_room pour user1:", currentUserId, "et user2:", sellerId);
    });

    socket.on("receive_message", function (data) {
        console.log("📨 Message reçu :", data);
        var chatBox = document.getElementById("chat-box");

        if (data.sender_id !== currentUserId) {
            var messageDiv = document.createElement("div");
            messageDiv.classList.add("message", "received");
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${data.message}</p>
                    <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
            `;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });

    var sendBtn = document.getElementById("send-btn");
    if (sendBtn) {
        console.log("✅ Bouton #send-btn trouvé !");
        sendBtn.addEventListener("click", function () {
            console.log("🖱️ Clic sur le bouton Envoyer détecté !");
            sendMessage();
        });
    } else {
        console.error("❌ Bouton #send-btn non trouvé !");
    }

    var messageInput = document.getElementById("message-input");
    if (messageInput) {
        console.log("✅ Champ #message-input trouvé !");
        messageInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                console.log("⏎ Touche Enter détectée !");
                sendMessage();
            }
        });
    } else {
        console.error("❌ Champ #message-input non trouvé !");
    }

    function sendMessage() {
        console.log("🚀 Début de sendMessage()");
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
            message: message,
            product_id: productId
        });
        console.log("📡 Message envoyé via SocketIO :", {
            sender_id: currentUserId,
            receiver_id: sellerId,
            message: message,
            product_id: productId
        });

        var chatBox = document.getElementById("chat-box");
        var messageDiv = document.createElement("div");
        messageDiv.classList.add("message", "sent");
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
                <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
        `;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        messageInput.value = "";
        console.log("✅ Message ajouté localement et champ vidé.");
    }

    window.onunload = function () {
        socket.emit("leave_room", {
            user1: currentUserId,
            user2: sellerId
        });
        console.log("🏃 Émission de leave_room");
    };
});