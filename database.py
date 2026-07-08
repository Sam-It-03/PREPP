import sqlite3
import json

# Unified database file for the whole app
DB_NAME = 'pune_app.db' 

def init_db():
    """Ensures all necessary tables exist before doing any operations"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Users table (For Registration/Login)
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
                 
    # 2. Session table (For the 'Remember Me' feature)
    c.execute('''CREATE TABLE IF NOT EXISTS session 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
                 
    # 3. Favorites table (Stores the property dictionaries as JSON strings)
    c.execute('''CREATE TABLE IF NOT EXISTS favorites 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, property_data TEXT)''')
                  
    conn.commit()
    conn.close()

# ==========================================
# 🔐 USER AUTHENTICATION
# ==========================================
def add_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        # Tries to insert the user. Will fail if username already exists (UNIQUE constraint)
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False 
    finally:
        conn.close()

def verify_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# ==========================================
# 💾 SESSION (REMEMBER ME)
# ==========================================
def set_remembered_user(username, password, remember_status):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM session') # Always clear old sessions
    if remember_status == "on":
        c.execute('INSERT INTO session (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def get_remembered_user():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT username, password FROM session LIMIT 1')
    row = c.fetchone()
    conn.close()
    return row

# ==========================================
# ⭐ FAVORITES MANAGEMENT
# ==========================================
def add_favorite(prop_dict):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    prop_str = json.dumps(prop_dict)
    c.execute('INSERT INTO favorites (property_data) VALUES (?)', (prop_str,))
    conn.commit()
    conn.close()

def remove_favorite(prop_id):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM favorites WHERE id=?', (prop_id,))
    conn.commit()
    conn.close()

def get_all_favorites():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, property_data FROM favorites')
    rows = c.fetchall()
    conn.close()
    
    saved = []
    for row in rows:
        prop = json.loads(row[1])
        prop['id'] = row[0] # Inject the DB row ID into the dictionary so we can delete it later
        saved.append(prop)
    return saved

def is_saved(prop_dict):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT property_data FROM favorites')
    rows = c.fetchall()
    conn.close()
    
    # Compare dictionaries (ignoring 'id' if it exists)
    check_dict = {k:v for k,v in prop_dict.items() if k != 'id'}
    
    for row in rows:
        db_dict = json.loads(row[0])
        if {k:v for k,v in db_dict.items() if k != 'id'} == check_dict:
            return True
    return False