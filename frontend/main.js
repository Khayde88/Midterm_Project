// main.js
async function createTrack() {
    const title = document.getElementById('title').value;
    const artist = document.getElementById('artist').value;
    const duration = parseFloat(document.getElementById('duration').value);
    const genre = document.getElementById('genre').value;

    const response = await fetch('http://localhost:8000/tracks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title,
            artist,
            duration,
            genre,
        }),
    });

    if (response.ok) {
        loadTracks();
    } else {
        alert('Failed to add track');
    }
}


async function loadTracks() {
    const response = await fetch('http://localhost:8000/tracks/');
    const tracks = await response.json();

    const tableBody = document.querySelector('#tracksTable tbody');
    tableBody.innerHTML = '';

    tracks.forEach(track => {
        const row = tableBody.insertRow();
        row.innerHTML = `
            <td>${track.id}</td>
            <td>${track.title}</td>
            <td>${track.artist}</td>
            <td>${track.duration}</td>
            <td>${track.genre}</td>
            <td class="button-container">
                <button onclick="updateTrack(${track.id})">Update</button>
                <button onclick="deleteTrack(this)" data-id="${track.id}">Delete</button>
            </td>
        `;
    });
}

async function updateTrack(trackId) {
    // Get updated information from the user
    const updatedTitle = prompt('Enter updated title:');
    const updatedArtist = prompt('Enter updated artist:');
    const updatedDuration = parseFloat(prompt('Enter updated duration:'));
    const updatedGenre = prompt('Enter updated genre:');

    // Create an updated track object
    const updatedTrack = {
        id: trackId, 
        title: updatedTitle,
        artist: updatedArtist,
        duration: updatedDuration,
        genre: updatedGenre,
    };

    try {
        const response = await fetch(`http://localhost:8000/tracks/${trackId}`, {
            method: 'PUT',  // Use PUT method for updates
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedTrack),
        });

        if (response.status === 200) {
            console.log('Track updated successfully');
            // Refresh or update the UI if needed
            loadTracks();
        } else {
            console.error('Failed to update track:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error updating track:', error);
    }
}

// main.js
async function deleteTrack(button) {
    const trackId = button.getAttribute('data-id');

    try {
        const response = await fetch(`http://localhost:8000/tracks/${trackId}`, {
            method: 'DELETE',
        });

        if (response.status === 200) {
            console.log('Track deleted successfully');
            // Refresh or update the UI if needed
            loadTracks();
        } else {
            console.error('Failed to delete track:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error deleting track:', error);
    }
}



// Initial load of tracks
loadTracks();
