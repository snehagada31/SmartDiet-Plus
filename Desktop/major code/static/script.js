// script.js

// --- Global DOM Elements (find them once when the script loads) ---
const allBackButtons = document.querySelectorAll('.back-button');

// --- NEW HELPER: Function to Clear Profile Form Fields ---
function clearProfileForm() {
    // List all IDs for the input fields on the profile section
    const idsToClear = [
        'name', 'age', 'email', 'password', 'confirm_password', 
        'occupation', 'citySelect', 'allergies', 'notes'
    ];

    idsToClear.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            // Reset the value of the input/textarea field
            element.value = '';
        }
    });

    // Reset dropdowns (select elements) to their first option
    const genderSelect = document.getElementById('gender');
    if (genderSelect) genderSelect.selectedIndex = 0;

    const dietSelect = document.getElementById('dietPreference');
    if (dietSelect) dietSelect.selectedIndex = 0;

    // Also clear the recommendation output area
    const recOutput = document.getElementById('recommendationOutput');
    if (recOutput) recOutput.innerHTML = '';
}
// --- END NEW HELPER ---


// --- Helper function to control back button visibility ---
function toggleBackButtons(show) {
    allBackButtons.forEach(button => {
        button.style.display = show ? 'inline-block' : 'none';
    });
}

function handleEnterKey(event, nextElementId) {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        const nextElement = document.getElementById(nextElementId);
        if (nextElement) {
            nextElement.focus();
        }
    }
}

// --- Main Navigation Function ---
function showContent(sectionId) {
    const targetElement = document.getElementById(sectionId);
    if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, '', `#${sectionId}`);
    }

    if (sectionId !== 'profile') {
        toggleBackButtons(true);
    } else {
        toggleBackButtons(false);
    }
}

// --- Function for the back button's click event ---
function goBackToProfile() {
    showContent('profile'); 
}


