const getRecsBtn = document.getElementById('get-recs-btn');
const recommendationsContainer = document.getElementById('recommendations-container');

const fetchRecommendations = async () => {
    recommendationsContainer.innerHTML = '<div class="loader"></div>';
    try {
        const response = await fetch(`https://product-recommender-c4fb.onrender.com/recommendations`, {
            credentials: 'include'
        });
        if (!response.ok) throw new Error('Network response was not ok');
        
        const recommendations = await response.json();
        recommendationsContainer.innerHTML = '';

        if (recommendations.length === 0) {
            recommendationsContainer.innerHTML = '<div class="placeholder"><p>No new recommendations for you right now!</p></div>';
            return;
        }

        recommendations.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'card';
            
            const platformsArray = rec.platforms.split('|');
            let platformsHTML = '';
            platformsArray.forEach(platform => {
                platformsHTML += `<a href="https://www.google.com/search?q=${encodeURIComponent(rec.product_name + ' ' + platform)}" target="_blank" class="platform-link">${platform}</a>`;
            });

            card.innerHTML = `
                <img src="${rec.image_url}" alt="${rec.product_name}" class="card-image">
                <div class="card-content">
                    <h3>${rec.product_name}</h3>
                    <p class="category">${rec.category}</p>
                    <p class="explanation"><strong>Why you might like this:</strong> ${rec.explanation}</p>
                    
                    <div class="platforms">
                        <span>Available on:</span>
                        ${platformsHTML}
                    </div>
                </div>
            `;
            
            recommendationsContainer.appendChild(card);
        });

    } catch (error) {
        console.error('There was a problem fetching recommendations:', error);
        recommendationsContainer.innerHTML = '<div class="placeholder"><p>Oops! Something went wrong. Please try again.</p></div>';
    }
};


getRecsBtn.addEventListener('click', fetchRecommendations);

