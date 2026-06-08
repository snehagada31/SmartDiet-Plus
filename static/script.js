// script.js

// --- Global DOM Elements (find them once when the script loads) ---
const allBackButtons = document.querySelectorAll('.back-button');

// ================= GLOBAL STATE DECLARATIONS (FIXED) =================
// Calorie Tracker State
let calorieData = {
    total: 0,
    goal: 2200,
    meals: { breakfast: 0, lunch: 0, dinner: 0, snacks: 0 },
    weekly: [0, 0, 0, 0, 0, 0, 0]
};
let calorieChart; // Chart instance for calorie tracker

// Gamification State
let userPoints = 0;
let weeklyProgress = [0, 0, 0, 0, 0, 0, 0]; // Tracks points per day (Sun to Sat)
let progressChart; // Chart instance for gamification


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

// 🚨 MODIFIED: Main Navigation Function (Now initializes charts)
function showContent(sectionId) {
    const targetElement = document.getElementById(sectionId);

    // Logic to hide all content sections and show the target section
    document.querySelectorAll('main section').forEach(section => {
        section.style.display = 'none';
    });
    if (targetElement) {
        targetElement.style.display = 'block';
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, '', `#${sectionId}`);
    }

    // 🚨 CHART INITIALIZATION LOGIC
    if (sectionId === 'progress') {
        // Initialize Gamification Chart when the Progress tab is opened
        if (typeof updateGamificationChart === 'function') {
            updateGamificationChart();
        }
    } else if (sectionId === 'tracker') {
        // Initialize Calorie Chart when the Tracker tab is opened
        if (typeof updateWeeklyChart === 'function') {
            updateWeeklyChart();
        }
    }
    // END CHART INITIALIZATION LOGIC

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

// ================= NEW: TAB NAVIGATION LOGIC =================
document.querySelectorAll(".tab-link").forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        // Remove 'active' from all links and content
        document.querySelectorAll(".tab-link").forEach(l => l.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(tab => tab.classList.remove("active"));

        // Add 'active' to the clicked link and its target content
        link.classList.add("active");
        document.getElementById(link.dataset.tab).classList.add("active");
    });
});

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


// ================= NEW: SIMPLE CALORIE TRACKER FUNCTIONS =================
function trackCalories() {
    const calorieInput = parseInt(document.getElementById("calories").value);
    const calorieProgress = document.getElementById("calorieProgress");
    const calorieStatus = document.getElementById("calorieStatus");

    if (!calorieInput || isNaN(calorieInput)) {
        alert("Please enter a valid calorie amount.");
        return;
    }

    const mealType = prompt("Which meal? (breakfast / lunch / dinner / snacks)").toLowerCase();
    if (!["breakfast", "lunch", "dinner", "snacks"].includes(mealType)) {
        alert("Invalid meal type. Please enter breakfast, lunch, dinner, or snacks.");
        return;
    }

    calorieData.total += calorieInput;
    calorieData.meals[mealType] += calorieInput;

    calorieProgress.value = calorieData.total;
    calorieStatus.innerText = `${calorieData.total} / ${calorieData.goal} kcal consumed`;

    document.getElementById("breakfastCalories").innerText = `${calorieData.meals.breakfast} kcal`;
    document.getElementById("lunchCalories").innerText = `${calorieData.meals.lunch} kcal`;
    document.getElementById("dinnerCalories").innerText = `${calorieData.meals.dinner} kcal`;
    document.getElementById("snackCalories").innerText = `${calorieData.meals.snacks} kcal`;

    calorieData.weekly[new Date().getDay()] = calorieData.total;
    updateWeeklyChart();
}

function resetCalorieTracker() {
    calorieData.total = 0;
    calorieData.meals = { breakfast: 0, lunch: 0, dinner: 0, snacks: 0 };
    document.getElementById("calorieProgress").value = 0;
    document.getElementById("calorieStatus").innerText = `0 / ${calorieData.goal} kcal consumed`;
    document.getElementById("breakfastCalories").innerText = "0 kcal";
    document.getElementById("lunchCalories").innerText = "0 kcal";
    document.getElementById("dinnerCalories").innerText = "0 kcal";
    document.getElementById("snackCalories").innerText = "0 kcal";
}

