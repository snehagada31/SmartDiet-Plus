# config.py

import os

# Define the base directory (where app.py and config.py are)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the folder where your data files will be stored
# This will create a 'data' subfolder next to your app.py
DATA_FOLDER = os.path.join(BASE_DIR, 'data')

# Full paths to your JSON data files
FOOD_LOGS_FILE = os.path.join(DATA_FOLDER, 'food_logs.json')
USER_PROFILES_FILE = os.path.join(DATA_FOLDER, 'user_profiles.json')

# --- Important: Create the data folder if it doesn't exist ---
# This part ensures the directory is ready when your app starts.
# It's here because it's part of the configuration setup.
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Config: Created data directory at {DATA_FOLDER}")