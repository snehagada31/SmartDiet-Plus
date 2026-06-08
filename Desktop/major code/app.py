from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint, session, redirect, url_for, g # ADDED 'g' for global context
import random
from db_insert import insert_user
from recipes_list import recipes_data
import json
import os
import datetime
import uuid
from user_routes import login_bp 
from werkzeug.security import generate_password_hash
from translations import LANGUAGES, TRANSLATIONS 
# ✨ NEW IMPORTS FOR FILE HANDLING ✨
from flask import send_from_directory
from werkzeug.utils import secure_filename 

# --- CRITICAL FIX: ADDING THE TRANSLATION LOOKUP FUNCTION ---
def translate_text(text, lang_code):
    """Looks up text in the imported TRANSLATIONS dictionary or returns original if no translation exists."""
    return TRANSLATIONS.get(text, {}).get(lang_code, text)

# --- START IMAGE RECOGNITION CONFIGURATION ---
UPLOAD_FOLDER = 'temp_uploads' # Temporary folder for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# --- END IMAGE RECOGNITION CONFIGURATION ---

app = Flask(__name__)
CORS(app)

# --- APPLY IMAGE CONFIGURATION TO APP ---
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ---

# <<< Set Secret Key for session management >>>
app.config['SECRET_KEY'] = 'A_VERY_STRONG_RANDOM_SECRET_KEY_FOR_SMARTDIET_PLUS' 

# NEW: Function to run before every request
@app.before_request
def before_request():
    # Set default language if none is in session
    if 'language' not in session:
        session['language'] = 'en'
    
    # Make the translation function and language code available globally in Jinja templates (g)
    g.lang_code = session['language']
    # g.translate now points to the function we defined above
    g.translate = lambda text: translate_text(text, g.lang_code)
    # Expose the imported LANGUAGES dictionary for template loops (e.g., in the translation popup)
    g.LANGUAGES = LANGUAGES


# Create a blueprint for recipe-related routes
recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

# --- FINAL BLUEPRINT REGISTRATION ---

# 1. Register the primary user blueprint
app.register_blueprint(login_bp) 

# ------------------------------------

# --- START MODIFIED SECTION: Data File Paths and Folder Creation ---
# Define the base directory of your application (where app.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the folder where your data files will be stored
DATA_FOLDER = os.path.join(BASE_DIR, 'data')

# Full paths to your JSON data files
FOOD_LOGS_FILE = os.path.join(DATA_FOLDER, 'food_logs.json')
USER_PROFILES_FILE = os.path.join(DATA_FOLDER, 'user_profiles.json')

# Important: Create the data folder if it doesn't exist
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"App: Created data directory at {DATA_FOLDER}")
# --- END MODIFIED SECTION ---

# --- IMAGE RECOGNITION HELPER FUNCTIONS ---

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- MOCK AI FUNCTION (Replace this later with real API calls) ---
def analyze_image_for_calories(filepath):
    # This simulates the result from an external AI service
    if 'chicken' in filepath.lower() or 'salad' in filepath.lower():
        return {'food': 'Chicken Salad Bowl', 'calories': 410, 'protein': 45, 'carbs': 15, 'fat': 20}
    elif 'oats' in filepath.lower() or 'breakfast' in filepath.lower():
        return {'food': 'Oatmeal with Berries', 'calories': 320, 'protein': 12, 'carbs': 55, 'fat': 5}
    else:
        # Generic fallback for unknown food
        return {'food': 'Unrecognized Meal', 'calories': 300, 'protein': 10, 'carbs': 30, 'fat': 10}
# -----------------------------------------------

