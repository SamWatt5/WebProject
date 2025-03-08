// const params = new URLSearchParams(window.location.search);
// const user = params.get("user");
const detailsDiv = document.getElementById("userDetails");
let userData = {};

const token = localStorage.getItem("token");
const user = jwt_decode(token).sub;
if (!token) {
    alert("You are not logged in!");
    window.location.href = "login.html";
} else {
    const user = jwt_decode(token).sub;
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
            renderProfileDetails();
        })
        .catch((error) => {
            console.error("Error fetching user data:", error);
            detailsDiv.innerHTML = `<p>Error fetching user data. Please try again later.</p>`;
        });
}

function renderProfileDetails() {
    detailsDiv.innerHTML = `
    <img src="${userData.profile_pic_url}" alt="Profile Picture" />
        <h2>${userData.first_name} ${userData.last_name}</h2>
        <ul>
            <li>Email: ${userData.email}</li>
            <li>Username: ${userData.username}</li>
            <li>Spotify Connected: ${userData.spotify_connected}</li>
            <li>Friends: ${userData.friends.join(", ")}</li>
        </ul>
        
        <input type="text" id="friendUsername" placeholder="Enter friend's username" />
        <button onclick="addFriend()">Add Friend</button>
        <button onclick="removeFriend()">Remove Friend</button>
    `;
}

function addFriend() {
    const friendUsername = document.getElementById("friendUsername").value;
    fetch(`http://localhost:8000/api/user/add-friend/${user}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ friend: friendUsername }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                alert(data.error);
                return;
            }
            // alert(data.message);
            // Update the userData object and re-render the profile details
            userData.friends.push(friendUsername);
            renderProfileDetails();
        })
        .catch((error) => {
            console.error("Error fetching user data:", error);
            detailsDiv.innerHTML = `<p>Error fetching user data. Please try again later.</p>`;
        });
}

function removeFriend() {
    const friendUsername = document.getElementById("friendUsername").value;
    fetch(`http://localhost:8000/api/user/remove-friend/${user}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ friend: friendUsername }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                alert(data.error);
                return;
            }
            // Remove the friend from the userData object and re-render the profile details
            userData.friends = userData.friends.filter((friend) => friend !== friendUsername);
            renderProfileDetails();
        })
        .catch((error) => {
            console.error("Error removing friend:", error);
            detailsDiv.innerHTML = `<p>Error removing friend. Please try again later.</p>`;
        });
}
