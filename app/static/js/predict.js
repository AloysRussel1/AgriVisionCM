document.addEventListener('DOMContentLoaded', function () {
    const manualEntryLink = document.getElementById('manual-entry');
    const manualProductInput = document.getElementById('manual-product');
    const productSelect = document.getElementById('product');
    const form = document.getElementById('prediction-form');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultsSection = document.getElementById('results');
    const insightsSection = document.getElementById('insights');

    const products = [
        "Ananas", "Arachides, non décortiquées", "Aubergines", "Avocats", "Bananes", "Basilic", "Carottes", "Café vert", "Choux", "Citrons", "Citrouilles", "Concombres", "Coriandre", "Courges", "Épinards", "Fèves de cacao", "Fibre de coton, égrenée", "Fonio", "Fruits de la passion", "Gingembre", "Gombos", "Goyaves", "Graines de sésame", "Graines de tournesol", "Haricots secs", "Huile de palme", "Ignames", "Lait cru de vache", "Laitue", "Lentilles", "Maïs", "Mangues", "Manioc frais", "Manioc séché", "Melons", "Miel naturel", "Mil", "Niébé sec", "Noix de cajou", "Oignons et échalotes secs (non déshydratés)", "Oignons verts", "Oranges", "Oseille", "Papayes", "Patates douces", "Persil", "Piments", "Pistaches en coque", "Plantains et bananes à cuire", "Poireaux", "Poivrons", "Pois d'Angole", "Pommes de terre", "Racines et tubercules comestibles à haute teneur en amidon ou en inuline, n.d.a., frais", "Riz", "Sorgho", "Tabac non manufacturé", "Taro", "Tomates", "Viande de bœuf avec os, fraîche ou réfrigérée (biologique)", "Viande de chèvre, fraîche ou réfrigérée (biologique)", "Viande de mouton, fraîche ou réfrigérée (biologique)", "Viande de porc avec os, fraîche ou réfrigérée (biologique)", "Viande de poulets, fraîche ou réfrigérée", "Viande de poulets, fraîche ou réfrigérée (biologique)"
    ];

    products.sort().forEach(product => {
        const option = document.createElement('option');
        option.value = product;
        option.textContent = product;
        productSelect.appendChild(option);
    });

    manualEntryLink.addEventListener('click', function (e) {
        e.preventDefault();
        productSelect.classList.toggle('hidden');
        manualProductInput.classList.toggle('hidden');
    });

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const product = manualProductInput.classList.contains('hidden') ? productSelect.value : manualProductInput.value;
        const region = document.getElementById('region').value;
        const date = document.getElementById('date').value;

        if (!product || !region || !date) {
            alert('Veuillez remplir tous les champs.');
            return;
        }

        loadingIndicator.classList.remove('hidden');
        resultsSection.style.display = 'none';
        insightsSection.style.display = 'none';

        try {
            const response = await fetch('/predict_price', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ product, region, date })
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.log('Détails de l’erreur serveur:', errorData);
                throw new Error(errorData.error || 'Erreur lors de la prédiction');
            }

            const data = await response.json();

            loadingIndicator.classList.add('hidden');
            resultsSection.style.display = 'block';
            insightsSection.style.display = 'block';

            document.getElementById('predicted-price').textContent = `${data.price} XAF`;
            document.getElementById('confidence-level').textContent = `${data.confidence.toFixed(0)}%`;
            document.getElementById('key-factors').textContent = data.factors.join(', ');

            const interpretationElement = document.getElementById('interpretation');
            if (interpretationElement) {
                interpretationElement.textContent = data.interpretation;
            }

            const recommendationsList = document.getElementById('recommendations');
            if (recommendationsList) {
                recommendationsList.innerHTML = '';
                data.recommendations.forEach(rec => {
                    const li = document.createElement('li');
                    li.textContent = rec;
                    recommendationsList.appendChild(li);
                });
            }

            // Ajouter une notification de prédiction (non persistante)
            window.addNotification(`Prédiction terminée pour ${product} dans ${region} : ${data.price} XAF`, 'prediction');

        } catch (error) {
            console.error('Erreur:', error);
            loadingIndicator.classList.add('hidden');
            window.addNotification(`Erreur lors de la prédiction pour ${product}.`, 'warning');
            alert(`Erreur: ${error.message}`);
        }
    });
});