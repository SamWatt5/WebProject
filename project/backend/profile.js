const params = new URLSearchParams(window.location.search);
const user = params.get("user");
const detailsDiv = document.getElementById("userDetails");
let userData = {};

const token = localStorage.getItem("token");

if (!token) {
    alert("You are not logged in!");
    window.location.href = "login.html";
} else {
    fetch(`http://localhost:8000/api/user/profile/${user}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                detailsDiv.innerHTML = `<p>${data.error}</p>`;
                return;
            }
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
        })
        .catch((error) => {
            console.error("Error fetching user data:", error);
            detailsDiv.innerHTML = `<p>Error fetching user data. Please try again later.</p>`;
        });
}