function updateWeeklyChart() {
    const ctx = document.getElementById("weeklyCalorieChart").getContext("2d");
    if (calorieChart) calorieChart.destroy();
    // IMPORTANT: This requires the Chart.js library to be loaded in your HTML
    calorieChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            datasets: [{
                label: "Calories Consumed",
                data: calorieData.weekly,
                backgroundColor: "rgba(76, 175, 80, 0.7)"
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}
// ================= END SIMPLE CALORIE TRACKER =================


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

// ================= NEW: SMART GROCERY LIST GENERATION =================
function generateGroceryList(meals) {
    const groceryCategories = { Vegetables: new Set(), Fruits: new Set(), Grains: new Set(), Proteins: new Set() };
    const mealToIngredients = {
        "Oatmeal Pancakes": ["Oats", "Milk", "Eggs", "Banana"], "Fruit Salad": ["Apple", "Banana", "Orange", "Grapes"],
        "Egg Sandwich": ["Eggs", "Bread", "Lettuce", "Tomato"], "Smoothie Bowl": ["Banana", "Berries", "Oats", "Milk"],
        "Yogurt Parfait": ["Yogurt", "Granola", "Strawberries"], "Veggie Stir Fry": ["Broccoli", "Carrots", "Bell Pepper", "Soy Sauce", "Garlic"],
        "Grilled Chicken Salad": ["Chicken", "Lettuce", "Tomato", "Cucumber"], "Paneer Wrap": ["Paneer", "Tortilla", "Lettuce", "Tomato"],
        "Quinoa Bowl": ["Quinoa", "Spinach", "Chickpeas", "Tomato"], "Dal with Rice": ["Lentils", "Rice", "Onion", "Tomato"],
        "Grilled Fish": ["Fish", "Lemon", "Garlic", "Olive Oil"], "Veggie Soup": ["Carrots", "Beans", "Tomato", "Onion"],
        "Chickpea Curry": ["Chickpeas", "Tomato", "Onion", "Spices"], "Stuffed Bell Peppers": ["Bell Pepper", "Rice", "Beans", "Corn"],
        "Vegetable Pasta": ["Pasta", "Tomato", "Zucchini", "Bell Pepper"]
    };
    const ingredientCategory = {
        Vegetables: ["Broccoli", "Carrots", "Bell Pepper", "Lettuce", "Spinach", "Tomato", "Cucumber", "Beans", "Zucchini", "Corn", "Onion", "Garlic"],
        Fruits: ["Apple", "Banana", "Orange", "Grapes", "Berries", "Strawberries", "Lemon"],
        Grains: ["Oats", "Bread", "Granola", "Quinoa", "Rice", "Pasta", "Tortilla"],
        Proteins: ["Eggs", "Milk", "Yogurt", "Chicken", "Paneer", "Chickpeas", "Fish", "Lentils"]
    };

    Object.values(meals).flat().forEach(meal => {
        // Ensure 'meal' is a string before looking up ingredients
        const ingredients = mealToIngredients[meal] || [];
        ingredients.forEach(ingredient => {
            for (const category in ingredientCategory) {
                if (ingredientCategory[category].includes(ingredient)) groceryCategories[category].add(ingredient);
            }
        });
    });

    const groceryDiv = document.getElementById("groceryOutput");
    // Ensure the output div exists before updating
    if (groceryDiv) {
        groceryDiv.innerHTML = `<h3>Weekly Smart Grocery List</h3>` +
            Object.entries(groceryCategories).map(([cat, items]) => items.size === 0 ? '' : `<h4>${cat}</h4><ul>${Array.from(items).map(i => `<li>${i}</li>`).join('')}</ul>`).join('');
    } else {
        console.warn("groceryOutput div not found in DOM.");
    }
}
// ================= END SMART GROCERY LIST GENERATION =================


// --- MODIFIED: Recommendation Fetching (now calls generateGroceryList) ---
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
                <ul>${data.meals.breakfast ? data.meals.breakfast.map(meal => `<li>${meal} <button onclick="showRecipe('${meal}')">Show Recipe</button></li>`).join('') : ''}</ul>
                <h3>Lunch Options:</h3>
                <ul>${data.meals.lunch ? data.meals.lunch.map(meal => `<li>${meal} <button onclick="showRecipe('${meal}')">Show Recipe</button></li>`).join('') : ''}</ul>
                <h3>Dinner Options:</h3>
                <ul>${data.meals.dinner ? data.meals.dinner.map(meal => `<li>${meal} <button onclick="showRecipe('${meal}')">Show Recipe</button></li>`).join('') : ''}</ul>
            `;
            // 🚨 INTEGRATION: Call new function to generate grocery list
            generateGroceryList(data.meals);
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

async function showRecipe(recipeName) {
    try {
        const response = await fetch("/recipe", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ recipe_name: recipeName })
        });
        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        const recipeDiv = document.getElementById("recipeOutput");
        recipeDiv.innerHTML = `
            <h3>${recipeName}</h3>
            <strong>Ingredients:</strong>
            <ul>${data.ingredients.map(i => `<li>${i}</li>`).join('')}</ul>
            <strong>Cooking Steps:</strong>
            <ol>${data.steps.map(s => `<li>${s}</li>`).join('')}</ol>
            <strong>Nutrition:</strong>
            <ul>
                <li>Calories: ${data.nutrition.calories}</li>
                <li>Protein: ${data.nutrition.protein}g</li>
                <li>Carbs: ${data.nutrition.carbs}g</li>
                <li>Fat: ${data.nutrition.fat}g</li>
                <li>Fiber: ${data.nutrition.fiber}g</li>
            </ul>
            ${data.video ? `<a href="${data.video}" target="_blank">Watch Cooking Video</a>` : ''}
            <strong>Substitutes:</strong>
            <ul>${Object.entries(data.substitutes).map(([key, vals]) => `<li>${key}: ${vals.join(", ")}</li>`).join('')}</ul>`;
        openPopup('recipePopup');
    } catch (error) {
        console.error("Error fetching recipe:", error);
        alert("Something went wrong while fetching recipe.");
    }
}
    // It's crucial that your HTML button has the ID 'get-smart-meal-btn'

// 🚨 NEW: GAMIFICATION CHART FUNCTION (ADDED FOR WEEKLY PROGRESS)
function updateGamificationChart() {
    const ctx = document.getElementById("progressChart");

    // Safety check to ensure the canvas exists and Chart is loaded
    if (!ctx || typeof Chart === 'undefined') {
        console.warn("Progress chart element or Chart.js library not found.");
        return;
    }

    // Destroy any existing chart instance tied to the global variable
    if (progressChart) {
        progressChart.destroy();
    }

    // Initialize the new chart using the Chart.js library
    progressChart = new Chart(ctx.getContext("2d"), {
        type: "bar",
        data: {
            labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            datasets: [{
                label: "Points Earned",
                data: weeklyProgress,
                backgroundColor: "rgba(76, 175, 80, 0.7)"
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: 50 // Ensures the initial blank chart has a clear scale
                }
            },
            animation: false
        }
    });
}


    // Event listener for the "Get Smart Meal Suggestion" 
// REPLACE your current fetchSmartMealFromBackend function with this code.
async function fetchSmartMealFromBackend() {
    // Collect all profile data from the form
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const occupation = document.getElementById("occupation").value;
    const diet = document.getElementById("dietPreference").value;
    const city = document.getElementById("citySelect").value;
    const allergies = document.getElementById("allergies") ? document.getElementById("allergies").value : 'none';
    const health_conditions = document.getElementById("healthConditions") ? document.getElementById("healthConditions").value : 'none';

    if (!age || !gender || !occupation || !diet || !city ) {
        alert("Please complete your profile before getting a smart meal.");
        return;
    }

    // 1. Prepare the data payload for the backend (Python's request.get_json())
    const userData = {
        age: parseInt(age),
        gender: gender,
        diet_preference: diet, // Matches the key in your Python's data.get()
        allergies: allergies,
        health_conditions: health_conditions,
    };

    try {
        const response = await fetch("/generate_smart_meal", {
            method: "POST", 
            
            // 🚨 FIX 1: Tell Flask we are sending JSON
            headers: {
                'Content-Type': 'application/json' 
            },
            
            // 🚨 FIX 2: Send the collected user data to the backend
            body: JSON.stringify(userData) 
        });

        if (!response.ok) {
            // Include server response text for better debugging if available
            const errorText = await response.text(); 
            throw new Error(`HTTP error! status: ${response.status}. Server message: ${errorText.substring(0, 100)}`);
        }

        const data = await response.json();
        const smartMealDiv = document.querySelector("#smart-meal #smartMealOutput");
        
        // --- DATA EXTRACTION ---
        const mealOptions = data;
        const mealTypes = ['breakfast', 'lunch', 'dinner'];
        const groceryList = data.grocery_list; 
        const hasMeals = mealTypes.some(type => mealOptions[type] && mealOptions[type].length > 0);

        if (smartMealDiv) {
            if (hasMeals) {
                let mealsHtml = '<h3>Your Smart Meal Plan:</h3>';
                
                mealTypes.forEach(type => {
                    if (mealOptions[type] && mealOptions[type].length > 0) {
                        const meal = mealOptions[type][0]; 
                        
                        if (meal && meal.name) {
                            mealsHtml += `
                                <p><strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> 
                                ${meal.name} 
                                <button onclick="showRecipe('${meal.name}')">Show Recipe</button></p>
                            `;
                        }
                    }
                });

                smartMealDiv.innerHTML = mealsHtml;

                // Call the grocery list display function
                generateGroceryList(groceryList); 

            } else {
                smartMealDiv.innerHTML = `<p>No smart meal suggestion available based on your profile. Try adjusting your preferences.</p>`;
                generateGroceryList([]); // Clear old grocery list
            }
        } else {
            console.error("Error: #smartMealOutput element not found in the DOM.");
            alert("An internal display error occurred. Please check console for details.");
        }

    } catch (error) {
        console.error("Smart Meal Fetch Error:", error);
        alert("Something went wrong while getting your Smart Meal.");
        const smartMealDiv = document.querySelector("#smart-meal #smartMealOutput");
        if (smartMealDiv) { 
            smartMealDiv.innerHTML = `<p style="color: red;">Failed to get Smart Meal: ${error.message}</p>`;
        }
    }
}

// Your existing generateGroceryList function is correct and does NOT need changes.

// 🚨 NEW: GAMIFICATION CHART FUNCTION (ADDED FOR WEEKLY PROGRESS)
function updateGamificationChart() {
    const ctx = document.getElementById("progressChart");

    // Safety check to ensure the canvas exists and Chart is loaded
    if (!ctx || typeof Chart === 'undefined') {
        console.warn("Progress chart element or Chart.js library not found.");
        return;
    }

    // Destroy any existing chart instance tied to the global variable
    if (progressChart) {
        progressChart.destroy();
    }

    // Initialize the new chart using the Chart.js library
    progressChart = new Chart(ctx.getContext("2d"), {
        type: "bar",
        data: {
            labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            datasets: [{
                label: "Points Earned",
                data: weeklyProgress,
                backgroundColor: "rgba(76, 175, 80, 0.7)"
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: 50 // Ensures the initial blank chart has a clear scale
                }
            },
            animation: false
        }
    });
}


// ================= NEW: GAMIFICATION LOGIC (MODIFIED) =================
function completeTask() {
    userPoints += 10;
    document.getElementById("points").innerText = userPoints;

    let badge = "Beginner";
    if (userPoints >= 50 && userPoints < 100) badge = "Intermediate";
    else if (userPoints >= 100) badge = "Pro";

    document.getElementById("badge").innerText = badge;

    // 🚨 CRITICAL FIX: Update weeklyProgress and draw chart
    const today = new Date().getDay(); // 0 = Sunday
    weeklyProgress[today] += 10;
    updateGamificationChart(); // Call the newly defined chart function
}
// ================= END GAMIFICATION LOGIC =================


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
                "Content-Type": "application/json"
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
    // --- In script.js: Add this block to your file ---

    let reminderSchedule = []; 
let notificationSentToday = {}; 

// --- Helpers and Checker Functions ---

function convertTo24Hour(time12h) {
    if (!time12h) return null;
    const parts = time12h.toUpperCase().split(' ');
    const time = parts[0];
    const modifier = parts.length > 1 ? parts[1] : '';
    
    let [hours, minutes] = time.split(':');
    
    if (hours === '12' && modifier === 'AM') {
        hours = '00';
    } else if (modifier === 'PM' && hours !== '12') {
        hours = parseInt(hours, 10) + 12;
    }
    return `${String(hours).padStart(2, '0')}:${minutes}`;
}

function showWaterReminder(time) {
    if (Notification.permission === "granted") {
        new Notification("💧 SmartDiet+ Reminder", {
            body: `It's ${time}. Time to hydrate!`,
            icon: '/path/to/water_icon.png' 
        });
    } else {
        alert(`💧 Time to drink water! It's ${time}.`); 
        if (Notification.permission !== "denied") {
            Notification.requestPermission();
        }
    }
}

