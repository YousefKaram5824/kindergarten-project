import sqlite3

def check_children_schema():
    conn = sqlite3.connect("kindergarten.db")
    cursor = conn.cursor()
    
    # Check if children table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Children table does not exist!")
        return
    
    # Get table schema
    cursor.execute("PRAGMA table_info(children)")
    columns = cursor.fetchall()
    
    print("Children table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    check_children_schema()
