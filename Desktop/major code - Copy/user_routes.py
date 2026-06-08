from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import check_password_hash 
# ALL NECESSARY IMPORTS FROM DB_INSERT
from db_insert import (
    fetch_user_profile_by_email, 
    update_user_profile,
    fetch_data_summary,              
    fetch_health_and_progress,   # ✅ USED FOR LATEST WEIGHT/SLEEP
    fetch_intake_reminders,      # ✅ USED FOR REMINDER DATA
    insert_food_log,
    fetch_meal_history,
    delete_meal_entry,
    update_meal_entry 
)
# ✅ FINAL IMPORTS from user_metrics.py
from user_metrics import (
    insert_progress_log, 
    fetch_full_progress_history, 
    fetch_single_progress_entry, 
    update_progress_entry 
)

# 1. Create the User Blueprint
login_bp = Blueprint('login_bp', __name__, url_prefix='/user')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
        except:
            return jsonify({"error": "Invalid data format or missing fields."}), 400

        user = fetch_user_profile_by_email(email) 
        
        # Unsecured login check (as requested)
        if user and user.get('password') == password:
            session['loggedin'] = True
            session['email'] = user['email']
            session['user_id'] = user['id'] 
            
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
            
    return render_template('login.html')


# ----------------------------------------------------------------------
# PROFILE PAGE ROUTE (MODIFIED)
# ----------------------------------------------------------------------
@login_bp.route('/profile')
def profile():
    # 1. Security Check
    if not session.get('loggedin'):
        return redirect(url_for('login_bp.login'))

    user_email = session['email']
    user_id = session.get('user_id')
    
    # 2. FETCH STATIC PROFILE DATA
    profile_data = fetch_user_profile_by_email(user_email) 

    # 3. FETCH DYNAMIC DASHBOARD DATA
    if user_id:
        # These functions are assumed to be implemented in db_insert.py
        summary_data = fetch_data_summary(user_id)
        # progress_data will contain latest_weight, sleep_duration, etc.
        progress_data = fetch_health_and_progress(user_id) 
        # reminders_data will contain water_status, water_times, etc.
        reminders_data = fetch_intake_reminders(user_id) 
        history_data = fetch_meal_history(user_id)
    else:
        summary_data, progress_data, reminders_data, history_data = None, None, None, []
    
    
    if profile_data:
        # 4. Render the page with ALL data
        return render_template('profile.html', 
                               profile=profile_data,
                               summary=summary_data,
                               # Pass the fetched data for the new boxes
                               progress=progress_data,
                               reminders=reminders_data,
                               history=history_data)
    else:
        session.clear() 
        return redirect(url_for('login_bp.login', error='Profile data is missing.'))


# ----------------------------------------------------------------------
# PROFILE UPDATE SUBMISSION (Your existing code)
# ----------------------------------------------------------------------
@login_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if not session.get('loggedin') or 'user_id' not in session:
        flash('You must be logged in to update your profile.', 'error')
        return redirect(url_for('login_bp.login'))

    user_id = session['user_id']
    
    try:
        data = {
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'occupation': request.form.get('occupation'),
            'city': request.form.get('city'),
            'diet_pref': request.form.get('diet_preference'), 
            'allergies': request.form.get('allergies'),
            'notes': request.form.get('notes'),
        }
    except Exception as e:
        flash('Error processing form data.', 'error')
        return redirect(url_for('login_bp.profile'))

    success = update_user_profile(user_id, data)
    
    if success:
        flash('Your profile has been successfully updated!', 'success')
    else:
        flash('Failed to update profile. Please try again.', 'error')
        
    return redirect(url_for('login_bp.profile'))


