// Get references to HTML elements
const recipeListContainer = document.getElementById('recipeList');
const applyFiltersBtn = document.getElementById('applyFiltersBtn');

// Modal elements
const recipeModal = document.getElementById('recipeModal');
const closeModalBtn = document.querySelector('.close-button');
const modalRecipeTitle = document.getElementById('modalRecipeTitle');
const modalRecipeImage = document.getElementById('modalRecipeImage');
const modalRecipeIngredients = document.getElementById('modalRecipeIngredients');
const modalRecipeInstructions = document.getElementById('modalRecipeInstructions');
const modalYoutubeLink = document.getElementById('modalYoutubeLink');

// Store all fetched recipes globally (or fetch by ID for details)
let allRecipes = [];

// --- Event Listeners ---
applyFiltersBtn.addEventListener('click', applyFilters);

recipeListContainer.addEventListener('click', (event) => {
    if (event.target.classList.contains('view-recipe')) {
        const recipeId = parseInt(event.target.dataset.recipeId);
        displayRecipeDetails(recipeId);
    }
});

closeModalBtn.addEventListener('click', () => {
    recipeModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target == recipeModal) {
        recipeModal.style.display = 'none';
    }
});


// --- Functions ---

// Fetches recipes from the backend based on filters
async function fetchRecipes(dietFilters = [], allergyFilters = []) {
    const dietParams = dietFilters.map(d => `diet=${encodeURIComponent(d)}`).join('&'); // Use encodeURIComponent
    const allergyParams = allergyFilters.map(a => `allergy=${encodeURIComponent(a)}`).join('&'); // Use encodeURIComponent

    let queryParams = '';
    if (dietParams && allergyParams) {
        queryParams = `${dietParams}&${allergyParams}`;
    } else if (dietParams) {
        queryParams = dietParams;
    } else if (allergyParams) {
        queryParams = allergyParams;
    }

    const url = `http://localhost:5000/api/recipes${queryParams ? '?' + queryParams : ''}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const recipes = await response.json();
        allRecipes = recipes;
        displayRecipes(recipes);
    } catch (error) {
        console.error("Could not fetch recipes:", error);
        recipeListContainer.innerHTML = '<p>Failed to load recipes.</p>';
    }
}

// Applies filters from the sidebar and triggers recipe fetch
function applyFilters() {
    const selectedDiet = Array.from(document.querySelectorAll('.recipe-sidebar input[name="diet"]:checked'))
        .map(checkbox => checkbox.value);

    const selectedAllergies = Array.from(document.querySelectorAll('.recipe-sidebar input[name="allergy"]:checked'))
        .map(checkbox => checkbox.value);

    fetchRecipes(selectedDiet, selectedAllergies);
}

// Displays recipes on the main page
function displayRecipes(recipes) {
    recipeListContainer.innerHTML = '';

    if (recipes.length === 0) {
        recipeListContainer.innerHTML = '<p>No recipes found matching your criteria.</p>';
        return;
    }

    recipes.forEach(recipe => {
        const recipeCard = document.createElement('div');
        recipeCard.classList.add('recipe-card');
        recipeCard.innerHTML = `
            <img src="${recipe.image}" alt="${recipe.title}">
            <h3>${recipe.title}</h3>
            <p>Diet: ${recipe.diet.join(', ')}</p>
            <p>Allergies: ${recipe.allergies.length > 0 ? recipe.allergies.join(', ') : 'None'}</p>
            ${recipe.youtube_link ? `<a href="${recipe.youtube_link}" target="_blank">Watch on YouTube</a>` : ''}
            <button class="view-recipe" data-recipe-id="${recipe.id}">View Recipe</button>
        `;
        recipeListContainer.appendChild(recipeCard);
    });
}

// Displays recipe details in the modal
function displayRecipeDetails(recipeId) {
    const recipe = allRecipes.find(r => r.id === recipeId);

    if (recipe) {
        modalRecipeTitle.textContent = recipe.title;
        modalRecipeImage.src = recipe.image;
        modalRecipeImage.alt = recipe.title;

        modalRecipeIngredients.innerHTML = '';
        modalRecipeInstructions.innerHTML = '';
        modalYoutubeLink.innerHTML = '';

        recipe.ingredients.forEach(ingredient => {
            const li = document.createElement('li');
            li.textContent = ingredient;
            modalRecipeIngredients.appendChild(li);
        });

        recipe.instructions.forEach(instruction => {
            const li = document.createElement('li');
            li.textContent = instruction;
            modalRecipeInstructions.appendChild(li);
        });

        if (recipe.youtube_link) {
            const youtubeLink = document.createElement('a');
            youtubeLink.href = recipe.youtube_link;
            youtubeLink.target = "_blank";
            youtubeLink.textContent = "Watch on YouTube";
            modalYoutubeLink.appendChild(youtubeLink);
        }

        recipeModal.style.display = 'flex';
    } else {
        console.error("Recipe not found in allRecipes for ID:", recipeId);
    }
}

// MODIFIED INITIAL LOAD LOGIC
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const dietParam = urlParams.getAll('diet'); // Can be multiple if checkboxes allow
    const allergyParam = urlParams.getAll('allergy'); // Can be multiple

    // If parameters are present in the URL, use them for the initial fetch
    if (dietParam.length > 0 || allergyParam.length > 0) {
        fetchRecipes(dietParam, allergyParam);

        // Optional: Pre-select sidebar checkboxes based on URL params for user feedback
        dietParam.forEach(d => {
            const checkbox = document.querySelector(`.recipe-sidebar input[name="diet"][value="${d}"]`);
            if (checkbox) checkbox.checked = true;
        });
        allergyParam.forEach(a => {
            const checkbox = document.querySelector(`.recipe-sidebar input[name="allergy"][value="${a}"]`);
            if (checkbox) checkbox.checked = true;
        });

    } else {
        // Otherwise, fetch all recipes (default behavior)
        fetchRecipes();
    }

    


});

