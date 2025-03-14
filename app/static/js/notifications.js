document.addEventListener('DOMContentLoaded', async function () {
    const notificationIcon = document.querySelector('.notification-icon');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    const notificationBadge = document.querySelector('.notification-badge');
    const notificationList = document.getElementById('notification-list');
    const notificationWrapper = document.querySelector('.notification-wrapper');
    let notifications = [];

    // Charger les notifications depuis le serveur
    async function loadNotifications() {
        try {
            const response = await fetch('/get_notifications', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                notifications = await response.json();
                updateNotifications();
            } else {
                console.error('Erreur lors du chargement des notifications:', response.status);
            }
        } catch (error) {
            console.error('Erreur réseau:', error);
        }
    }

    // Afficher/masquer la liste déroulante et marquer comme lu
    notificationIcon.addEventListener('click', async function () {
        notificationDropdown.classList.toggle('hidden');
        if (!notificationDropdown.classList.contains('hidden')) {
            for (const notif of notifications) {
                if (!notif.is_read) {
                    await fetch('/mark_notification_read', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ notification_id: notif.id })
                    });
                    notif.is_read = true;
                }
            }
            updateNotifications();
        }
    });

    // Cacher la liste si on clique ailleurs
    document.addEventListener('click', function (e) {
        if (!notificationWrapper.contains(e.target)) {
            notificationDropdown.classList.add('hidden');
        }
    });

    // Ajouter une notification localement (pour les prédictions en temps réel)
    function addNotification(message, type = 'info') {
        const notification = {
            message: message,
            type: type,
            timestamp: new Date().toLocaleTimeString(),
            is_read: false
        };
        notifications.unshift(notification);
        updateNotifications();
    }

    // Mettre à jour l'affichage des notifications
    function updateNotifications() {
        notificationList.innerHTML = '';
        const unreadCount = notifications.filter(n => !n.is_read).length;
        notifications.forEach((notif) => {
            const li = document.createElement('li');
            li.textContent = `[${notif.timestamp}] ${notif.message}`;
            li.classList.add(`notification-${notif.type}`);
            if (!notif.is_read) li.classList.add('unread');
            notificationList.appendChild(li);
        });
        if (unreadCount > 0) {
            notificationBadge.textContent = unreadCount;
            notificationBadge.classList.remove('hidden');
        } else {
            notificationBadge.classList.add('hidden');
        }
        notificationIcon.classList.toggle('active', notifications.length > 0);
    }

    // Exporter la fonction
    window.addNotification = addNotification;

    // Charger les notifications au démarrage
    await loadNotifications();
});

const blinkStyle = `
    .blink { animation: blink 0.5s infinite; }
    @keyframes blink { 50% { opacity: 0.5; } }
`;
document.head.insertAdjacentHTML('beforeend', `<style>${blinkStyle}</style>`);