# ----------------------------------------------------------------------
# MEAL LOG SUBMISSION (Your existing code)
# ----------------------------------------------------------------------
@login_bp.route('/log_meal', methods=['POST'])
def log_meal():
    if not session.get('loggedin') or 'user_id' not in session:
        flash('Session expired. Please log in to log your meal.', 'error')
        return redirect(url_for('login_bp.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        try:
            calories = int(request.form.get('calories'))
            protein = int(request.form.get('protein'))
            food_name = request.form.get('food_name').strip() 
        
        except (ValueError, TypeError):
            flash('Error: Please enter valid numbers for Calories and Protein.', 'error')
            return redirect(url_for('login_bp.profile')) 
        except Exception as e:
            flash(f'An unexpected error occurred during data processing: {e}', 'error')
            return redirect(url_for('login_bp.profile'))

        success = insert_food_log(user_id, calories, protein, food_name)

        if success:
            flash(f'Meal "{food_name}" logged successfully! Your summary is updated.', 'success')
        else:
            flash('Failed to log meal due to a database error.', 'error')
            
        return redirect(url_for('login_bp.profile'))
    
    return redirect(url_for('login_bp.profile'))


# ----------------------------------------------------------------------
# MEAL MANAGEMENT (Delete Functionality)
# ----------------------------------------------------------------------
@login_bp.route('/manage_meal/<int:meal_id>', methods=['POST'])
def manage_meal(meal_id):
    if not session.get('loggedin') or 'user_id' not in session:
        flash('You must be logged in to manage meals.', 'error')
        return redirect(url_for('login_bp.login'))

    user_id = session['user_id']
    action = request.form.get('action')
    
    if action == 'delete':
        if delete_meal_entry(meal_id, user_id):
            flash('Meal entry successfully deleted.', 'success')
        else:
            flash('Failed to delete meal entry. Meal not found or ownership issue.', 'error')
            
    return redirect(url_for('login_bp.profile'))


# ----------------------------------------------------------------------
# LOG PROGRESS SUBMISSION (Saves Weight/Sleep data from the mini-form)
# ----------------------------------------------------------------------
@login_bp.route('/log_progress', methods=['POST'])
def log_progress():
    if not session.get('loggedin') or 'user_id' not in session:
        flash('Please log in to update progress.', 'error')
        return redirect(url_for('login_bp.login'))

    user_id = session['user_id']
    
    try:
        weight_str = request.form.get('weight')
        sleep_str = request.form.get('sleep')
        
        weight = float(weight_str) if weight_str else None
        sleep_duration = float(sleep_str) if sleep_str else None
        
        if weight is None and sleep_duration is None:
              flash('Please enter your Weight or Sleep Duration.', 'error')
              return redirect(url_for('login_bp.profile'))
              
    except ValueError:
        flash('Weight and Sleep must be valid numbers.', 'error')
        return redirect(url_for('login_bp.profile'))

    success = insert_progress_log(user_id, weight, sleep_duration)

    if success:
        flash('Health metrics successfully updated!', 'success')
    else:
        flash('Failed to update metrics due to a database error.', 'error')
        
    return redirect(url_for('login_bp.profile'))
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# PROGRESS HISTORY PAGE (Resolves the /user/progress_log 404)
# ----------------------------------------------------------------------
@login_bp.route('/progress_log')
def progress_log():
    if not session.get('loggedin'):
        return redirect(url_for('login_bp.login'))

    user_id = session.get('user_id')
    
    # Fetch the full progress history list
    history_list = fetch_full_progress_history(user_id) 
    
    # Renders the HTML file you created
    return render_template('progress.html', history=history_list) 
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# DISPLAY/PROCESS EDIT FORM (Health History)
# ----------------------------------------------------------------------
@login_bp.route('/edit_progress/<int:entry_id>', methods=['GET', 'POST'])
def edit_progress(entry_id):
    if not session.get('loggedin'):
        flash('Please log in to edit entries.', 'error')
        return redirect(url_for('login_bp.login'))

    user_id = session.get('user_id')
    
    # --- A. Handle POST Submission (Update Logic) ---
    if request.method == 'POST':
        try:
            weight = float(request.form.get('weight'))
            sleep_duration = float(request.form.get('sleep_duration'))
            
            # Call the database update function
            success = update_progress_entry(entry_id, user_id, weight, sleep_duration)

            if success:
                flash('Progress entry successfully updated!', 'success')
            else:
                flash('Failed to update entry (it may have already been deleted).', 'error')
            
            return redirect(url_for('login_bp.progress_log'))
        
        except ValueError:
            flash('Weight and Sleep must be valid numbers.', 'error')
            
    # --- B. Handle GET Request (Display Form) ---
    entry_data = fetch_single_progress_entry(entry_id, user_id)

    if not entry_data:
        flash('Progress entry not found or access denied.', 'error')
        return redirect(url_for('login_bp.progress_log'))

    return render_template('edit_progress.html', entry=entry_data)
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# REMINDER SETTINGS PAGE (MODIFIED LINK)
# ----------------------------------------------------------------------
@login_bp.route('/reminders', methods=['GET', 'POST']) # 👈 CHANGED ROUTE NAME to match HTML link
def reminders_settings():
    if not session.get('loggedin'):
        return redirect(url_for('login_bp.login'))
        
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        water_status = True if request.form.get('water_reminder') == 'on' else False
        times_input = request.form.get('reminder_times').strip()
        
        # NOTE: Placeholder logic here for saving settings
        # You will need to implement a function like:
        # save_reminder_settings(user_id, water_status, times_input) 
        
        flash('Reminder settings successfully updated.', 'success')
        return redirect(url_for('login_bp.profile'))

    settings = fetch_intake_reminders(user_id) 
    
    return render_template('reminders_page.html', settings=settings)
# ----------------------------------------------------------------------
@login_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not session.get('loggedin'):
        return redirect(url_for('login_bp.login'))
        
    if request.method == 'POST':
        # Placeholder logic to process password change form submission goes here
        flash('Password change feature coming soon!', 'info')
        return redirect(url_for('login_bp.profile'))
        
    # In a real app, you would render a change_password.html template here.
    # For now, let's just redirect back or render a simple message to prevent the build error.
    
    # Since you haven't created a change_password.html yet, we will redirect 
    # the user back to the profile page with a message.
    flash('Change Password Page: Use this page to update your credentials!', 'info')
    return redirect(url_for('login_bp.profile'))


@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_bp.login'))

# --- LANGUAGE SETTER ROUTE ---
@login_bp.route('/set_language/<lang>')
def set_language(lang):
    # This checks if the user is logged in before setting a preference
    if not session.get('loggedin'):
        return redirect(url_for('login_bp.login'))

    # Store the selected language code (e.g., 'hi', 'kn') in the user's session
    session['language'] = lang
    
    # Redirect the user back to the page they were just on to apply the new translation
    # request.referrer holds the URL of the last page visited.
    return redirect(request.referrer or url_for('login_bp.profile'))
# ------------------------------