import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

class KindergartenDatabase:
    def __init__(self, db_path: str = "kindergarten.db"):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Establish connection to the database"""
        if not os.path.exists(self.db_path):
            print(f"Database file {self.db_path} not found.")
            return False
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
            
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            
    def initialize_database(self):
        """Initialize the database with all required tables"""
        if not self.connect():
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Create Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create Students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    birth_date TEXT NOT NULL,
                    phone TEXT,
                    dad_job TEXT,
                    mum_job TEXT,
                    problem TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create Parents table (linked to students)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    job TEXT,
                    relationship TEXT NOT NULL, -- 'father' or 'mother'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
                )
            ''')
            
            # Create Financial Records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financial_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    monthly_fee DECIMAL(10, 2) NOT NULL,
                    bus_fee DECIMAL(10, 2) DEFAULT 0,
                    month_year TEXT NOT NULL, -- Format: YYYY-MM
                    paid BOOLEAN DEFAULT FALSE,
                    payment_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
                )
            ''')
            
            # Create Inventory table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    purchase_price DECIMAL(10, 2) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.connection.commit()
            print("Database initialized successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            return False
        finally:
            self.close()
            
    def migrate_users_from_json(self, json_file_path: str = "users.json"):
        """Migrate users from JSON file to database"""
        if not os.path.exists(json_file_path):
            print(f"JSON file {json_file_path} not found")
            return False
            
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                
            if not self.connect():
                return False
                
            cursor = self.connection.cursor()
            
            for user_data in users_data:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (username, hashed_password, role)
                    VALUES (?, ?, ?)
                ''', (user_data['username'], user_data['hashed_password'], user_data['role']))
                
            self.connection.commit()
            print(f"Migrated {len(users_data)} users from JSON to database")
            return True
            
        except Exception as e:
            print(f"Migration error: {e}")
            return False
        finally:
            self.close()
            
    # User operations
    def create_user(self, username: str, hashed_password: str, role: str = "user") -> bool:
        """Create a new user"""
        try:
            if not self.connect():
                return False
                
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO users (username, hashed_password, role)
                VALUES (?, ?, ?)
            ''', (username, hashed_password, role))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error:
            return False
        finally:
            self.close()
            
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            if not self.connect():
                return None
                
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user:
                return dict(user)
            return None
            
        except sqlite3.Error:
            return None
        finally:
            self.close()
            
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        try:
            if not self.connect():
                return []
                
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users ORDER BY username')
            users = cursor.fetchall()
            
            return [dict(user) for user in users]
            
        except sqlite3.Error:
            return []
        finally:
            self.close()
            
    # Student operations
    def create_student(self, name: str, age: int, birth_date: str, phone: str, 
                        dad_job: str, mum_job: str, problem: str) -> int:
        """Create a new student and return student ID"""
        try:
            if not self.connect():
                return -1
                
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO students (name, age, birth_date, phone, dad_job, mum_job, problem)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, age, birth_date, phone, dad_job, mum_job, problem))
            
            student_id = cursor.lastrowid
            self.connection.commit()
            return student_id
            
        except sqlite3.Error:
            return -1
        finally:
            self.close()
            
    def get_all_students(self) -> List[Dict[str, Any]]:
        """Get all students"""
        try:
            if not self.connect():
                return []
                
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM students ORDER BY name')
            students = cursor.fetchall()
            
            return [dict(student) for student in students]
            
        except sqlite3.Error:
            return []
        finally:
            self.close()
            
    # Parent operations
    def add_parent(self, student_id: int, name: str, job: str, relationship: str) -> bool:
        """Add a parent for a student"""
        try:
            if not self.connect():
                return False
                
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO parents (student_id, name, job, relationship)
                VALUES (?, ?, ?, ?)
            ''', (student_id, name, job, relationship))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error:
            return False
        finally:
            self.close()
            
    # Financial operations
    def add_financial_record(self, student_id: int, monthly_fee: float, 
                            bus_fee: float, month_year: str) -> bool:
        """Add financial record for a student"""
        try:
            if not self.connect():
                return False
                
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO financial_records (student_id, monthly_fee, bus_fee, month_year)
                VALUES (?, ?, ?, ?)
            ''', (student_id, monthly_fee, bus_fee, month_year))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error:
            return False
        finally:
            self.close()
            
    # Inventory operations
    def add_inventory_item(self, item_name: str, quantity: int, 
                            purchase_price: float, description: str) -> bool:
        """Add inventory item"""
        try:
            if not self.connect():
                return False
                
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO inventory (item_name, quantity, purchase_price, description)
                VALUES (?, ?, ?, ?)
            ''', (item_name, quantity, purchase_price, description))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error:
            return False
        finally:
            self.close()
            
    def get_all_inventory(self) -> List[Dict[str, Any]]:
        """Get all inventory items"""
        try:
            if not self.connect():
                return []
                
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM inventory ORDER BY item_name')
            items = cursor.fetchall()
            
            return [dict(item) for item in items]
            
        except sqlite3.Error:
            return []
        finally:
            self.close()

# Global database instance
db = KindergartenDatabase()

def initialize_database():
    """Initialize the database and migrate existing data"""
    if db.initialize_database():
        db.migrate_users_from_json()
        return True
    return False

if __name__ == "__main__":
    # Test the database initialization
    if initialize_database():
        print("Database setup completed successfully!")
        
        # Test getting users
        db.connect()
        users = db.get_all_users()
        print(f"Found {len(users)} users in database")
        
        # Test getting inventory (should be empty initially)
        inventory = db.get_all_inventory()
        print(f"Found {len(inventory)} inventory items")
        
        db.close()
    else:
        print("Database setup failed!")