# --- Helper functions for JSON file operations (Keep for existing routes) ---
def load_food_logs_data():
    os.makedirs(os.path.dirname(FOOD_LOGS_FILE), exist_ok=True)
    if not os.path.exists(FOOD_LOGS_FILE):
        with open(FOOD_LOGS_FILE, 'w') as f:
            json.dump({}, f, indent=4) 
        return {}
    with open(FOOD_LOGS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_food_logs_data(data):
    os.makedirs(os.path.dirname(FOOD_LOGS_FILE), exist_ok=True)
    with open(FOOD_LOGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_user_profiles_data():
    os.makedirs(os.path.dirname(USER_PROFILES_FILE), exist_ok=True)
    if not os.path.exists(USER_PROFILES_FILE):
        with open(USER_PROFILES_FILE, 'w') as f:
            json.dump({}, f, indent=4) 
        return {}
    with open(USER_PROFILES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_user_profiles_data(data):
    os.makedirs(os.path.dirname(USER_PROFILES_FILE), exist_ok=True)
    with open(USER_PROFILES_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# --- Core Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes_page():
    return render_template('recipes.html')

# ----------------------------------------------------
# ✨ LANGUAGE SWITCHING ROUTE ✨
@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    """Sets the user's language preference in the session and redirects back."""
    # Check if the requested language code is one we support (from your LANGUAGES dict)
    if lang_code in LANGUAGES:
        session['language'] = lang_code
    
    # Redirect the user back to the page they came from (or the homepage if no referrer)
    return redirect(request.referrer or url_for('index'))
# ----------------------------------------------------

# --- IMAGE RECOGNITION ROUTE ADDED HERE ---
@app.route('/upload_food_image', methods=['POST'])
def upload_food_image():
    user_id = session.get('email', 'demo_user') # Get user ID
    
    if 'food_image' not in request.files:
        return jsonify({'error': g.translate('No file part in the request.')}), 400
    
    file = request.files['food_image']
    original_filename = file.filename
    
    if file.filename == '':
        return jsonify({'error': g.translate('No selected file.')}), 400
        
    if file and allowed_file(file.filename):
        # 1. Save the file temporarily
        unique_filename = str(uuid.uuid4()) + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # 2. Analyze the image using the mock function
        analysis_result = analyze_image_for_calories(original_filename) 
            
        # 3. Clean up the temporary file (important for security/storage)
        os.remove(filepath) 
        
        # 4. Return results as JSON
        return jsonify({
            'message': g.translate('Analysis complete!'),
            'result': analysis_result,
            'log_prompt': g.translate('Click "Log Meal" to add this to your tracker.')
        })

    return jsonify({'error': g.translate('File type not allowed.')}), 400
# ------------------------------------------

# --- Recommendation Logic ---
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()

        age = data.get('age')
        gender = data.get('gender')
        occupation = data.get('occupation')
        diet_preference = data.get('diet_preference')
        city = data.get('city')
        allergies = data.get('allergies', '').lower()

        user_id = data.get('email', "demo_user_id") 
        all_user_profiles = load_user_profiles_data()
        user_profile = all_user_profiles.get(user_id, {})

        calorie_goal = data.get('calorie_goal', user_profile.get('calorie_goal', 2200))
        protein_goal = data.get('protein_goal', user_profile.get('protein_goal', 70))
        carbs_goal = data.get('carbs_goal', user_profile.get('carbs_goal', 250))
        fat_goal = data.get('fat_goal', user_profile.get('fat_goal', 60))

        if not all([age, gender, occupation, diet_preference, city]):
            return jsonify({"error": "Missing required data for recommendation (age, gender, occupation, diet_preference, city)."}), 400

        # --- Save/Update User Profile (simplified JSON handling) ---
        if user_id != "demo_user_id": 
            if age is not None: user_profile['age'] = age
            if gender is not None: user_profile['gender'] = gender
            if occupation is not None: user_profile['occupation'] = occupation
            if city is not None: user_profile['city'] = city
            if diet_preference is not None: user_profile['diet_preference'] = diet_preference
            if allergies is not None: user_profile['allergies'] = allergies
            
            if data.get('calorie_goal') is not None: user_profile['calorie_goal'] = float(data['calorie_goal'])
            if data.get('protein_goal') is not None: user_profile['protein_goal'] = float(data['protein_goal'])
            if data.get('carbs_goal') is not None: user_profile['carbs_goal'] = float(data['carbs_goal'])
            if data.get('fat_goal') is not None: user_profile['fat_goal'] = float(data['fat_goal'])

            all_user_profiles[user_id] = user_profile
            save_user_profiles_data(all_user_profiles)
        # --- End Save/Update User Profile ---

        recommendations = generate_recommendations(
            age, gender, occupation, diet_preference, city, allergies
        )

        return jsonify(recommendations)

    except Exception as e:
        print(f"Error in /recommend route: {e}")
        return jsonify({"error": f"Failed to process recommendation request: {str(e)}. Check if all required profile data (age, gender, occupation, diet, city) is sent from the frontend."}), 500


def generate_recommendations(age, gender, occupation, diet_preference, city, allergies):
    occupation = occupation.lower()

    if any(word in occupation for word in ['office', 'desk', 'manager', 'it', 'software', 'admin']):
        activity_level = 'low'
    elif any(word in occupation for word in ['construction', 'labor', 'manual', 'driver', 'farmer', 'delivery']):
        activity_level = 'high'
    else:
        activity_level = 'medium'

    meals = get_meals_based_on_activity(
        diet_preference, activity_level, allergies)
    exercises = get_exercises_based_on_activity_level(activity_level)

    return {
        'meals': meals,
        'exercises': exercises
    }


def get_meals_based_on_activity(diet_preference, activity_level, allergies):
    all_meals = {
        'low': {
            'breakfast': [
                'Oatmeal with fruits', 'Smoothie bowl', 'Boiled eggs with toast', 'Poha',
                'Fruit salad', 'Yogurt Parfait', 'Scrambled Eggs with Cheese', 'Quick Banana Pancakes'
            ],
            'lunch': [
                'Grilled paneer salad', 'Vegetable soup with bread', 'Mixed veg curry with roti',
                'Khichdi', 'Veg wrap', 'Simple Cheese Sandwich', 'Creamy Tomato Soup', 'Homemade Pizza Bagels'
            ],
            'dinner': [
                'Quinoa with veggies', 'Lentil soup', 'Tofu stir fry', 'Dalia khichdi',
                'Veg pulao', 'Classic Veggie Burger', 'Pasta with Marinara Sauce', 'Baked Sweet Potatoes with Toppings'
            ]
        },
        'medium': {
            'breakfast': [
                'Idli with chutney', 'Cornflakes with milk', 'Veg sandwich', 'Upma',
                'Besan chilla', 'French Toast with Berries', 'Fluffy Pancakes with Syrup', 'Breakfast Quesadilla'
            ],
            'lunch': [
                'Chole with roti', 'Dal tadka with rice', 'Pulao with curd', 'Bhindi sabzi with roti',
                'Vegetable korma', 'Chicken Caesar Salad', 'Cheesy Veggie Quesadillas', 'DIY Burrito Bowl'
            ],
            'dinner': [
                'Stuffed capsicum', 'Veg noodles', 'Rajma with brown rice', 'Kadhi chawal',
                'Spinach dal', 'Easy Chicken Stir-fry', 'Sheet Pan Sausage & Veggies', 'Hearty Lentil Shepherd\'s Pie'
            ]
        },
        'high': {
            'breakfast': [
                'Paratha with curd', 'Banana peanut butter sandwich', 'Omelette with toast',
                'Moong dal chilla', 'Paneer bhurji', 'High-Protein Breakfast Burrito', 'Greek Yogurt with Granola & Fruit'
            ],
            'lunch': [
                'Paneer curry with rice', 'Egg biryani', 'Mixed dal with jeera rice',
                'Chicken pulao', 'Soya chunk curry', 'Tuna Salad Sandwich', 'Spicy BBQ Chicken Wraps', 'Loaded Nachos'
            ],
            'dinner': [
                'Grilled chicken with veggies', 'Rajma chawal', 'Fish curry with rice',
                'Matar paneer with roti', 'Stuffed paratha with salad', 'One-Pan Salmon & Asparagus', 'Beef Chili with Cornbread', 'Classic Lasagna'
            ]
        }
    }

    def filter_allergies(meals_list):
        if allergies:
            user_allergies_list = [a.strip().lower() for a in allergies.split(',') if a.strip()]
            filtered = []
            for meal_name in meals_list:
                meal_name_lower = meal_name.lower()
                is_allergic = False
                for ua in user_allergies_list:
                    if ua in meal_name_lower:
                        is_allergic = True
                        break
                if not is_allergic:
                    filtered.append(meal_name)
            return filtered
        return meals_list

    selected_meals = {
        'breakfast': random.sample(filter_allergies(all_meals[activity_level]['breakfast']), k=min(len(filter_allergies(all_meals[activity_level]['breakfast'])), 6)),
        'lunch': random.sample(filter_allergies(all_meals[activity_level]['lunch']), k=min(len(filter_allergies(all_meals[activity_level]['lunch'])), 6)),
        'dinner': random.sample(filter_allergies(all_meals[activity_level]['dinner']), k=min(len(filter_allergies(all_meals[activity_level]['dinner'])), 6))
    }
    
    return selected_meals

def get_exercises_based_on_activity_level(activity_level):
    if activity_level == 'low':
        return ['Walking', 'Yoga', 'Light stretching']
    elif activity_level == 'high':
        return ['Running', 'Weight training', 'Cycling']
    else:
        return ['Jogging', 'Bodyweight exercises', 'Swimming']


@app.route('/submit_user', methods=['POST'])
def submit_user():
    try:
        data = request.get_json()
        if data:
            name = data.get('username')
            age = data.get('age')
            email = data.get('email')
            password = data.get('password') # Raw password from frontend
            
            gender = data.get('gender')
            occupation = data.get('occupation')
            diet_preference = data.get('diet_preference')
            city = data.get('city')
            allergies = data.get('allergies')
            notes = data.get('notes')

            # --- CRITICAL HASHING STEP ---
            if not password:
                return jsonify({"error": "Password is required for sign-up."}), 400
            
            # Hash the password before saving it
            # NOTE: Your actual user_routes.py now uses unsecured login (as requested)
            # You should decide whether to save hashed or plain text here for consistency.
            hashed_password = generate_password_hash(password)
            # ------------------------------

            # FIX: Pass the HASHED password (hashed_password) to insert_user
            insert_user(name, age, email, hashed_password, diet_preference, occupation, city, allergies, notes, gender)
            
            return jsonify({"message": "User data successfully saved!"}), 201
        else:
            return jsonify({"error": "No JSON data received."}), 400
    except Exception as e:
        print(f"Error in /submit_user route: {e}")
        return jsonify({"error": "Failed to save user data."}), 500

# --- Smart Meal Generator (Directly in app.py) ---
@app.route('/generate_smart_meal', methods=['GET'])
def generate_smart_meal():
    meals = {
        "breakfast": [
            "Oats with almond milk and fruits", "Avocado toast with boiled egg",
            "Smoothie bowl with granola", "Greek yogurt with honey and berries"
        ],
        "lunch": [
            "Grilled chicken with quinoa and veggies", "Paneer tikka wrap",
            "Mixed veggie stir-fry with brown rice", "Tofu salad with chickpeas and lemon dressing"
        ],
        "dinner": [
            "Lentil soup with whole grain toast", "Steamed fish with sautéed greens",
            "Veggie pasta with tomato basil sauce", "Chapati with dal and cucumber salad"
        ]
    }
    meal_plan = {
        "breakfast": random.choice(meals["breakfast"]),
        'lunch': random.choice(meals["lunch"]),
        'dinner': random.choice(meals["dinner"])
    }
    return jsonify(meal_plan)


# --- Recipe API Endpoints ---
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    diet_filters = request.args.getlist('diet')
    allergy_filters = request.args.getlist('allergy')

    print(f"\n--- API Call Received ---")
    print(f"Received Diet Filters: {diet_filters}")
    print(f"Received Allergy Filters: {allergy_filters}")

    filtered_recipes = []

    for recipe in recipes_data:
        should_include = True
        recipe_allergies_lower = [a.lower() for a in recipe.get('allergies', [])]

        if 'vegetarian' in diet_filters and 'non-vegetarian' in diet_filters:
            if allergy_filters:
                if any(selected_allergy.lower() in recipe_allergies_lower for selected_allergy in allergy_filters):
                    should_include = False
        else:
            if diet_filters:
                if not any(d.lower() in [s.lower() for s in recipe.get('diet', [])] for d in diet_filters):
                    should_include = False

            if allergy_filters:
                if any(selected_allergy.lower() in recipe_allergies_lower for selected_allergy in allergy_filters):
                    should_include = False

        print(f"Recipe '{recipe.get('title', 'N/A')}': should_include = {should_include}")
        if should_include:
            filtered_recipes.append(recipe)

    print(f"Final Filtered Recipes Count: {len(filtered_recipes)}")
    print(f"Final Filtered Recipes: {filtered_recipes}")
    print(f"--- End API Call ---")
    return jsonify(filtered_recipes)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe_detail(recipe_id):
    recipe = next((r for r in recipes_data if r['id'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({"message": "Recipe not found"}), 404

# --- Calorie Tracker Routes ---

@app.route('/log_food', methods=['POST'])
def log_food_entry():
    try:
        data = request.get_json()

        # IMPORTANT: In a real app, this should use `session['email']` after login!
        user_id = "demo_user_id" 

        food_item = data.get('food_item')
        calories = data.get('calories')
        protein = data.get('protein')
        carbs = data.get('carbs')
        fat = data.get('fat')
        meal_type = data.get('meal_type')
        log_date = data.get('log_date', datetime.date.today().strftime('%Y-%m-%d'))

        if not all([food_item, calories is not None, protein is not None, carbs is not None, fat is not None, meal_type, log_date]):
            return jsonify({"error": "Missing required food log fields (food_item, calories, protein, carbs, fat, meal_type, log_date)."}), 400

        try:
            calories = float(calories)
            protein = float(protein)
            carbs = float(carbs)
            fat = float(fat)
            if any(val < 0 for val in [calories, protein, carbs, fat]):
                return jsonify({"error": "Nutrient values cannot be negative"}), 400
        except ValueError:
            return jsonify({"error": "Nutrient values must be numbers"}), 400

        all_logs = load_food_logs_data()
        user_logs = all_logs.get(user_id, {})
        food_logs_for_date = user_logs.get(log_date, [])

        new_log = {
            "id": str(uuid.uuid4()), 
            "food_item": food_item,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "meal_type": meal_type,
            "timestamp": datetime.datetime.now().strftime('%H:%M:%S')
        }
        food_logs_for_date.append(new_log)

        all_logs[user_id] = user_logs
        save_food_logs_data(all_logs)

        return jsonify({"message": "Food logged successfully!", "log_id": new_log['id']}), 201

    except Exception as e:
        print(f"Error in /log_food: {e}")
        return jsonify({"error": "Failed to log food entry: {str(e)}"}), 500


@app.route('/get_daily_calorie_summary', methods=['GET'])
def get_daily_calorie_summary_route():
    try:
        user_id = request.args.get('user_id', "demo_user_id")
        log_date = request.args.get('log_date', datetime.date.today().strftime('%Y-%m-%d'))

        all_logs = load_food_logs_data()
        user_logs = all_logs.get(user_id, {})
        food_logs_for_date = user_logs.get(log_date, [])

        total_calories = sum(entry['calories'] for entry in food_logs_for_date)
        total_protein = sum(entry.get('protein', 0) for entry in food_logs_for_date)
        total_carbs = sum(entry.get('carbs', 0) for entry in food_logs_for_date)
        total_fat = sum(entry.get('fat', 0) for entry in food_logs_for_date)

        all_user_profiles = load_user_profiles_data()
        current_user_profile = all_user_profiles.get(user_id, {})
        calorie_goal = current_user_profile.get('calorie_goal', 2200)
        protein_goal = current_user_profile.get('protein_goal', 70)
        carbs_goal = current_user_profile.get('carbs_goal', 250)
        fat_goal = current_user_profile.get('fat_goal', 60)

        return jsonify({
            "date": log_date,
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fat": total_fat,
            "food_logs": food_logs_for_date,
            "goals": {
                "calorie": calorie_goal,
                "protein": protein_goal,
                "carbs": carbs_goal,
                "fat": fat_goal
            }
        }), 200

    except Exception as e:
        print(f"Error in /get_daily_calorie_summary route: {e}")
        return jsonify({"error": "Failed to retrieve daily summary: {str(e)}"}), 500

@app.route('/delete_food_log/<string:log_id>', methods=['DELETE'])
def delete_food_log_entry(log_id):
    try:
        user_id = request.args.get('user_id', "demo_user_id")

        all_logs = load_food_logs_data()
        user_logs = all_logs.get(user_id, {})

        found_and_deleted = False
        for date, logs_on_date in user_logs.items():
            initial_len = len(logs_on_date)
            user_logs[date] = [log for log in logs_on_date if log.get('id') != log_id]
            if len(user_logs[date]) < initial_len:
                found_and_deleted = True
                break

        if not found_and_deleted:
            return jsonify({"error": "Food log entry not found"}), 404

        all_logs[user_id] = user_logs 
        save_food_logs_data(all_logs) 

        return jsonify({"message": "Food log entry deleted successfully!"}), 200

    except Exception as e:
        print(f"Error deleting food log: {e}")
        return jsonify({"error": "Failed to delete food log entry: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)