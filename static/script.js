document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const queryInput = document.getElementById('query');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    searchForm.reset();

    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset UI
        resultsDiv.innerHTML = '';
        errorDiv.classList.add('d-none');
        loadingDiv.classList.remove('d-none');

        const query = queryInput.value.trim();
        
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `query=${encodeURIComponent(query)}`
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                throw new Error(data.error || 'An error occurred');
            }
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('d-none');
        } finally {
            loadingDiv.classList.add('d-none');
        }
    });

    function displayResults(data) {
        if (!data) {
            resultsDiv.innerHTML = '<p class="text-center">No weather data available.</p>';
            return;
        }
        // Display current weather
        const currentWeather = `
            <div class="result-item mb-4">
                <h4 class="text-center mb-3">Weather in ${data.city}</h4>
                <div class="container mb-4">
                    <div class="row">
                        <img src="${data.granma}" class="img-fluid rounded mx-auto d-block col" alt="an image of an elderly lady">
                        <p class="text-center col">${data.recommendations}</p>
                    </div>
                </div>
                <div class="row text-center">
                    <div class="col-md-4">
                        <h5>Temperature</h5>
                        <p>${data.current.temperature}°C</p>
                    </div>
                    <div class="col-md-4">
                        <h5>Humidity</h5>
                        <p>${data.current.humidity}%</p>
                    </div>
                    <div class="col-md-4">
                        <h5>Wind Speed</h5>
                        <p>${data.current.wind_speed} km/h</p>
                    </div>
                </div>
            </div>
        `;

        const image = `<div class="container-md"><div class="text-center mb-4">Also make sure you check the forecast for the coming days below the picture.</div><img src="${data.image}" class="img-fluid rounded mx-auto d-block" alt="${data.city}"></div>`
        // Display 7-day forecast
        const forecast = `
            <div class="result-item">
                <h4 class="text-center mb-3">7-Day Forecast</h4>
                <div class="row">
                    ${data.daily.map(day => `
                        <div class="col-md-4 mb-3">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <h5>${new Date(day.date).toLocaleDateString()}</h5>
                                    <p class="mb-1">Max: ${day.max_temp}°C</p>
                                    <p class="mb-1">Min: ${day.min_temp}°C</p>
                                    <p class="mb-0">Precipitation: ${day.precipitation}mm</p>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        resultsDiv.innerHTML = currentWeather + image + forecast;
    }
}); 