import pymysql
from datetime import datetime, date # Import date for CURDATE comparison

# --- PyMySQL Configuration ---
# NOTE: Ensure these credentials match your running MySQL server (e.g., XAMPP or WAMP)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # IMPORTANT: Use your actual MySQL root password here if you set one
    'database': 'smartdiet',
    'port': 3306,
    'charset': 'utf8mb4',
    # Returns results as dictionaries for easy access in Flask templates
    'cursorclass': pymysql.cursors.DictCursor 
}
# -----------------------------

def get_db_connection():
    """Establishes and returns a PyMySQL database connection."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print(">>> Database connection successful (PyMySQL)")
        return conn
    except pymysql.Error as err:
        print(f">>> PyMySQL Connection Error: {err}")
        return None

# --- Existing Fetch Functions ---

def fetch_user_profile_by_email(email):
    """Fetches a single user's complete profile from the user_profiles table by email."""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = None
    try:
        cursor = conn.cursor()
        print(">>> Cursor created for fetching.")
        
        query = "SELECT * FROM user_profiles WHERE email = %s"
        cursor.execute(query, (email,))
        profile_data = cursor.fetchone()
        
        if profile_data:
            print(f">>> Profile fetched successfully for {email}")
        else:
            print(f">>> Profile not found for {email}")
            
        return profile_data

    except pymysql.Error as err:
        print(f">>> PyMySQL Error during fetch: {err}")
        return None
        
    finally:
        if cursor: cursor.close()
        if conn and conn.open: conn.close()
        print(">>> DB connection closed after fetch.")


