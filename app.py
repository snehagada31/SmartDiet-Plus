from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint, session, redirect, url_for, g
import random
from db_insert import insert_user
from recipes_list import recipes_data
import json
import os
import datetime
import uuid
from user_routes import login_bp 
from werkzeug.security import generate_password_hash
# Imports for File Handling and Mock AI
from flask import send_from_directory
from werkzeug.utils import secure_filename 
from translations import LANGUAGES, TRANSLATIONS 
from google import genai
from google.genai import types 

# ----------------------------------------------------
# RECIPE DATA AND TRANSLATION CORE
# ----------------------------------------------------

# ========================= RECIPE DATA (Used by the /recipe endpoint) ========================# ========================= RECIPE DATA (Used by the /recipe endpoint) =========================
# 🚨 YOU MUST ADD ALL RECIPES HERE (e.g., "Fluffy Pancakes with Syrup") 🚨
recipes_basic_data = {
    "Oatmeal Pancakes": {
        "ingredients": ["Oats", "Milk", "Eggs", "Banana"],
        "steps": ["Mix oats and milk.", "Add banana and eggs.", "Cook."],
        "nutrition": {"calories": 250, "protein": 8, "carbs": 45, "fat": 6, "fiber": 5},
        "video": "https://youtu.be/wx4UGGpbOgI?si=DZZGCnEeclKncZkg",
        "substitutes": {"Milk": ["Almond milk", "Soy milk"], "Eggs": ["Chia seeds"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk", "eggs"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Veggie Stir Fry": {
        "ingredients": ["Broccoli", "Carrots", "Bell Pepper", "Soy Sauce", "Garlic"],
        "steps": ["Heat oil, saute garlic.", "Add veggies, stir-fry.", "Add soy sauce."],
        "nutrition": {"calories": 180, "protein": 6, "carbs": 30, "fat": 5, "fiber": 8},
        "video": "https://youtu.be/spDs_wzn8To?si=0jVHEeBTxfZ47IQj",
        "substitutes": {"Broccoli": ["Cauliflower"], "Soy Sauce": ["Tamari"]},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": ["soy", "garlic"],
        "health_conditions": ["high-bp"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Fluffy Pancakes with Syrup": {
        "ingredients": ["All-purpose flour", "Milk", "Egg", "Baking powder", "Sugar", "Maple Syrup"],
        "steps": ["Whisk dry ingredients.", "Mix wet ingredients.", "Combine and cook. Serve with syrup."],
        "nutrition": {"calories": 300, "protein": 10, "carbs": 50, "fat": 8, "fiber": 2},
        "video": "https://www.youtube.com/watch?v=some_pancake_video_link",
        "substitutes": {"Milk": ["Buttermilk"], "Sugar": ["Honey"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk", "eggs", "gluten"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s"] # Added "30s"
    },
    "Veg sandwich": {
        "ingredients": ["Bread", "Cucumber", "Tomato", "Onion", "Green Chutney", "Butter"],
        "steps": ["Toast bread, spread chutney.", "Layer fresh veggies.", "Serve."],
        "nutrition": {"calories": 250, "protein": 8, "carbs": 30, "fat": 10},
        "video": "https://www.youtube.com/watch?v=some_sandwich_video_link",
        "substitutes": {"Bread": ["Brown bread", "Gluten-free bread"]},
        "diet_type": ["vegetarian"],
        "allergens": ["gluten", "onion", "milk"],
        "health_conditions": ["high-bp"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Cornflakes with milk": {
        "ingredients": ["Cornflakes", "Milk", "Sugar"],
        "steps": ["Pour cornflakes in a bowl.", "Add milk and sugar to taste."],
        "nutrition": {"calories": 200, "protein": 5, "carbs": 40, "fat": 3},
        "video": "https://www.youtube.com/watch?v=some_cornflakes_video_link",
        "substitutes": {"Milk": ["Almond milk", "Soy milk"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk"],
        "health_conditions": ["high-bp"],
        "age_groups": ["under-30", "30s", "40-plus"] # Added "30s"
    },
    "Idli with chutney": {
        "ingredients": ["Idli batter", "Water", "Salt", "Coconut", "Dals", "Chilies"],
        "steps": ["Steam idlis.", "Grind coconut, dals, chilies for chutney."],
        "nutrition": {"calories": 180, "protein": 5, "carbs": 35, "fat": 2},
        "video": "https://www.youtube.com/watch?v=some_idli_video_link",
        "substitutes": {},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": [],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Besan chilla": {
        "ingredients": ["Besan (chickpea flour)", "Water", "Onion", "Green chili", "Coriander"],
        "steps": ["Mix besan with water and spices to make batter.", "Cook like a pancake."],
        "nutrition": {"calories": 220, "protein": 10, "carbs": 30, "fat": 7},
        "video": "https://www.youtube.com/watch?v=some_chilla_video_link",
        "substitutes": {},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": ["onion"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "French Toast with Berries": {
        "ingredients": ["Bread", "Eggs", "Milk", "Cinnamon", "Berries", "Maple Syrup"],
        "steps": ["Dip bread in egg-milk mixture.", "Cook until golden.", "Top with berries and syrup."],
        "nutrition": {"calories": 350, "protein": 12, "carbs": 45, "fat": 15},
        "video": "https://www.youtube.com/watch?v=some_frenchtoast_video_link",
        "substitutes": {"Milk": ["Almond milk"], "Bread": ["Whole wheat bread"]},
        "diet_type": ["vegetarian"],
        "allergens": ["gluten", "eggs", "milk"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s"] # Added "30s"
    },
    "Pulao with curd": {
        "ingredients": ["Rice", "Mixed Vegetables", "Spices", "Curd"],
        "steps": ["Cook rice with vegetables and spices to make pulao.", "Serve with curd."],
        "nutrition": {"calories": 380, "protein": 10, "carbs": 60, "fat": 10},
        "video": "https://www.youtube.com/watch?v=some_pulao_video_link",
        "substitutes": {"Rice": ["Brown rice"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk"],
        "health_conditions": ["high-bp"],
        "age_groups": ["under-30", "30s", "40-plus"] # Added "30s"
    },
    "Smoothie bowl with granola": {
        "ingredients": ["Frozen fruit", "Yogurt", "Granola", "Seeds"],
        "steps": ["Blend fruit and yogurt.", "Top with granola and seeds."],
        "nutrition": {"calories": 350, "protein": 15, "carbs": 55, "fat": 8},
        "video": "https://www.youtube.com/watch?v=some_smoothiebowl_video_link",
        "substitutes": {"Yogurt": ["Plant-based yogurt"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk"],
        "health_conditions": ["pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Grilled chicken with quinoa and veggies": {
        "ingredients": ["Chicken breast", "Quinoa", "Broccoli", "Bell pepper", "Olive oil", "Herbs"],
        "steps": ["Grill chicken.", "Cook quinoa.", "Roast vegetables and combine."],
        "nutrition": {"calories": 450, "protein": 40, "carbs": 35, "fat": 15},
        "video": "https://www.youtube.com/watch?v=some_grilledchicken_video_link",
        "substitutes": {"Chicken": ["Tofu", "Paneer"]},
        "diet_type": ["non-vegetarian", "gluten-free"],
        "allergens": [],
        "health_conditions": ["high-bp", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Veggie pasta with tomato basil sauce": {
        "ingredients": ["Pasta", "Tomatoes", "Basil", "Garlic", "Onion", "Zucchini", "Bell pepper"],
        "steps": ["Cook pasta.", "Sauté veggies with garlic and onion.", "Add tomato sauce and basil."],
        "nutrition": {"calories": 400, "protein": 12, "carbs": 60, "fat": 12},
        "video": "https://www.youtube.com/watch?v=some_pasta_video_link",
        "substitutes": {"Pasta": ["Gluten-free pasta"], "Onion/Garlic": ["Asafoetida powder"]},
        "diet_type": ["vegetarian"],
        "allergens": ["gluten", "garlic", "onion"],
        "health_conditions": ["high-bp", "pregnancy"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Oatmeal with fruits": {
        "ingredients": ["Oats", "Water/Milk", "Fruits", "Nuts"],
        "steps": ["Cook oats.", "Top with fruits and nuts."],
        "nutrition": {"calories": 280, "protein": 9, "carbs": 50, "fat": 7},
        "video": "https://www.youtube.com/watch?v=oats_fruits",
        "substitutes": {"Milk": ["Almond milk"]},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": ["milk"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Boiled eggs with toast": {
        "ingredients": ["Eggs", "Bread", "Butter"],
        "steps": ["Boil eggs.", "Toast bread.", "Serve with butter."],
        "nutrition": {"calories": 280, "protein": 15, "carbs": 25, "fat": 10},
        "video": "https://www.youtube.com/watch?v=eggs_toast",
        "substitutes": {"Bread": ["Whole wheat bread"]},
        "diet_type": ["non-vegetarian"],
        "allergens": ["eggs", "gluten", "milk"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s", "40-plus"] # Added "30s"
    },
    "Grilled paneer salad": {
        "ingredients": ["Paneer", "Lettuce", "Cucumber", "Tomato", "Bell Pepper", "Lemon-Herb Dressing"],
        "steps": ["Grill paneer.", "Chop veggies.", "Combine with dressing."],
        "nutrition": {"calories": 350, "protein": 20, "carbs": 15, "fat": 25},
        "video": "https://www.youtube.com/watch?v=paneer_salad",
        "substitutes": {"Paneer": ["Tofu"]},
        "diet_type": ["vegetarian", "gluten-free"],
        "allergens": ["milk"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Quinoa with veggies": {
        "ingredients": ["Quinoa", "Broccoli", "Carrots", "Spinach", "Spices"],
        "steps": ["Cook quinoa.", "Sauté veggies.", "Mix together."],
        "nutrition": {"calories": 300, "protein": 12, "carbs": 45, "fat": 8},
        "video": "https://www.youtube.com/watch?v=quinoa_veggies",
        "substitutes": {},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": [],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Lentil soup with whole grain toast": {
        "ingredients": ["Lentils", "Vegetable broth", "Carrots", "Celery", "Onion", "Whole grain bread"],
        "steps": ["Cook lentils with veggies.", "Serve with toasted bread."],
        "nutrition": {"calories": 380, "protein": 20, "carbs": 50, "fat": 10},
        "video": "https://www.youtube.com/watch?v=lentil_soup",
        "substitutes": {},
        "diet_type": ["vegetarian", "vegan"],
        "allergens": ["onion", "gluten"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Rajma with brown rice": {
        "ingredients": ["Kidney beans (rajma)", "Tomatoes", "Onion", "Garlic", "Ginger", "Spices", "Brown rice"],
        "steps": ["Cook rajma curry.", "Serve with brown rice."],
        "nutrition": {"calories": 420, "protein": 18, "carbs": 70, "fat": 10},
        "video": "https://www.youtube.com/watch?v=rajma_rice",
        "substitutes": {},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": ["onion", "garlic"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Steamed fish with sautéed greens": {
        "ingredients": ["Fish fillet", "Spinach", "Broccoli", "Lemon", "Herbs"],
        "steps": ["Steam fish.", "Sauté greens.", "Serve with lemon and herbs."],
        "nutrition": {"calories": 300, "protein": 30, "carbs": 10, "fat": 15},
        "video": "https://www.youtube.com/watch?v=steamed_fish",
        "substitutes": {},
        "diet_type": ["non-vegetarian", "gluten-free"],
        "allergens": [],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Avocado toast with boiled egg": {
        "ingredients": ["Avocado", "Bread", "Egg", "Salt", "Pepper"],
        "steps": ["Toast bread.", "Mash avocado, spread on toast.", "Top with boiled egg."],
        "nutrition": {"calories": 350, "protein": 15, "carbs": 30, "fat": 20},
        "video": "https://www.youtube.com/watch?v=avocado_egg_toast",
        "substitutes": {"Bread": ["Gluten-free bread"]},
        "diet_type": ["non-vegetarian"],
        "allergens": ["gluten", "eggs"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s", "40-plus"] # Added "30s"
    },
    "Paneer tikka wrap": {
        "ingredients": ["Paneer", "Yogurt", "Spices", "Bell peppers", "Onion", "Whole wheat wrap"],
        "steps": ["Marinate and grill paneer.", "Sauté veggies.", "Wrap in a tortilla."],
        "nutrition": {"calories": 400, "protein": 25, "carbs": 40, "fat": 20},
        "video": "https://www.youtube.com/watch?v=paneer_tikka_wrap",
        "substitutes": {"Wrap": ["Gluten-free wrap"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk", "onion", "gluten"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s"] # Added "30s"
    },
    "Tofu salad with chickpeas and lemon dressing": {
        "ingredients": ["Tofu", "Chickpeas", "Mixed greens", "Cucumber", "Tomato", "Lemon dressing"],
        "steps": ["Press and dice tofu.", "Combine all ingredients with dressing."],
        "nutrition": {"calories": 320, "protein": 20, "carbs": 25, "fat": 15},
        "video": "https://www.youtube.com/watch?v=tofu_salad",
        "substitutes": {},
        "diet_type": ["vegetarian", "vegan", "gluten-free"],
        "allergens": ["soy"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "Chapati with dal and cucumber salad": {
        "ingredients": ["Whole wheat flour", "Lentils (dal)", "Cucumber", "Tomato", "Onion", "Lemon"],
        "steps": ["Make chapatis.", "Cook dal.", "Prepare salad."],
        "nutrition": {"calories": 380, "protein": 15, "carbs": 60, "fat": 8},
        "video": "https://www.youtube.com/watch?v=chapati_dal_salad",
        "substitutes": {},
        "diet_type": ["vegetarian"],
        "allergens": ["gluten", "onion"],
        "health_conditions": ["high-bp", "pregnancy", "hypertension"],
        "age_groups": ["under-30", "30s", "40-plus", "40-plus-women"] # Added "30s"
    },
    "High-Protein Breakfast Burrito": {
        "ingredients": ["Whole wheat tortilla", "Eggs", "Black beans", "Salsa", "Avocado", "Spinach"],
        "steps": ["Scramble eggs.", "Warm beans.", "Assemble burrito."],
        "nutrition": {"calories": 400, "protein": 25, "carbs": 40, "fat": 18},
        "video": "https://www.youtube.com/watch?v=breakfast_burrito",
        "substitutes": {"Tortilla": ["Gluten-free tortilla"]},
        "diet_type": ["non-vegetarian"],
        "allergens": ["gluten", "eggs"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s"] # Added "30s"
    },
    "Greek Yogurt with Granola & Fruit": {
        "ingredients": ["Greek yogurt", "Granola", "Mixed berries", "Honey"],
        "steps": ["Combine ingredients in a bowl."],
        "nutrition": {"calories": 320, "protein": 20, "carbs": 40, "fat": 10},
        "video": "https://www.youtube.com/watch?v=greekyogurt",
        "substitutes": {"Yogurt": ["Plant-based yogurt"]},
        "diet_type": ["vegetarian"],
        "allergens": ["milk", "gluten"],
        "health_conditions": [],
        "age_groups": ["under-30", "30s", "40-plus"] # Added "30s"
    }
}


def translate_text(text, lang_code):
    """Looks up text in the imported TRANSLATIONS dictionary or returns original if no translation exists."""
    return TRANSLATIONS.get(text, {}).get(lang_code, text)

# ----------------------------------------------------
# 2. IMAGE RECOGNITION & MOCK AI
# ----------------------------------------------------

UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# REPLACE your existing analyze_image_for_calories(filename) function with this:

def analyze_image_for_calories(filepath):
    """
    Uses Gemini Pro Vision to analyze the image at the given filepath and estimate nutrition.
    The file is temporarily saved by the route, and we use the full path here.
    """
    try:
        client = genai.Client()        
        # 1. Prepare the image as a byte array part for the API call
        with open(filepath, "rb") as f:
            image_bytes = f.read()
            
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg" # Use this for safety, assuming common formats
        )
            
        # 2. Define the structured output schema for reliable JSON results
        schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "food_item": types.Schema(type=types.Type.STRING, description="The most dominant food item, e.g., dosa."),
                "calories": types.Schema(type=types.Type.INTEGER, description="Total estimated Kcal for the serving shown."),
                "protein": types.Schema(type=types.Type.NUMBER),
                "carbs": types.Schema(type=types.Type.NUMBER),
                "fat": types.Schema(type=types.Type.NUMBER)
            },
            required=["food_item", "calories", "protein", "carbs", "fat"]
        )

        # 3. Craft the prompt and call the model
        prompt_parts = [
            image_part,
            "You are a professional nutritionist. Analyze the image. Identify the main food item and estimate the total macronutrients and calories for the serving size shown. Return the output as a clean JSON object."
        ]
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_parts,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )
        
        # 4. Return the parsed JSON object
        if response.text:
            return json.loads(response.text)
        
        return {'food': 'AI Failed', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        # Ensure the user's uploaded file is deleted in the calling route even if this fails.
        return {'food': 'Analysis Failed', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

# ----------------------------------------------------
# 3. APP CONFIGURATION & FILE HELPERS
# ----------------------------------------------------

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'A_VERY_STRONG_RANDOM_SECRET_KEY_FOR_SMARTDIET_PLUS' 

@app.before_request
def before_request():
    if 'language' not in session:
        session['language'] = 'en'
    
    g.lang_code = session['language']
    g.translate = lambda text: translate_text(text, g.lang_code)
    g.LANGUAGES = LANGUAGES


# Create a blueprint for recipe-related routes
recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')
app.register_blueprint(login_bp) 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
FOOD_LOGS_FILE = os.path.join(DATA_FOLDER, 'food_logs.json')
USER_PROFILES_FILE = os.path.join(DATA_FOLDER, 'user_profiles.json')

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


# --- Helper functions for JSON file operations ---
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

# exicers 
# ========================= EXERCISES DATA (NEW) =========================
# This new data structure holds exercises tailored by age and gender
exercises_data = {
    "Yoga and Stretching": {
        "description": "Improves flexibility and reduces stress.",
        "gender_specifics": ["all"],
        "age_groups": ["30s", "40s", "50-plus"],
        "benefits": ["flexibility", "stress reduction", "joint health"]
    },
    "Light Cardio (Brisk Walking, Swimming)": {
        "description": "Excellent for cardiovascular health with low impact on joints.",
        "gender_specifics": ["all"],
        "age_groups": ["40s", "50-plus"],
        "benefits": ["cardiovascular health", "endurance"]
    },
    "Bodyweight Strength Training (Planks, Squats)": {
        "description": "Builds muscle tone and core strength using your own body.",
        "gender_specifics": ["all"],
        "age_groups": ["30s", "40s"],
        "benefits": ["strength", "muscle tone", "endurance"]
    },
    "High-Intensity Interval Training (HIIT)": {
        "description": "Short bursts of intense exercise followed by rest.",
        "gender_specifics": ["all"],
        "age_groups": ["under-30", "30s"],
        "benefits": ["cardiovascular health", "weight loss", "metabolism boost"]
    },
    "Heavy Weightlifting": {
        "description": "For building significant muscle mass and strength.",
        "gender_specifics": ["male"],
        "age_groups": ["under-30", "30s", "40s"],
        "benefits": ["strength", "muscle building"]
    },
    "Pilates": {
        "description": "Focuses on core strength, posture, and flexibility.",
        "gender_specifics": ["female", "all"],
        "age_groups": ["30s", "40s", "50-plus"],
        "benefits": ["core strength", "flexibility", "posture"]
    },
    "Kegel Exercises": {
        "description": "Strengthens pelvic floor muscles, highly recommended.",
        "gender_specifics": ["female"],
        "age_groups": ["40s", "50-plus"],
        "benefits": ["pelvic health", "core strength"]
    },
    "Running and Cycling": {
        "description": "Classic cardio for burning calories and improving heart health.",
        "gender_specifics": ["all"],
        "age_groups": ["under-30", "30s", "40s"],
        "benefits": ["cardiovascular health", "endurance", "calorie burning"]
    },
    "Tai Chi or Qigong": {
        "description": "Low-impact exercises focusing on balance and calm.",
        "gender_specifics": ["all"],
        "age_groups": ["50-plus"],
        "benefits": ["balance", "joint health", "stress reduction"]
    },
    "Dance Cardio": {
        "description": "Fun, high-energy exercise that improves coordination.",
        "gender_specifics": ["female", "all"],
        "age_groups": ["under-30", "30s"],
        "benefits": ["cardiovascular health", "coordination", "stress reduction"]
    },
    "Golf or Walking on Hilly Terrain": {
        "description": "A low-impact activity that combines walking with skill.",
        "gender_specifics": ["male", "all"],
        "age_groups": ["50-plus"],
        "benefits": ["cardiovascular health", "endurance", "mental focus"]
    },
}


# ========================= EXERCISE FILTERING LOGIC (NEW) =========================
# This function selects exercises based on the user's age and gender.
def filter_exercises(user_age, user_gender):
    """
    Filters exercises based on a person's age and gender.
    """
    if user_age <= 30:
        age_group = "under-30"
    elif 30 < user_age <= 40:
        age_group = "30s"
    elif 40 < user_age <= 50:
        age_group = "40s"
    else:
        age_group = "50-plus"
    
    user_gender = user_gender.lower() if user_gender else "all"

    filtered_exercises = []
    
    for exercise_name, exercise_details in exercises_data.items():
        age_matches = age_group in exercise_details.get("age_groups", [])
        gender_matches = "all" in exercise_details.get("gender_specifics", []) or user_gender in exercise_details.get("gender_specifics", [])

        if age_matches and gender_matches:
            filtered_exercises.append(exercise_name)
    
    return random.sample(filtered_exercises, k=min(len(filtered_exercises), 3))


def filter_recipes(user_age, user_gender, user_diet_preference, user_allergies, user_health_conditions):
    """
    Filters recipes based on a comprehensive set of user preferences.
    """
    filtered_meals = {}
    user_diet_preference = user_diet_preference.lower() if user_diet_preference else ""
    user_allergies_list = [a.strip().lower() for a in user_allergies.split(',') if a.strip()] if user_allergies else []
    user_health_conditions_list = [h.strip().lower() for h in user_health_conditions.split(',') if h.strip()] if user_health_conditions else []
    all_filtered_recipes = []

    for meal_name, recipe_details in recipes_basic_data.items():
        # --- 1. Diet Filter ---
        if user_diet_preference and user_diet_preference not in recipe_details.get("diet_type", []):
            continue
        
        # --- 2. Allergy Filter ---
        has_allergen = any(allergen in recipe_details.get("allergens", []) for allergen in user_allergies_list)
        if has_allergen:
            continue
        
        # --- 3. Health Conditions Filter ---
        is_unsuitable_for_health_condition = any(
            cond in recipe_details.get("health_conditions", []) for cond in user_health_conditions_list
        )
        if is_unsuitable_for_health_condition:
            continue
        
        # --- 4. Age Group Filter (FIXED) ---
        age_group_match = False
        recipe_age_groups = recipe_details.get("age_groups", [])

        # Assign user to an age group key
        user_age_key = None
        if user_age <= 30:
            user_age_key = "under-30"
        elif 30 < user_age <= 40:
            user_age_key = "30s"
        elif user_age > 40:
            if user_gender.lower() == "female":
                user_age_key = "40-plus-women"
            else:
                user_age_key = "40-plus"

        # Check if the user's age key is in the recipe's age groups, or if the recipe has no specific age groups
        if not recipe_age_groups or user_age_key in recipe_age_groups:
            age_group_match = True
            
        if not age_group_match:
            continue

        # If all filters passed, add the recipe
        all_filtered_recipes.append(meal_name)
    
    # ... (The rest of the function for organizing meals into breakfast, lunch, dinner remains the same)
    breakfast_options = [meal for meal in all_filtered_recipes if "pancakes" in meal.lower() or "oats" in meal.lower() or "sandwich" in meal.lower() or "eggs" in meal.lower() or "smoothie" in meal.lower() or "idli" in meal.lower() or "chilla" in meal.lower() or "toast" in meal.lower() or "cornflakes" in meal.lower() or "poha" in meal.lower() or "upma" in meal.lower() or "burrito" in meal.lower() or "yogurt" in meal.lower()]
    lunch_options = [meal for meal in all_filtered_recipes if "salad" in meal.lower() or "soup" in meal.lower() or "curry" in meal.lower() or "khichdi" in meal.lower() or "wrap" in meal.lower() or "pulao" in meal.lower() or "chole" in meal.lower() or "dal" in meal.lower() or "quesadilla" in meal.lower() or "burrito" in meal.lower() or "chicken" in meal.lower() or "paneer" in meal.lower() or "stir fry" in meal.lower() or "roti" in meal.lower()]
    dinner_options = [meal for meal in all_filtered_recipes if "quinoa" in meal.lower() or "soup" in meal.lower() or "stir fry" in meal.lower() or "pasta" in meal.lower() or "fish" in meal.lower() or "rajma" in meal.lower() or "noodles" in meal.lower() or "chicken" in meal.lower() or "shepherd" in meal.lower() or "salmon" in meal.lower() or "lasagna" in meal.lower()]
    
    filtered_meals['breakfast'] = random.sample(list(set(breakfast_options)), k=min(len(set(breakfast_options)), 6))
    filtered_meals['lunch'] = random.sample(list(set(lunch_options)), k=min(len(set(lunch_options)), 6))
    filtered_meals['dinner'] = random.sample(list(set(dinner_options)), k=min(len(set(dinner_options)), 6))

    return filtered_meals

def generate_recommendations(age, gender, occupation, diet_preference,city,allergies, health_conditions):
    occupation = occupation.lower()
    if any(word in occupation for word in ['office', 'desk', 'manager', 'it', 'software', 'admin']):
        activity_level = 'low'
    elif any(word in occupation for word in ['construction', 'labor', 'manual', 'driver', 'farmer', 'delivery']):
        activity_level = 'high'
    else:
        activity_level = 'medium'
    
    meals = filter_recipes(age, gender, diet_preference, allergies, health_conditions)
    
    # This is the new line that calls the advanced exercise function
    exercises = filter_exercises(age, gender)

    return {
        'meals': meals,
        'exercises': exercises
    }

# ----------------------------------------------------
# 5. FLASK ROUTES
# ----------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes_page():
    return render_template('recipes.html')

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    """Sets the user's language preference in the session and redirects back."""
    if lang_code in LANGUAGES:
        session['language'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route('/upload_food_image', methods=['POST'])
def upload_food_image():
    user_id = session.get('email', 'demo_user')
    
    if 'food_image' not in request.files:
        return jsonify({'error': g.translate('No file part in the request.')}), 400
    
    file = request.files['food_image']
    original_filename = file.filename
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': g.translate('Invalid or missing file selected.')}), 400
        
    unique_filename = str(uuid.uuid4()) + secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)
    

    # 2. Analyze the image using the mock function
    analysis_result = analyze_image_for_calories(filepath) 
     
    os.remove(filepath) 
    
    return jsonify({
        'message': g.translate('Analysis complete!'),
        'result': analysis_result,
        'log_prompt': g.translate('Click "Log Meal" to add this to your tracker.')
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()

        age =   age = int(data.get('age'))
        gender = data.get('gender')
        occupation = data.get('occupation')
        diet_preference = data.get('diet_preference')
        city = data.get('city')
        allergies = data.get('allergies', '').lower()
        health_conditions = data.get('health_conditions', '').lower()

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
            age, gender, occupation, diet_preference, city, allergies,health_conditions
        )

        return jsonify(recommendations)

    except Exception as e:
        print(f"Error in /recommend route: {e}")
        return jsonify({"error": f"Failed to process recommendation request: {str(e)}. Check if all required profile data (age, gender, occupation, diet, city) is sent from the frontend."}), 500

@app.route('/submit_user', methods=['POST'])
def submit_user():
    try:
        data = request.get_json()
        if data:
            name = data.get('username')
            age = data.get('age')
            email = data.get('email')
            password = data.get('password')
            
            gender = data.get('gender')
            occupation = data.get('occupation')
            diet_preference = data.get('diet_preference')
            city = data.get('city')
            allergies = data.get('allergies')
            notes = data.get('notes')
            health_conditions = data.get('health_conditions')

            if not password:
                return jsonify({"error": "Password is required for sign-up."}), 400
            
            
            insert_user(name, age, email, password, diet_preference, occupation, city, allergies, notes, gender,health_conditions)
            
            return jsonify({"message": "User data successfully saved!"}), 201
        else:
            return jsonify({"error": "No JSON data received."}), 400
    except Exception as e:
        print(f"Error in /submit_user route: {e}")
        return jsonify({"error": "Failed to save user data."}), 500
    
# REPLACE YOUR CURRENT @app.route('/generate_smart_meal', methods=['GET']) FUNCTION WITH THIS:
# In app.py, find and replace the entire def generate_smart_meal(): block with this:

@app.route('/generate_smart_meal', methods=['POST'])
def generate_smart_meal():
    try:
        # 1. Retrieve user data (sent from the frontend form)
        data = request.get_json()
        age = int(data.get('age', 30))
        gender = data.get('gender', 'not specified')
        diet_preference = data.get('diet_preference', 'vegetarian')
        allergies = data.get('allergies', 'none')
        health_conditions = data.get('health_conditions', 'none')

        client = genai.Client()

        # 2. Define the schema to force the AI to return MEAL NAME AND INGREDIENTS
        meal_schema = types.Schema(type=types.Type.OBJECT, properties={
            "name": types.Schema(type=types.Type.STRING),
            "ingredients": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="List of unique, essential ingredients.")
        }, required=["name", "ingredients"])

        schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "breakfast": meal_schema,
                "lunch": meal_schema,
                "dinner": meal_schema
            },
            required=["breakfast", "lunch", "dinner"]
        )

        prompt = (
            f"Generate a balanced daily meal plan (breakfast, lunch, and dinner) for an individual with: "
            f"Age: {age}, Gender: {gender}, Diet: {diet_preference}, Allergies: {allergies}, Health Status: {health_conditions}. "
            "For each meal, provide the meal name and the unique essential ingredients. Respond ONLY with a clean JSON object following the schema."
        )

        # 3. Call the Gemini API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )
        
        # 4. Process the response
        meal_data = json.loads(response.text)
        grocery_list = []

        for meal_type in ["breakfast", "lunch", "dinner"]:
            meal = meal_data.get(meal_type, {"name": "No meal provided", "ingredients": []})
            if meal.get("ingredients"):
                grocery_list.extend(meal["ingredients"])
        
        unique_grocery_list = sorted(list(set(grocery_list)))
        
        # 5. Final Return
        formatted_response = {
            "breakfast": [meal_data["breakfast"]] if meal_data.get("breakfast") else [],
            "lunch": [meal_data["lunch"]] if meal_data.get("lunch") else [],
            "dinner": [meal_data["dinner"]] if meal_data.get("dinner") else [],
            "grocery_list": unique_grocery_list # <--- THE COMPLETE, AI-GENERATED LIST
        }

        return jsonify(formatted_response)

    except Exception as e:
        print(f"Gemini Meal Generation Error: {e}")
        # 🚨 FINAL FIX: RETURN A GRACEFUL EMPTY LIST INSTEAD OF CRASHING/HARDCODED MESSAGE 🚨
        return jsonify({"breakfast": [], "lunch": [], "dinner": [], "grocery_list": []})
# recipe

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
        recipe_allergies_lower = [a.lower()
                                  for a in recipe.get('allergies', [])]

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

        print(
            f"Recipe '{recipe.get('title', 'N/A')}': should_include = {should_include}")
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
@app.route('/recipe', methods=['POST'])
def get_recipe():
    data = request.json
    recipe_name = data.get("recipe_name")
    # Using the integrated basic recipe data
    recipe = recipes_basic_data.get(recipe_name)
    if recipe:
        return jsonify(recipe)
    return jsonify({"error": "Recipe not found"}), 404



@app.route('/calories', methods=['POST'])
def calories():
    """Placeholder for future calorie tracking."""
    data = request.json
    return jsonify({"status": "success", "data": data})

@app.route('/log_food', methods=['POST'])
def log_food_entry():
    # ... (content omitted for brevity - the function logic is fine) ...
    try:
        data = request.get_json()

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

        user_logs[log_date] = food_logs_for_date
        all_logs[user_id] = user_logs
        save_food_logs_data(all_logs)

        return jsonify({"message": "Food logged successfully!", "log_id": new_log['id']}), 201

    except Exception as e:
        print(f"Error in /log_food: {e}")
        return jsonify({"error": "Failed to log food entry: {str(e)}"}), 500


@app.route('/get_daily_calorie_summary', methods=['GET'])
def get_daily_calorie_summary_route():
    # ... (content omitted for brevity - the function logic is fine) ...
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
    # ... (content omitted for brevity - the function logic is fine) ...
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
        return jsonify({"error": f"Failed to delete food log entry: {str(e)}"}), 500
    
    # --- In app.py: Add this block to the top of your file ---
# GLOBAL IN-MEMORY STORAGE (Resets when server restarts - use PyMySQL for persistence)
REMINDER_SCHEDULES = {} 
DEFAULT_USER_ID = "user_2" # Use "user_2" to match your server log output

# Helper functions for storage
def save_user_schedule(user_id, schedule_data):
    # Expects a dictionary like {'water_status': 'Active', 'water_times': '10:00 AM, 2:00 PM, 5:00 PM'}
    REMINDER_SCHEDULES[user_id] = schedule_data
    print(f">>> Reminders data successfully formatted for user {user_id}: {schedule_data}")

def get_user_schedule(user_id):
    # Returns the stored dictionary or a default structure
    return REMINDER_SCHEDULES.get(user_id, {
        'water_status': 'Inactive', 
        'water_times': '' 
    })

# --- NEW FLASK ROUTES ---

# Route 1: To GET the current schedule (for displaying and starting the checker)
@app.route('/user/get_reminders', methods=['GET'])
def get_reminders():
    # In a real app, you would fetch this from PyMySQL using the current user's ID
    schedule_data = get_user_schedule(DEFAULT_USER_ID)
    return jsonify(schedule_data)

# Route 2: To SAVE the new schedule (for the "Edit/View Schedule" feature)
@app.route('/user/update_reminders', methods=['POST'])
def update_reminders():
    try:
        data = request.get_json()
        
        # The frontend sends the full schedule dictionary
        save_user_schedule(DEFAULT_USER_ID, data)
        
        return jsonify({"status": "success", "message": "Schedule updated."})
    except Exception as e:
        print(f"Error updating reminders: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)