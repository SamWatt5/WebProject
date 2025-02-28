const params = new URLSearchParams(window.location.search);
const user = params.get("user");
const detailsDiv = document.getElementById("userDetails");
let userData = {};

fetch(`http://localhost:8000/api/user/profile/${user}`)
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        userData = data;
        detailsDiv.innerHTML = `
        <h2>${data.first_name} ${data.last_name}</h2>
        <ul>
            <li>Email: ${data.email}</li>
            <li>Username: ${data.username}</li>
            <li>Profile Picture: <img src="${data.profile_pic_url}" alt="Profile Picture"></li>
            <li>Spotify Connected: ${data.spotify_connected}</li>
            <li>Friends: ${data.friends.join(", ")}</li>
        </ul>
        <a href="index.html">Back To Home</a><br>
    `;
    });