function checkReminderTime() {
    const now = new Date();
    const currentTime = now.toTimeString().substring(0, 5); 
    const todayKey = now.toDateString(); 

    if (!notificationSentToday[todayKey]) {
        notificationSentToday = {};
        notificationSentToday[todayKey] = {};
    }

    if (reminderSchedule.includes(currentTime)) {
        if (!notificationSentToday[todayKey][currentTime]) {
            showWaterReminder(currentTime); 
            notificationSentToday[todayKey][currentTime] = true; 
        }
    }
}

function startReminderChecker() {
    if (window.reminderInterval) {
        clearInterval(window.reminderInterval); 
    }
    window.reminderInterval = setInterval(checkReminderTime, 20000); // Check every 20 seconds
}

// ----------------------------------------------------------------------------------
// --- NEW EDITING/MODAL CONTROL FUNCTIONS ---
// ----------------------------------------------------------------------------------

// Function called by the 'Edit/View Schedule →' link
function openSimpleReminderPopup() {
    toggleReminderModal(true);
}

function toggleReminderModal(show) {
    const popup = document.getElementById('simpleReminderPopup');
    const input = document.getElementById('reminderScheduleInput');
    const timesContainer = document.getElementById('displayReminderTimesContainer');
    
    if (popup) {
        if (show) {
            popup.style.display = 'block';

            // Load the current schedule times into the input field for editing
            if (input && timesContainer) {
                // Collect the text from the current time tags
                const currentTimes = Array.from(timesContainer.querySelectorAll('.time-tag')).map(tag => tag.textContent).join(', ');
                
                input.value = currentTimes;
            }
        } else {
            popup.style.display = 'none';
        }
    }
}

