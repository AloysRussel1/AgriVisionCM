document.addEventListener('DOMContentLoaded', () => {
    console.log('Script events.js chargé avec succès'); // Confirme que le script s'exécute

    const deleteButtons = document.querySelectorAll('.delete-btn');
    console.log(`Nombre de boutons "Supprimer" trouvés : ${deleteButtons.length}`); // Vérifie si les boutons sont trouvés

    // Gestion des boutons "Supprimer"
    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            console.log('Clic sur le bouton Supprimer détecté'); // Confirme que le clic est capturé
            if (confirm('Voulez-vous vraiment supprimer cet événement ?')) {
                const id = button.getAttribute('data-id');
                console.log(`Tentative de suppression de l'événement ID: ${id}`); // Confirme l'ID
                fetch(`/delete_event/${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erreur HTTP: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        button.closest('.event-card').remove();
                        console.log(`Événement ${id} supprimé avec succès`);
                    } else {
                        alert('Erreur lors de la suppression : ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Erreur lors de la suppression:', error);
                    alert('Une erreur est survenue lors de la suppression.');
                });
            }
        });
    });
});