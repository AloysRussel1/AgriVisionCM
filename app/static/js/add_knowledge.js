document.addEventListener('DOMContentLoaded', () => {
    const typeSelect = document.getElementById('type-select');
    const contentGroup = document.getElementById('content-group');
    const fileGroup = document.getElementById('file-group');
    const form = document.getElementById('knowledge-form');
    const contentInput = document.getElementById('content');
    const fileInput = document.getElementById('file-upload');

    function updateFormFields() {
        const selectedType = typeSelect.value;
        if (selectedType === 'qna') {
            contentGroup.style.display = 'block';
            contentInput.disabled = false;
            fileGroup.style.display = 'none';
            fileInput.disabled = true;
            fileInput.value = ''; // Réinitialise le champ fichier
        } else {
            contentGroup.style.display = 'none';
            contentInput.disabled = true;
            contentInput.value = ''; // Réinitialise le champ contenu
            fileGroup.style.display = 'block';
            fileInput.disabled = false;
        }
    }

    // Initialisation
    updateFormFields();
    typeSelect.addEventListener('change', updateFormFields);

    // Validation côté client avant soumission
    form.addEventListener('submit', (e) => {
        const selectedType = typeSelect.value;

        if (selectedType === 'qna' && !contentInput.value.trim()) {
            e.preventDefault();
            alert('Le contenu est requis pour les Q&A.');
        } else if (selectedType !== 'qna' && !fileInput.files.length) {
            e.preventDefault();
            alert('Un fichier est requis pour les articles (PDF) ou vidéos (MP4).');
        } else if (selectedType === 'article' && fileInput.files.length) {
            const file = fileInput.files[0];
            if (!file.name.endsWith('.pdf')) {
                e.preventDefault();
                alert('Seuls les fichiers PDF sont acceptés pour les articles.');
            }
        } else if (selectedType === 'video' && fileInput.files.length) {
            const file = fileInput.files[0];
            if (!file.name.endsWith('.mp4')) {
                e.preventDefault();
                alert('Seuls les fichiers MP4 sont acceptés pour les vidéos.');
            }
        }
    });
});