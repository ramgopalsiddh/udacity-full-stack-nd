document.addEventListener('DOMContentLoaded', function () {
    // Initial load
    getMovies();
    getActors();

    // Event listeners
    document.getElementById('create-movie-form').addEventListener('submit', function (e) {
        e.preventDefault();
        createMovie();
    });

    document.getElementById('create-actor-form').addEventListener('submit', function (e) {
        e.preventDefault();
        createActor();
    });
});

function getMovies() {
    fetch('http://localhost:8080/movies')
        .then(response => response.json())
        .then(data => {
            displayMovies(data.movies);
        })
        .catch(error => console.error('Error fetching movies:', error));
}

function getActors() {
    fetch('http://localhost:8080/actors')
        .then(response => response.json())
        .then(data => {
            displayActors(data.actors);
        })
        .catch(error => console.error('Error fetching actors:', error));
}

function displayMovies(movies) {
    const moviesList = document.getElementById('movies-list');
    moviesList.innerHTML = '';
    movies.forEach(movie => {
        const listItem = document.createElement('li');
        listItem.textContent = `${movie.title} (Release Date: ${movie.release_date})`;
        moviesList.appendChild(listItem);

        // Add click event to show details
        listItem.addEventListener('click', function () {
            showDetails(movie.id, 'movie');
        });
    });
}

function displayActors(actors) {
    const actorsList = document.getElementById('actors-list');
    actorsList.innerHTML = '';
    actors.forEach(actor => {
        const listItem = document.createElement('li');
        listItem.textContent = `${actor.name} (Age: ${actor.age}, Gender: ${actor.gender})`;
        actorsList.appendChild(listItem);

        // Add click event to show details
        listItem.addEventListener('click', function () {
            showDetails(actor.id, 'actor');
        });
    });
}

function createMovie() {
    const title = document.getElementById('create-movie-title').value;
    const releaseDate = document.getElementById('create-movie-release-date').value;

    fetch('http://localhost:8080/movies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            release_date: releaseDate
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            getMovies(); // Refresh the movie list
        } else {
            displayErrorMessage('Failed to create movie.');
        }
    })
    .catch(error => console.error('Error creating movie:', error));
}

function createActor() {
    const name = document.getElementById('create-actor-name').value;
    const age = document.getElementById('create-actor-age').value;
    const gender = document.getElementById('create-actor-gender').value;
    const movieId = document.getElementById('create-actor-movie-id').value;

    fetch('http://localhost:8080/actors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            age: age,
            gender: gender,
            movie_id: movieId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            getActors(); // Refresh the actor list
        } else {
            displayErrorMessage('Failed to create actor.');
        }
    })
    .catch(error => console.error('Error creating actor:', error));
}

function showDetails(id, type) {
    const detailsModal = document.getElementById('details-modal');
    const detailsTitle = document.getElementById('details-title');
    const detailsReleaseDate = document.getElementById('details-release-date');
    const detailsActors = document.getElementById('details-actors');

    // TODO: Fetch details based on the 'type' (movie or actor) and 'id'
    // Update the modal content and display the modal
}

function closeDetailsModal() {
    document.getElementById('details-modal').style.display = 'none';
}

function displayErrorMessage(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    setTimeout(() => {
        errorMessage.textContent = '';
    }, 5000);
}
