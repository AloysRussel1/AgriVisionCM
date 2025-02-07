document.addEventListener('DOMContentLoaded', () => {
    const filterButtons = document.querySelectorAll('.filter-button');
    const knowledgeItems = document.querySelectorAll('.knowledge-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            // Supprime la classe 'active' de tous les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Ajoute la classe 'active' au bouton cliqué
            e.target.classList.add('active');

            const filter = e.target.getAttribute('data-filter');

            knowledgeItems.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-type') === filter) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});