// Function called by the 'Save Schedule' button in the modal
async function saveWaterRemindersAndClosePopup() {
    // 1. Call the saving function
    const success = await saveWaterReminders(); 
    
    // 2. Close the popup only if the save was successful
    if (success) {
        toggleReminderModal(false);
    }
}

// --- FUNCTION TO SAVE/EDIT REMINDERS (Connect this to your 'Save' button) ---
async function saveWaterReminders() {
    const inputElement = document.getElementById('reminderScheduleInput'); 
    
    if (!inputElement) {
        alert("Error: Cannot find the input field for saving the schedule.");
        return false;
    }
    
    const newTimesString = inputElement.value;
    const timesArray = newTimesString.split(',').map(t => t.trim()).filter(t => t.length > 0);
    
    const dataToSend = {
        water_status: timesArray.length > 0 ? 'Active' : 'Inactive',
        water_times: newTimesString 
    };
    
    try {
        const response = await fetch("/user/update_reminders", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dataToSend)
        });

        if (response.ok) {
            alert("Reminder schedule saved successfully!");
            // 2. Reload to update the display and activate the checker
            loadWaterReminders(); 
            return true;
        } else {
            alert(`Failed to save schedule. Status: ${response.status}`);
            return false;
        }
    } catch (error) {
        console.error("Save Reminder Error:", error);
        alert("A network error occurred while saving the schedule.");
        return false;
    }
}