// --- MODIFIED: Theme Toggling Logic ---
function toggleTheme() {
    document.body.classList.toggle("theme-dark");
    if (document.body.classList.contains('theme-dark')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}


// --- Your Existing Popup Functions (UNCHANGED) ---
function openPopup(id) {
    document.getElementById("overlay").style.display = "block";
    document.getElementById(id).style.display = "flex"; 
    document.getElementById(id).focus();
}

function closePopup() {
    document.getElementById("overlay").style.display = "none";
    document.querySelectorAll(".popup").forEach(popup => {
        popup.style.display = "none";
    });
}

// --- Your Existing Navigation to Filtered Recipes (UNCHANGED) ---
function navigateToFilteredRecipes() {
    const dietPreference = document.getElementById('dietPreference').value;
    const allergies = document.getElementById('allergies').value.trim();

    let queryParams = new URLSearchParams();

    let dietFilterValue = '';
    if (dietPreference === 'Vegetarian') {
        dietFilterValue = 'vegetarian';
    } else if (dietPreference === 'Non-Vegetarian') {
        dietFilterValue = 'non-vegetarian';
    } else if (dietPreference === 'Vegan') {
        dietFilterValue = 'vegan';
    } else if (dietPreference === 'Gluten-Free') {
        dietFilterValue = 'gluten-free';
    }
    if (dietFilterValue) {
        queryParams.append('diet', dietFilterValue);
    }

    if (allergies) {
        const allergyList = allergies.split(',').map(item => item.trim().toLowerCase()).filter(item => item !== '');
        allergyList.forEach(allergy => {
            queryParams.append('allergy', allergy);
        });
    }

    const baseUrl = '/recipes';
    const fullUrl = `${baseUrl}?${queryParams.toString()}`;

    window.location.href = fullUrl;
}

// --- MODIFIED: Profile Validation and Submission (FIXED) ---
async function validateProfile() {
    // 1. Data Collection (Collecting values from input IDs)
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value.trim();
    const gender = document.getElementById("gender").value;
    const occupation = document.getElementById("occupation").value.trim();
    const citySelectElement = document.getElementById("citySelect");
    const city = citySelectElement ? citySelectElement.value : "";
    const dietPreference = document.getElementById("dietPreference").value;
    const allergies = document.getElementById("allergies").value.trim();
    const notes = document.getElementById("notes").value.trim();
    const emailInput = document.getElementById("email");
    const email = emailInput ? emailInput.value.trim() : "";

    // Retrieve password values
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");

    const password = passwordInput ? passwordInput.value : "";
    const confirmPassword = confirmPasswordInput ? confirmPasswordInput.value : "";

    // 2. Client-Side Validation for Required Fields
    if (!name || !age || !gender || !email || !password || !confirmPassword) {
        alert("Please fill out all required profile fields (Name, Age, Gender, Email, and Password).");
        return;
    }
    
    // Check if passwords match
    if (password !== confirmPassword) {
        alert("Passwords do not match. Please re-enter.");
        return; 
    }
    // End Validation

    // 3. Prepare Data Object
    const userData = {
        username: name,
        age: parseInt(age),
        email: email,
        password: password, 
        gender: gender,
        diet_preference: dietPreference,
        occupation: occupation,
        city: city,
        allergies: allergies,
        notes: notes
    };

    // 4. Send Data to Flask Backend
    try {
        const response = await fetch("http://localhost:5000/submit_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Success:', data);
            alert(data.message || "Profile data saved successfully! You can now log in.");
            
            // 🚨 ACTION 1: Clear the form fields locally
            clearProfileForm(); 

            // 🚨 ACTION 2: FORCED RELOAD TO CLEAR BROWSER CACHE
            window.location.reload(); 

        } else {
            console.error('Error:', data);
            alert(data.error || "Failed to save profile data."); 
        }

    } catch (error) {
        console.error("Fetch Error:", error);
        alert("Something went wrong while submitting your profile.");
    }
}

// --- Your Existing Calorie Tracking (UNCHANGED) ---
function getTodayDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

async function logFood() {
    const foodItem = document.getElementById('logFoodItem').value.trim();
    const caloriesInput = document.getElementById('logCalories').value.trim();
    const proteinInput = document.getElementById('logProtein').value.trim();
    const carbsInput = document.getElementById('logCarbs').value.trim();
    const fatInput = document.getElementById('logFat').value.trim();
    const mealType = document.getElementById('logMealType').value;
    const logDate = document.getElementById('logDate').value;

    if (!foodItem || !caloriesInput || !proteinInput || !carbsInput || !fatInput || !mealType || !logDate) {
        showErrorMessage("Please fill in all food log fields.");
        return;
    }

    let calories, protein, carbs, fat;
    try {
        calories = parseFloat(caloriesInput);
        protein = parseFloat(proteinInput);
        carbs = parseFloat(carbsInput);
        fat = parseFloat(fatInput);
        if (isNaN(calories) || isNaN(protein) || isNaN(carbs) || isNaN(fat) || calories < 0 || protein < 0 || carbs < 0 || fat < 0) {
            showErrorMessage("Please enter valid non-negative numbers for all nutrient fields.");
            return;
        }
    } catch (e) {
        showErrorMessage("Invalid nutrient amount.");
        return;
    }

    const userId = "demo_user_id"; 

    try {
        const response = await fetch('/log_food', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                food_item: foodItem,
                calories: calories,
                protein: protein,
                carbs: carbs,
                fat: fat,
                meal_type: mealType,
                log_date: logDate
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Server error logging food: ${response.status} - ${errorData.error}`);
        }

        const result = await response.json();
        alert(result.message); 

        // Clear input fields after successful log
        document.getElementById('logFoodItem').value = '';
        document.getElementById('logCalories').value = '';
        document.getElementById('logProtein').value = '0';
        document.getElementById('logCarbs').value = '0';
        document.getElementById('logFat').value = '0';
        document.getElementById('logMealType').value = 'Breakfast';

        loadDailyCalorieSummary(); 

    } catch (error) {
        console.error("Error logging food:", error);
        showErrorMessage(`Error adding food: ${error.message || error}`);
    }
}

async function loadDailyCalorieSummary() {
    const logDate = document.getElementById('logDate').value;
    const userId = "demo_user_id"; 

    if (!logDate) {
        document.getElementById('currentSummaryDate').textContent = 'N/A';
        document.getElementById('totalCalories').textContent = '0';
        document.getElementById('totalProtein').textContent = '0';
        document.getElementById('totalCarbs').textContent = '0';
        document.getElementById('totalFat').textContent = '0';
        document.getElementById('calorieProgress').value = 0;
        document.getElementById('calorieStatus').textContent = 'Please select a date.';
        document.getElementById('loggedFoodsList').innerHTML = '<li>No food logged for this date.</li>';
        return;
    }

    try {
        const response = await fetch(`/get_daily_calorie_summary?user_id=${userId}&log_date=${logDate}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to load daily summary: ${response.status} - ${errorData.error}`);
        }

        const data = await response.json();
        
        document.getElementById('currentSummaryDate').textContent = data.date === getTodayDate() ? 'Today' : data.date;

        const totalCalories = data.total_calories || 0;
        const totalProtein = data.total_protein || 0;
        const totalCarbs = data.total_carbs || 0;
        const totalFat = data.total_fat || 0;

        document.getElementById('totalCalories').textContent = totalCalories.toFixed(0);
        document.getElementById('totalProtein').textContent = totalProtein.toFixed(1);
        document.getElementById('totalCarbs').textContent = totalCarbs.toFixed(1);
        document.getElementById('totalFat').textContent = totalFat.toFixed(1);

        // NEW: Get goals from response and display (assuming app.py sends 'goals' object)
        const calorieGoal = data.goals ? data.goals.calorie : 2200; 
        const proteinGoal = data.goals ? data.goals.protein : 70;
        const carbsGoal = data.goals ? data.goals.carbs : 250;
        const fatGoal = data.goals ? data.goals.fat : 60;

        // Ensure these span IDs exist in your index.html's calorieSummaryOutput
        if (document.getElementById('dailyCalorieGoal')) document.getElementById('dailyCalorieGoal').textContent = calorieGoal.toFixed(0);
        if (document.getElementById('dailyProteinGoal')) document.getElementById('dailyProteinGoal').textContent = proteinGoal.toFixed(1);
        if (document.getElementById('dailyCarbsGoal')) document.getElementById('dailyCarbsGoal').textContent = carbsGoal.toFixed(1);
        if (document.getElementById('dailyFatGoal')) document.getElementById('dailyFatGoal').textContent = fatGoal.toFixed(1);


        document.getElementById('calorieProgress').value = totalCalories;
        document.getElementById('calorieProgress').max = calorieGoal;
        document.getElementById('calorieStatus').textContent = `You've consumed ${totalCalories.toFixed(0)} out of ${calorieGoal} calories today.`;

        const loggedFoodsList = document.getElementById('loggedFoodsList');
        loggedFoodsList.innerHTML = ''; 

        if (data.food_logs && data.food_logs.length > 0) {
            data.food_logs.forEach(log => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <strong>${log.meal_type}</strong>: ${log.food_item} - ${log.calories} kcal
                    (P: ${log.protein}g, C: ${log.carbs}g, F: ${log.fat}g)
                    <button class="delete-food-btn" data-log-id="${log.id}">Delete</button>
                `;
                loggedFoodsList.appendChild(li);
            });
            document.querySelectorAll('.delete-food-btn').forEach(button => {
                button.addEventListener('click', (event) => {
                    const logId = event.target.dataset.logId;
                    deleteFoodLog(logId);
                });
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No food logged for this date.';
            loggedFoodsList.appendChild(li);
        }

    } catch (error) {
        console.error("Error loading daily calorie summary:", error);
        showErrorMessage(`Something went wrong while loading daily summary: ${error.message || error}`);
    }
}

async function deleteFoodLog(logId) {
    if (!confirm("Are you sure you want to delete this food entry?")) {
        return;
    }

    try {
        const response = await fetch(`/delete_food_log/${logId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to delete food log: ${response.status} - ${errorData.error}`);
        }

        const result = await response.json();
        alert(result.message); 
        loadDailyCalorieSummary(); 

    } catch (error) {
        console.error("Error deleting food log:", error);
        showErrorMessage(`Something went wrong while deleting food entry: ${error.message || error}`);
    }
}

// --- Your Existing Smart Meal Generation (UNCHANGED) ---
function generateSmartMeal() {
    const meals = [
        "Quinoa Salad with Chickpeas",
        "Grilled Tofu Stir-Fry",
        "Oats with Berries and Almonds",
        "Lentil Soup with Whole Grain Bread", 
        "Veggie Wrap with Hummus"
    ];
    const randomMeal = meals[Math.floor(Math.random() * meals.length)];
    const outputDiv = document.getElementById("smartMealOutput");

    if (outputDiv) {
        outputDiv.innerText = `Suggested Smart Meal: ${randomMeal}`;
    } else {
        console.warn("smartMealOutput div not found in DOM.");
    }
}

// --- Your Existing BMI Calculation (UNCHANGED) ---
function calculateBMI() {
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("weight").value);
    const bmiResult = document.getElementById("bmiResult");

    if (!height || !weight || height <= 0 || weight <= 0) {
        bmiResult.innerText = "Please enter valid height and weight.";
        return;
    }

    const bmi = (weight / ((height / 100) ** 2)).toFixed(2);
    bmiResult.innerText = `Your BMI is ${bmi}`;
}

// --- Your Existing Recommendation Fetching (UNCHANGED) ---
async function getRecommendation() {
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const email = document.getElementById('email').value.trim();
    const occupation = document.getElementById("occupation").value;
    const diet = document.getElementById("dietPreference").value;
    const city = document.getElementById("citySelect").value;
    const allergies = document.getElementById("allergies").value;
    const recommendationOutput = document.getElementById("recommendationOutput");


    if (!age || !gender || !occupation || !diet || !city) {
        alert("Please complete all fields before requesting a recommendation.");
        return;
    }

    try {
        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                age: age,
                gender: gender,
                occupation: occupation,
                diet_preference: diet,
                city: city,
                allergies: allergies
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        let mealsHtml = '<h3>Breakfast Options:</h3><ul></ul><h3>Lunch Options:</h3><ul></ul><h3>Dinner Options:</h3><ul></ul>';
        if (data.meals) {
            mealsHtml = `
                <h3>Breakfast Options:</h3>
                <ul>${data.meals.breakfast ? data.meals.breakfast.map(meal => `<li>${meal}</li>`).join('') : ''}</ul>
                <h3>Lunch Options:</h3>
                <ul>${data.meals.lunch ? data.meals.lunch.map(meal => `<li>${meal}</li>`).join('') : ''}</ul>
                <h3>Dinner Options:</h3>
                <ul>${data.meals.dinner ? data.meals.dinner.map(meal => `<li>${meal}</li>`).join('') : ''}</ul>
            `;
        }

        let exercisesHtml = '<h3>Recommended Exercises:</h3><ul></ul>';
        if (data.exercises) {
            exercisesHtml = `
                <h3>Recommended Exercises:</h3>
                <ul>${data.exercises.map(exercise => `<li>${exercise}</li>`).join('')}</ul>
            `;
        }

        document.getElementById("recommendationOutput").innerHTML = mealsHtml + exercisesHtml;

    } catch (error) {
        console.error("Error fetching recommendations:", error);
        alert("Something went wrong while getting recommendations.");
        document.getElementById("recommendationOutput").innerHTML = `<p style="color: red;">Failed to get recommendations: ${error.message}</p>`;
    }
}

// --- Your Existing Smart Meal Fetching from Backend (UNCHANGED) ---
async function fetchSmartMealFromBackend() {
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const occupation = document.getElementById("occupation").value;
    const diet = document.getElementById("dietPreference").value;
    const city = document.getElementById("citySelect").value;
    const allergies = document.getElementById("allergies").value;

    // It's good to keep basic validation
    if (!age || !gender || !occupation || !diet || !city) {
        alert("Please complete your profile before getting a smart meal.");
        return;
    }

    try {
        // *** CHANGE 1: Call the correct endpoint and method ***
        // The /generate_smart_meal endpoint in your Flask app is a GET request
        // and does not require a request body for its current implementation.
        const response = await fetch("/generate_smart_meal", {
            method: "GET" // Changed method from POST to GET
            // Removed headers and body as they are not needed for a GET request to this specific endpoint
            // headers: { "Content-Type": "application/json" },
            // body: JSON.stringify({ /* ... profile data ... */ })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json(); // This 'data' will now contain { "breakfast": "...", "lunch": "...", "dinner": "..." }
        const smartMealDiv = document.querySelector("#smart-meal #smartMealOutput");

        // *** CHANGE 2: Update display logic to show all three meal types ***
        // Ensure the smartMealDiv exists before trying to update its innerHTML
        if (smartMealDiv) {
            if (data.breakfast || data.lunch || data.dinner) {
                let mealsHtml = '<h3>Your Smart Meal Plan:</h3>';
                if (data.breakfast) {
                    mealsHtml += `<p><strong>Breakfast:</strong> ${data.breakfast}</p>`;
                }
                if (data.lunch) {
                    mealsHtml += `<p><strong>Lunch:</strong> ${data.lunch}</p>`;
                }
                if (data.dinner) {
                    mealsHtml += `<p><strong>Dinner:</strong> ${data.dinner}</p>`;
                }
                smartMealDiv.innerHTML = mealsHtml;
            } else {
                smartMealDiv.innerHTML = `<p>No smart meal suggestion available.</p>`;
            }
        } else {
            console.error("Error: #smartMealOutput element not found in the DOM.");
            alert("An internal display error occurred. Please check console for details.");
        }


    } catch (error) {
        console.error("Smart Meal Fetch Error:", error);
        alert("Something went wrong while getting your Smart Meal.");
        const smartMealDiv = document.querySelector("#smart-meal #smartMealOutput");
        if (smartMealDiv) { // Ensure the div exists even in the error case
            smartMealDiv.innerHTML = `<p style="color: red;">Failed to get Smart Meal: ${error.message}</p>`;
        }
    }
}


// --- NEW: DOMContentLoaded and hashchange listeners ---
// These ensure the theme is applied on page load and back button visibility is correct
// when navigating via browser history or initial URL hashes.
document.addEventListener('DOMContentLoaded', () => {
    // 1. Apply saved theme on page load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') { // Check for 'dark' value, set your theme-dark class
        document.body.classList.add('theme-dark');
    }

    // 2. Handle initial back button visibility based on URL hash
    const currentHash = window.location.hash.substring(1); // Remove '#'

    // If a hash exists and it's not 'profile', show back buttons
    if (currentHash && currentHash !== 'profile' && document.getElementById(currentHash)) {
        toggleBackButtons(true);
        // Ensure the page scrolls to the correct section if loaded with a hash
        document.getElementById(currentHash).scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        // If no hash, or hash is 'profile', hide back buttons
        toggleBackButtons(false);
        // Ensure we are at the top of the profile section if no hash is present or it's 'profile'
        if (!currentHash || currentHash === 'profile') {
             document.getElementById('profile').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Set today's date for the calorie tracker
    document.getElementById('logDate').value = getTodayDate();
    loadDailyCalorieSummary(); // Load summary for today on page load
});

// In script.js

async function handleUserLogin() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    try {
        // 1. Send credentials to your Flask login route (/user/login)
        const response = await fetch('/user/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (response.ok) {
            // SUCCESS! The server has started a session.
            
            // Close the pop-up immediately to clear the screen
            closePopup(); 
            
            // 🚨 CRITICAL FIX: REDIRECT TO THE PROFILE PAGE 🚨
            // This forces the browser to load the /user/profile page, which runs 
            // the database fetch function (fetch_user_profile_by_email) and displays the data.
            window.location.href = '/user/profile'; 
            
        } else {
            // FAILURE: Server returns an error (invalid credentials)
            const errorData = await response.json();
            alert("Login Failed: " + (errorData.error || "Invalid email or password."));
        }

    } catch (error) {
        console.error("Login Fetch Error:", error);
        alert("An internal error occurred during login. Check server status and console for details.");
    }
}

// 3. Listen for hash changes (e.g., if user manually changes URL hash or uses browser back/forward)
window.addEventListener('hashchange', () => {
    const newHash = window.location.hash.substring(1);
    if (newHash && newHash !== 'profile') {
        toggleBackButtons(true);
    } else {
        toggleBackButtons(false);
    }
    // Ensure we scroll to the new hash target on hashchange
    const targetElement = document.getElementById(newHash);
    if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});