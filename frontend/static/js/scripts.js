document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
});

function initializeEventListeners() {
    document.getElementById('searchForm').addEventListener('submit', handleSearchSubmit);
    document.getElementById('randomAnimeButton').addEventListener('click', fetchRandomAnime);
    document.getElementById('charactersButton').addEventListener('click', fetchCharacters);
    document.getElementById('genresButton').addEventListener('click', fetchGenres);
    document.getElementById('personButton').addEventListener('click', fetchPersons);
    document.getElementById('producersButton').addEventListener('click', fetchProducers);
    document.getElementById('seasonsButton').addEventListener('click', fetchSeasons);
    document.getElementById('topButton').addEventListener('click', fetchTopAnime);
}

async function handleSearchSubmit(event) {
    event.preventDefault();
    const query = document.getElementById('searchQuery').value;
    await fetchAnimeData(query);
}

async function fetchAnimeData(query) {
    try {
        const response = await fetch(`/anime/${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data) {
            const characters = await fetchAnimeCharacters(data.mal_id);
            displayAnimeData(data, characters);
        } else {
            document.getElementById('results').innerHTML = '<p>Anime not found.</p>';
        }
    } catch (error) {
        console.error('Error fetching anime data:', error);
        document.getElementById('results').innerHTML = '<p>Error fetching data.</p>';
    }
}

async function fetchAnimeCharacters(animeId) {
    try {
        const response = await fetch(`/anime/${animeId}/characters`);
        const data = await response.json();
        return data.characters || [];
    } catch (error) {
        console.error('Error fetching characters:', error);
        return [];
    }
}

function displayAnimeData(anime, characters) {
    const charactersHTML = characters.map(character => `
        <li>${character.name}</li>
    `).join('');

    const resultHTML = `    
        <div class="anime-card">
            <img src="${anime.images.webp.large_image_url}" alt="${anime.title}">
            <div class="anime-details">
                <h2>${anime.title}</h2>
                <p>${anime.synopsis}</p>
                <div class="anime-info">
                    <div><strong>Score:</strong> ${anime.score}</div>
                    <div><strong>Episodes:</strong> ${anime.episodes}</div>
                    <div><strong>Air Dates:</strong> ${anime.aired.string}</div>
                </div>
                <a href="${anime.url}" target="_blank">More Info</a>
                <div class="anime-characters">
                    <h3>Characters</h3>
                    <ul>${charactersHTML}</ul>
                </div>
            </div>
        </div>
    `;
    document.getElementById('results').innerHTML = resultHTML;
}

async function fetchRandomAnime() {
    try {
        const response = await fetch('/anime/random');
        const data = await response.json();
        if (data) {
            await fetchAnimeData(data.mal_id); // Ищем случайное аниме
        } else {
            document.getElementById('results').innerHTML = '<p>Random anime not found.</p>';
        }
    } catch (error) {
        console.error('Error fetching random anime:', error);
        document.getElementById('results').innerHTML = '<p>Error fetching random anime.</p>';
    }
}

async function fetchGenres() {
    try {
        const response = await fetch('/genres/anime');
        const data = await response.json();
        displayGenres(data.genres);
    } catch (error) {
        console.error('Error fetching genres:', error);
        document.getElementById('results').innerHTML = '<p>Error fetching genres.</p>';
    }
}

function displayGenres(genres) {
    const genresHTML = genres.map(genre => `<li>${genre.name}</li>`).join('');
    document.getElementById('results').innerHTML = `<ul>${genresHTML}</ul>`;
}

async function fetchCharacters() {
    // Подобным образом реализуйте функцию для получения персонажей
}

async function fetchPersons() {
    // Подобным образом реализуйте функцию для получения персон
}

async function fetchProducers() {
    // Подобным образом реализуйте функцию для получения продюсеров
}

async function fetchSeasons() {
    // Подобным образом реализуйте функцию для получения сезонов
}

async function fetchTopAnime() {
    try {
        const response = await fetch('/top/anime');
        const data = await response.json();
        displayTopAnime(data.top);
    } catch (error) {
        console.error('Error fetching top anime:', error);
        document.getElementById('results').innerHTML = '<p>Error fetching top anime.</p>';
    }
}

function displayTopAnime(topAnime) {
    const topAnimeHTML = topAnime.map(anime => `
        <div class="anime-card">
            <img src="${anime.images.webp.large_image_url}" alt="${anime.title}">
            <h2>${anime.title}</h2>
            <p>${anime.synopsis}</p>
        </div>
    `).join('');
    document.getElementById('results').innerHTML = topAnimeHTML;
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

