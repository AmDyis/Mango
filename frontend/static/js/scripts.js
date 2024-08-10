document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
});

function initializeEventListeners() {
    document.getElementById('searchForm').addEventListener('submit', handleSearchSubmit);
}

function handleSearchSubmit(event) {
    event.preventDefault();
    const query = document.getElementById('searchQuery').value;
    window.location.href = `/search?query=${encodeURIComponent(query)}`;
}


async function fetchAnimeCharacters(animeId) {
    try {
        const charactersResponse = await fetch(`/anime/${animeId}/characters`);
        const charactersResults = await charactersResponse.json();
        return charactersResults.data || [];
    } catch (error) {
        console.error('Error fetching characters:', error);
        return [];
    }
}

async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint);
        const results = await response.json();

        if (!results || !results.data) {
            document.getElementById('results').innerHTML = '<p>No data found.</p>';
            return;
        }

        const data = results.data;
        const dataId = data.mal_id;

        const characters = await fetchAnimeCharacters(dataId);
        displayAnimeData(data, characters);
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('results').innerHTML = '<p>Error fetching data.</p>';
    }
}

function displayAnimeData(anime, characters) {
    const charactersHTML = characters.map(character => `
        <li>${character.character.name}</li>
    `).join('');

    const resultHTML = `    
        <div class="anime-card">
            <img src="${anime.images.webp.large_image_url}" 
            alt="${anime.title}">
            <div class="anime-details">
                <h2 class="anime-title">${anime.title}</h2>
                <p class="anime-synopsis">${anime.synopsis}</p>
                <div class="anime-info">
                    <div><strong>Score:</strong> ${anime.score}</div>
                    <div><strong>Episodes:</strong> ${anime.episodes}</div>
                    <div><strong>Air Dates:</strong> ${anime.aired.string}</div>
                </div>
                <a href="${anime.url}" target="_blank">More Info</a>
                <div class="anime-characters">
                    <h3>Characters</h3>
                    <ul>
                        ${charactersHTML}
                    </ul>
                </div>
            </div>
        </div>
    `;
    document.getElementById('results').innerHTML = resultHTML;
}
let leftButtonPressed = false;
let rightButtonPressed = false;
let gifPlayed = false;

function handleGifButtonClick(button) {
    if (button === 'left') {
        leftButtonPressed = true;
    } else if (button === 'right') {
        rightButtonPressed = true;
    }

    checkAndAnimateCircles();
}

function checkAndAnimateCircles() {
    if (leftButtonPressed && rightButtonPressed && !gifPlayed) {
        const blueButton = document.querySelector('button.circle-button.blue');
        const redButton = document.querySelector('button.circle-button.red');

        blueButton.classList.add('animate');
        redButton.classList.add('animate');

        // После завершения анимации скрываем кнопки и показываем гифку
        setTimeout(() => {
            blueButton.style.display = 'none';
            redButton.style.display = 'none';
            playGif();
        }, 2000); // Время анимации кнопок

        gifPlayed = true;
    }
}

function playGif() {
    const gif = document.getElementById('gif');

    // Сбрасываем src для гифки, чтобы она начиналась с начала
    gif.style.display = 'none'; // Сначала скрываем гифку
    gif.src = ''; // Очищаем src

    setTimeout(() => {
        gif.src = 'static/othergif/gojo.gif'; // Задаем путь к гифке заново
        gif.style.display = 'block'; // Показываем гифку

        setTimeout(() => {
            gif.style.display = 'none'; // Скрываем гифку через 5 секунд
            resetCircles(); // Возвращаем кнопки на исходные позиции
        }, 5000); // Длительность показа гифки
    }, 50); // Небольшая задержка, чтобы сброс src успел сработать
}
function resetCircles() {
    const blueButton = document.querySelector('button.circle-button.blue');
    const redButton = document.querySelector('button.circle-button.red');

    blueButton.classList.remove('animate');
    redButton.classList.remove('animate');

    // Возвращаем кнопки на исходные позиции
    blueButton.style.left = '10px';
    redButton.style.right = '10px';

    // Показываем кнопки снова
    blueButton.style.display = 'block';
    redButton.style.display = 'block';

    gifPlayed = false; // Сбрасываем флаг, чтобы позволить повторное проигрывание
    leftButtonPressed = false;
    rightButtonPressed = false;
}

