# user_metrics.py

import pymysql
# Import your connection function
from db_insert import get_db_connection 

def insert_progress_log(user_id, weight, sleep_duration):
    """
    Saves a user's latest weight and sleep duration into the user_progress table.
    Returns True on success.
    """
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        
        # NOTE: Inserts weight and sleep, along with the current date (CURDATE())
        query = """
        INSERT INTO user_progress 
        (user_id, weight, sleep_duration, date_logged)
        VALUES (%s, %s, %s, CURDATE())
        """
        values = (user_id, weight, sleep_duration)

        cursor.execute(query, values)
        conn.commit()
        print(f"Progress logged for user {user_id}: {weight}kg, {sleep_duration}hrs.")
        return True

    except pymysql.Error as err:
        print(f">>> DB Error logging progress: {err}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.open: conn.close()


def fetch_full_progress_history(user_id):
    """
    Retrieves ALL weight and sleep log entries for a user, 
    including the entry ID for editing/deleting.
    """
    conn = get_db_connection()
    if not conn: return []

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT id, date_logged, weight, sleep_duration 
            FROM user_progress 
            WHERE user_id = %s 
            ORDER BY date_logged DESC;
        """
        cursor.execute(query, (user_id,))
        # Fetching all records for the history page
        return cursor.fetchall()
    except pymysql.Error as err:
        print(f"Error fetching full progress history: {err}")
        return []
    finally:
        if conn and conn.open: conn.close()


# ----------------------------------------------------------------------
# ✅ NEW FUNCTION: FETCH SINGLE ENTRY FOR EDITING
# ----------------------------------------------------------------------
def fetch_single_progress_entry(entry_id, user_id):
    """
    Fetches a single progress entry by its ID, ensuring user ownership.
    """
    conn = get_db_connection()
    if not conn: return None
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT id, weight, sleep_duration, date_logged 
            FROM user_progress 
            WHERE id = %s AND user_id = %s;
        """
        cursor.execute(query, (entry_id, user_id))
        return cursor.fetchone()
    except pymysql.Error as err:
        print(f">>> DB Error fetching single progress entry: {err}")
        return None
    finally:
        if conn and conn.open: conn.close()
        
        
# ----------------------------------------------------------------------
# ✅ NEW FUNCTION: UPDATE EXISTING ENTRY
# ----------------------------------------------------------------------
def update_progress_entry(entry_id, user_id, new_weight, new_sleep):
    """
    Updates an existing progress entry in the database.
    Returns True if a row was updated, False otherwise.
    """
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            UPDATE user_progress 
            SET weight = %s, sleep_duration = %s
            WHERE id = %s AND user_id = %s;
        """
        # Note the order of parameters: new_weight, new_sleep, entry_id, user_id
        values = (new_weight, new_sleep, entry_id, user_id)
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount > 0
    except pymysql.Error as err:
        print(f">>> DB Error updating progress entry: {err}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.open: conn.close()