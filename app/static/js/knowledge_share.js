document.addEventListener('DOMContentLoaded', () => {
    const filterButtons = document.querySelectorAll('.filter-button');
    const knowledgeItems = document.querySelectorAll('.knowledge-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Retirer la classe active de tous les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Ajouter la classe active au bouton cliqué
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');

            knowledgeItems.forEach(item => {
                const itemType = item.getAttribute('data-type');
                if (filter === 'all' || itemType === filter) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});