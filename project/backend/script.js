async function fetchUserPlaylists() {
    const response = await fetch("http://localhost:8000/api/spotify/me_playlists", {
        credentials: "include", // Ensures the session cookie is sent with the request
    });
    if (!response.ok) {
        console.log("it threw an error here");
        throw new Error(`Server error: ${response.status}`);
    }
    data = await response.json();
    // localStorage.setItem("user_playlists", JSON.stringify(data));
    return data;
}

async function fetchPlaylistContents(playlistId) {
    let data = localStorage.getItem(playlistId);
    if (!data) {
        const response = await fetch(`http://localhost:8000/api/spotify/playlist/${playlistId}/tracks`, {
            credentials: "include", // Ensures the session cookie is sent with the request
        });
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        data = await response.json();
        localStorage.setItem(playlistId, JSON.stringify(data));
    } else {
        data = JSON.parse(data);
    }
    return data;
}

function createPlaylistArea(data) {
    const playlistContainer = document.querySelector(".playlist");
    data.items.forEach((playlist) => {
        playlistContainer.appendChild(createUserPlaylistCard(playlist));
    });
}

function createUserPlaylistCard(playlist) {
    const card = document.createElement("div");
    card.className = "col-md-4 mb-3";
    const imageUrl = playlist.images && playlist.images.length > 0 ? playlist.images[0].url : "default-image-url.jpg";
    card.innerHTML = `
            <div class="col">
                <div class="card" style="width: 18rem;">
                    <img src="${imageUrl}" class="card-img-top" alt="${playlist.name} cover">
                    <div class="card-body">
                        <h5 class="card-title">${playlist.name}</h5>
                        <p class="card-text">${playlist.description}</p>
                        <a href="${playlist.external_urls.spotify}" class="btn btn-primary" target="_blank">Open in Spotify</a>
                        <button onclick="togglePlaylist('${playlist.id}')" class="btn btn-primary" target="_blank">Expand</a>
                        
                    </div>
                    <div id="${playlist.id}-expanded"></div>
                </div>
            </div>
        `;
    return card;
}

function togglePlaylist(playlistId) {
    const expandedDiv = document.getElementById(`${playlistId}-expanded`);
    if (expandedDiv.innerHTML === "") {
        expandPlaylist(playlistId);
    } else {
        contractPlaylist(playlistId);
    }
}

function expandPlaylist(playlistId) {
    fetchPlaylistContents(playlistId).then((data) => {
        const expandedDiv = document.getElementById(`${playlistId}-expanded`);
        let tracks = "<ul>";
        data.items.forEach((item) => {
            const track = item.track;
            const artists = track.artists.map((artist) => artist.name).join(", ");
            tracks += `<li>${track.name} - ${artists}</li>`;
        });
        tracks += "</ul>";
        expandedDiv.innerHTML = tracks;
    });
}

function contractPlaylist(playlistId) {
    const expandedDiv = document.getElementById(`${playlistId}-expanded`);
    expandedDiv.innerHTML = "";
}

async function initialize() {
    // const data = await fetchUserPlaylists();
    console.log("teuiefuios")
    createPlaylistArea(data);
}

console.log("teuiefuios1223444")
initialize();
