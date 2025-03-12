document.addEventListener('DOMContentLoaded', function () {
    const manualEntryLink = document.getElementById('manual-entry');
    const manualProductInput = document.getElementById('manual-product');
    const productSelect = document.getElementById('product');

    // Liste des produits triés par ordre alphabétique
    const products = [
        "Ananas", "Arachides, non décortiquées", "Aubergines", "Avocats", "Bananes", "Basilic", "Carottes", "Café vert", "Choux", "Citrons", "Citrouilles", "Concombres", "Coriandre", "Courges", "Épinards", "Fèves de cacao", "Fibre de coton, égrenée", "Fonio", "Fruits de la passion", "Gingembre", "Gombos", "Goyaves", "Graines de sésame", "Graines de tournesol", "Haricots secs", "Huile de palme", "Ignames", "Lait cru de vache", "Laitue", "Lentilles", "Maïs", "Mangues", "Manioc frais", "Manioc séché", "Melons", "Miel naturel", "Mil", "Niébé sec", "Noix de cajou", "Oignons et échalotes secs (non déshydratés)", "Oignons verts", "Oranges", "Oseille", "Papayes", "Patates douces", "Persil", "Piments", "Pistaches en coque", "Plantains et bananes à cuire", "Poireaux", "Poivrons", "Pois d'Angole", "Pommes de terre", "Racines et tubercules comestibles à haute teneur en amidon ou en inuline, n.d.a., frais", "Riz", "Sorgho", "Tabac non manufacturé", "Taro", "Tomates", "Viande de bœuf avec os, fraîche ou réfrigérée (biologique)", "Viande de chèvre, fraîche ou réfrigérée (biologique)", "Viande de mouton, fraîche ou réfrigérée (biologique)", "Viande de porc avec os, fraîche ou réfrigérée (biologique)", "Viande de poulets, fraîche ou réfrigérée", "Viande de poulets, fraîche ou réfrigérée (biologique)"
    ];

    // Ajouter les produits triés à la liste déroulante
    products.sort().forEach(product => {
        const option = document.createElement('option');
        option.value = product;
        option.textContent = product;
        productSelect.appendChild(option);
    });

    // Basculer entre sélection et saisie manuelle
    manualEntryLink.addEventListener('click', function (e) {
        e.preventDefault();
        productSelect.classList.toggle('hidden');
        manualProductInput.classList.toggle('hidden');
    });

    // Gérer la soumission du formulaire
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Afficher l'indicateur de chargement
        document.getElementById('loading-indicator').classList.remove('hidden');

        // Simuler une prédiction
        setTimeout(() => {
            document.getElementById('loading-indicator').classList.add('hidden');
            document.getElementById('results').style.display = 'block';
            document.getElementById('insights').style.display = 'block';

            // Afficher des résultats fictifs
            document.getElementById('predicted-price').textContent = '5000 XAF';
            document.getElementById('confidence-level').textContent = '75%';
            document.getElementById('key-factors').textContent = 'Demande élevée, faible production';

            // Ajouter des recommandations fictives
            const recommendations = document.getElementById('recommendations');
            recommendations.innerHTML = `
                <li>Augmenter la production pour répondre à la demande.</li>
                <li>Surveiller les tendances saisonnières.</li>
                <li>Considérer une diversification des cultures.</li>
            `;
        }, 2000);
    });
});