
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('new-comment-form');

    form.addEventListener('submit', (e) => {
        // Ici, vous pourriez ajouter du JS pour gérer l'envoi du commentaire via AJAX si vous voulez une mise à jour en temps réel sans recharger la page.
        // Pour l'instant, nous allons laisser Flask gérer cela avec une redirection.
        e.preventDefault();
        
        const content = form.elements['content'].value;
        if (content.trim() === '') {
            alert('Veuillez entrer un message.');
            return;
        }
        
        // Si vous voulez ajouter une logique AJAX ici, vous pouvez le faire et ensuite mettre à jour la page sans rechargement.
        form.submit();
    });
});
