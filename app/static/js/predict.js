document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('loading-indicator').classList.remove('hidden');
    document.querySelector('.prediction-results').style.display = 'none';
    document.querySelector('.prediction-insights').style.display = 'none';

    const formData = new FormData(event.target);
    fetch('/api/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading-indicator').classList.add('hidden');
        document.querySelector('.prediction-results').style.display = 'block';
        document.querySelector('.prediction-insights').style.display = 'block';
        
        // Mettre à jour le DOM avec les résultats de la prédiction
        document.getElementById('predicted-price').textContent = data.predicted_price;
        document.getElementById('confidence-level').textContent = data.confidence + '%';
        document.getElementById('key-factors').textContent = data.key_factors.join(', ');
        
        // Générer le graphique ici avec les données reçues
        // (Exemple avec Chart.js qui devrait être inclus dans votre HTML)
        let ctx = document.getElementById('prediction-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: data.chart_data,
            options: {...} // Options de configuration du graphique
        });
        
        // Mettre à jour les recommandations
        let recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = '';
        data.recommendations.forEach(rec => {
            let li = document.createElement('li');
            li.textContent = rec;
            recommendationsList.appendChild(li);
        });
    });
});