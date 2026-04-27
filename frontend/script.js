const BASE_URL = "http://127.0.0.1:8000"
window.addEventListener("DOMContentLoaded", updateUI());

async function handleLogin(){
  const email = document.getElementById("email").value
  const password = document.getElementById("password").value

  const response = await fetch(`${BASE_URL}/user/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email: email, password: password })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    alert("Login successful!");
    updateUI(); // Update the UI to show workout section
  }
  else {
    alert("Login failed. Please check your credentials.");
  }
}

async function handleAddWorkout() {
  const name = document.getElementById('wName').value
  const type = document.getElementById('wType').value
  const duration = Number(document.getElementById('wDuration').value)
  const calories = Number(document.getElementById('wCalories').value)
  const notes = document.getElementById('wNotes').value
  const token = localStorage.getItem("token")

  const response = await fetch(`${BASE_URL}/workouts`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({
    workout_name: name,
    workout_type: type,
    duration_minutes: duration,
    calories_burned: calories,
    notes: notes
  })
});

if (response.ok) {
  alert("Workout logged successfully!");

  document.getElementById('wName').value = "";
  // Refresh the list!
  showWorkouts();
}
else {
  alert("Failed to log workout. Please try again.");
}

}


function logOut() {
  localStorage.removeItem("token");
  alert("Logged out successfully!");
  location.reload();
}

async function showWorkouts() {
  const token = localStorage.getItem("token");

  try {
    // 1. Send the request and wait for the response "envelope"
    const response = await fetch(`${BASE_URL}/workouts/all`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    // 2. Check if the server actually allowed us in (Status 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 3. Open the "envelope" and get the actual workout data
    const data = await response.json();
    
    // 4. Use the data (e.g., log it or show it on the UI)
    console.log("Workouts received:", data);
    displayWorkoutsOnPage(data); // A helper function to update your HTML

  } catch (error) {
    // This catches network failures or server crashes
    console.error("Error fetching workouts:", error);
  }
}

function displayWorkoutsOnPage(workouts) {
    const container = document.getElementById('workoutList'); // Assume you have a <div> with this ID
    container.innerHTML = ""; // Clear old stuff

    workouts.forEach(workout => {
        const div = document.createElement('div');
        div.className = 'workout-card';
        div.innerHTML = `
            <h3>${workout.workout_name}</h3>
            <p>Type: ${workout.workout_type}</p>
            <p>Duration: ${workout.duration_minutes} minutes</p>
            <p>Calories: ${workout.calories_burned}</p>
            <p>Notes: ${workout.notes}</p>
            <hr>
        `;
        container.appendChild(div);
    });
}

function updateUI() {
    const token = localStorage.getItem("token");
    const loginSection = document.getElementById("loginSection");
    const workoutSection = document.getElementById("workoutSection");

    if (token) {
        // If we have a token, hide Login and show Workouts
        loginSection.style.display = "none";
        workoutSection.style.display = "block";
        showWorkouts(); // Fetch the data now that we're "in"
    } else {
        // If no token, show Login and hide Workouts
        loginSection.style.display = "block";
        workoutSection.style.display = "none";
    }
}