# ----------------------------------------------------------------------
# FETCH DATA SUMMARY (Calorie/Macros)
# ----------------------------------------------------------------------
def fetch_data_summary(user_id):
    """
    Fetches personalized calorie and macro data for the dashboard 
    for the current day.
    """
    conn = get_db_connection()
    if not conn: return None

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                COALESCE(SUM(calories_intake), 0) AS total_calories,
                COALESCE(SUM(protein_intake), 0) AS total_protein,
                MAX(date_logged) AS last_updated 
            FROM diet_recommendation 
            WHERE user_id = %s AND DATE(date_logged) = CURDATE();
        """
        cursor.execute(query, (user_id,))
        summary = cursor.fetchone()
        
        if summary:
            summary['calories_goal'] = 2000  # Example: Default goal
            if summary['last_updated']:
                 summary['last_updated'] = summary['last_updated'].strftime('%Y-%m-%d')
            else:
                 summary['last_updated'] = date.today().strftime('%Y-%m-%d')
        
        print(f">>> Data summary fetched for user {user_id}: {summary}")
        return summary
    except pymysql.Error as err:
        print(f">>> Error fetching data summary: {err}")
        return None
    finally:
        if cursor: cursor.close()
        if conn and conn.open: conn.close()
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# FETCH HEALTH AND PROGRESS (Weight/Sleep)
# ----------------------------------------------------------------------
def fetch_health_and_progress(user_id):
    """
    Fetches latest health, weight, and sleep metrics.
    Assumes a 'user_progress' table with columns 'user_id', 'weight', and 'sleep_duration'.
    """
    conn = get_db_connection()
    # Provide defaults in case of no connection/error
    default_result = {'latest_weight': 'N/A', 'sleep_duration': 'N/A'}
    if not conn: return default_result

    cursor = None
    try:
        cursor = conn.cursor()
        
        query_progress = """
            SELECT weight, sleep_duration 
            FROM user_progress 
            WHERE user_id = %s 
            ORDER BY date_logged DESC 
            LIMIT 1;
        """
        cursor.execute(query_progress, (user_id,))
        progress = cursor.fetchone()
        
        result = {
            # Use the fetched data, or the default 'N/A' if no record exists
            'latest_weight': progress.get('weight', 'N/A') if progress and progress.get('weight') is not None else 'N/A',
            'sleep_duration': progress.get('sleep_duration', 'N/A') if progress and progress.get('sleep_duration') is not None else 'N/A'
        }
        print(f">>> Progress data fetched for user {user_id}: {result}")
        return result
    except pymysql.Error as err:
        print(f">>> Error fetching health/progress: {err}")
        return default_result
    finally:
        if cursor: cursor.close()
        if conn and conn.open: conn.close()
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# FETCH INTAKE REMINDERS (MAPPED TO HTML TEMPLATE EXPECTATIONS)
# ----------------------------------------------------------------------
def fetch_intake_reminders(user_id):
    """
    Fetches active reminder settings for the user.
    NOTE: Currently returns hardcoded data to match the screenshot structure.
    """
    # Placeholder data
    reminders = {
        'water_active': True,
        'meal_times': ['10:00 AM', '2:00 PM', '5:00 PM']
    }
    
    # Map placeholder data to the keys expected by the profile.html template
    result = {
        # Template expects 'water_status', so convert boolean to string
        'water_status': 'Active' if reminders['water_active'] else 'Inactive', 
        # Template expects 'water_times' as a single string
        'water_times': ', '.join(reminders['meal_times'])
    }
    
    # In a real application, you would fetch these from a 'user_reminders' table.
    
    print(f">>> Reminders data successfully formatted for user {user_id}: {result}")
    return result
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# FETCH MEAL HISTORY (Retrieves list of all meals)
# ----------------------------------------------------------------------
def fetch_meal_history(user_id):
    """
    Retrieves all meal log entries for a specific user, ordered by date.
    Returns a list of dictionaries, including the 'id' for management.
    """
    conn = get_db_connection()
    if not conn:
        return []

    cursor = None
    try:
        cursor = conn.cursor()
        
        # NOTE: 'id' is crucial for deletion/editing
        query = """
            SELECT 
                id,                  
                food_name, 
                calories_intake, 
                protein_intake, 
                DATE_FORMAT(date_logged, '%%Y-%%m-%%d at %%H:%%i') AS logged_time 
            FROM diet_recommendation 
            WHERE user_id = %s 
            ORDER BY date_logged DESC;
        """
        cursor.execute(query, (user_id,))
        
        meal_history = cursor.fetchall()
        
        print(f">>> Fetched {len(meal_history)} historical meal entries for user {user_id}.")
        return meal_history

    except pymysql.Error as err:
        print(f">>> Error fetching meal history: {err}")
        return []
    finally:
        if cursor: cursor.close()
        if conn and conn.open: conn.close()
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# INSERT FOOD LOG ENTRY
# ----------------------------------------------------------------------
def insert_food_log(user_id, calories, protein, food_name):
    """
    Inserts a user's food log entry into the diet_recommendation table.
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        print(f">>> Attempting to log meal for user ID: {user_id}")

        query = """
        INSERT INTO diet_recommendation 
        (user_id, calories_intake, protein_intake, food_name)
        VALUES (%s, %s, %s, %s)
        """
        values = (user_id, calories, protein, food_name)

        cursor.execute(query, values)
        conn.commit()
        print(f">>> Food log inserted successfully for user {user_id}: {food_name}")
        return True

    except pymysql.Error as err:
        print(f">>> PyMySQL Error during food log insert: {err}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn and conn.open:
            conn.close()
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# ✅ MANAGEMENT FUNCTION: DELETE MEAL ENTRY
# ----------------------------------------------------------------------
def delete_meal_entry(meal_id, user_id):
    """
    Deletes a specific meal entry, ensuring it belongs to the user for security.
    """
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        # CRITICAL: Delete based on meal_id AND user_id for security
        query = "DELETE FROM diet_recommendation WHERE id = %s AND user_id = %s"
        cursor.execute(query, (meal_id, user_id))
        conn.commit()
        return cursor.rowcount > 0 
    except pymysql.Error as err:
        print(f">>> DB Error deleting meal: {err}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.open: conn.close()

# ----------------------------------------------------------------------
# ✅ MANAGEMENT FUNCTION: UPDATE MEAL ENTRY (For future use)
# ----------------------------------------------------------------------
def update_meal_entry(meal_id, user_id, food_name, calories, protein):
    """
    Updates a specific meal entry, ensuring it belongs to the user.
    """
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            UPDATE diet_recommendation 
            SET food_name = %s, calories_intake = %s, protein_intake = %s
            WHERE id = %s AND user_id = %s
        """
        cursor.execute(query, (food_name, calories, protein, meal_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except pymysql.Error as err:
        print(f">>> DB Error updating meal: {err}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.open: conn.close()


# --- Existing Update and Insert Functions ---

def update_user_profile(user_id, data):
    """Updates a user's profile data in the user_profiles table based on their ID."""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        print(f">>> Starting profile update for user ID: {user_id}")

        column_mapping = {
            'age': 'age', 'gender': 'gender', 'occupation': 'occupation', 
            'city': 'city', 'diet_pref': 'diet_pref', 'allergies': 'allergies',
            'notes': 'notes'
        }

        set_clauses = []
        values = []
        
        for form_key, db_column in column_mapping.items():
            if form_key == 'diet_pref':
                value = data.get('diet_preference')
            else:
                value = data.get(form_key)
            
            if value is not None:
                set_clauses.append(f"{db_column} = %s")
                values.append(value)

        if not set_clauses:
            print(">>> No data provided to update.")
            return True

        sql_query = f"UPDATE user_profiles SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(user_id)
        
        cursor.execute(sql_query, values)
        conn.commit()
        print(f">>> Profile successfully updated for user ID: {user_id}")
        return True

    except pymysql.Error as err:
        print(f">>> PyMySQL Error during profile update: {err}")
        if conn: conn.rollback()
        return False
        
    finally:
        if cursor: cursor.close()
        if conn and conn.open: conn.close()
        print(">>> DB connection closed after update.")


def insert_user(name, age, email, password_hash, diet_pref,health_condition, occupation=None, city=None, allergies=None, notes=None, gender=None):
    """Inserts new user data into the user_profiles table."""
    conn = get_db_connection()
    if not conn: return
    cursor = None
    try:
        print(">>> Entering insert_user function...")
        cursor = conn.cursor()
        
        query = """
        INSERT INTO user_profiles (name, age, email, password, diet_pref,health_condition, occupation, city, allergies, notes, submitted_at, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        values = (name, age, email, password_hash, diet_pref, health_condition, occupation, city, allergies, notes, datetime.now(), gender)

        cursor.execute(query, values)
        conn.commit()
        print(f"User '{name}' data inserted successfully.")

    except pymysql.Error as err:
        print(f">>> PyMySQL Error during insert: {err}")
        if conn: conn.rollback()
        print(">>> Transaction rolled back due to error")

    finally:
        if cursor: cursor.close()
        if conn and conn.open: conn.close()
        print(">>> Exiting insert_user function.")

if __name__ == "__main__":
    pass