// --- FUNCTION TO LOAD AND DISPLAY DATA (Runs when the page loads) ---
async function loadWaterReminders() {
    try {
        const response = await fetch("/user/get_reminders");
        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }
        
        const data = await response.json(); 
        const timesString = data.water_times || ''; 
        
        // 1. Prepare data for the timer
        if (timesString) {
             const timesArray12h = timesString.split(',').map(t => t.trim());
             reminderSchedule = timesArray12h.map(convertTo24Hour).filter(t => t !== null);
        } else {
             reminderSchedule = [];
        }
        
        const totalCount = reminderSchedule.length;

        // 2. Update the HTML elements using your exact structure
        
        const totalCountElement = document.getElementById('displayReminderCount'); 
        const timesContainer = document.getElementById('displayReminderTimesContainer'); 
        const noTimesMessage = document.getElementById('noTimesMessage'); 
        
        // Update the Total Count (0, 1, 2, etc.)
        if (totalCountElement) {
             totalCountElement.textContent = totalCount; 
        }
        
        // Update the Active Times section (time tags)
        if (timesContainer && noTimesMessage) {
            // Clear all existing time tags before rendering new ones
            Array.from(timesContainer.querySelectorAll('.time-tag')).forEach(tag => tag.remove());

            if (timesString && totalCount > 0) {
                const timesArray = timesString.split(',').map(t => t.trim()).filter(t => t.length > 0);
                
                // Hide the "Tap Edit" message
                noTimesMessage.style.display = 'none';

                // Add new time tags
                timesArray.forEach(time => {
                    const span = document.createElement('span');
                    span.className = 'time-tag'; // Use the appropriate class for styling
                    span.textContent = time;
                    // Insert the new tag before the "noTimesMessage" element
                    timesContainer.insertBefore(span, noTimesMessage); 
                });
            } else {
                // Show the "Tap Edit" message if the schedule is empty
                noTimesMessage.style.display = 'inline';
            }
        }

        // 3. Start the continuous checker
        if (totalCount > 0) {
            startReminderChecker();
        }

    } catch (error) {
        console.error("Error loading water reminders:", error);
    }
}

// 4. Initialize on page load
loadWaterReminders();

});