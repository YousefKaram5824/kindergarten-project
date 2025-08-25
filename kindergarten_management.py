import hashlib
import secrets
import json
import os

class User:
    def __init__(self, username, hashed_password, role="admin"):
        self.username = username
        self.hashed_password = hashed_password
        self.role = role

class Student:
    def __init__(self, name, age, birth_date, phone, parent_job):
        self.name = name
        self.age = age
        self.birth_date = birth_date
        self.phone = phone
        self.parent_job = parent_job

class Parent:
    def __init__(self, name, job):
        self.name = name
        self.job = job

class FinancialRecord:
    def __init__(self, student_name, monthly_fee, bus_fee):
        self.student_name = student_name
        self.monthly_fee = monthly_fee
        self.bus_fee = bus_fee

class InventoryItem:
    def __init__(self, item_name, quantity, purchase_price):
        self.item_name = item_name
        self.quantity = quantity
        self.purchase_price = purchase_price

# Authentication utilities
class AuthManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()
        
    def hash_password(self, password, salt=None):
        """Hash password with salt using SHA256"""
        if salt is None:
            salt = secrets.token_hex(16)
        salted_password = salt + password
        hashed = hashlib.sha256(salted_password.encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def verify_password(self, stored_password, provided_password):
        """Verify provided password against stored hash"""
        try:
            salt, stored_hash = stored_password.split('$')
            salted_password = salt + provided_password
            provided_hash = hashlib.sha256(salted_password.encode()).hexdigest()
            return provided_hash == stored_hash
        except:
            return False
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    return {user_data['username']: User(**user_data) for user_data in users_data}
            except:
                return {}
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        users_data = [
            {
                'username': user.username,
                'hashed_password': user.hashed_password,
                'role': user.role
            }
            for user in self.users.values()
        ]
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def create_user(self, username, password, role="admin"):
        """Create a new user"""
        if username in self.users:
            return False, "اسم المستخدم موجود مسبقاً"
        
        hashed_password = self.hash_password(password)
        self.users[username] = User(username, hashed_password, role)
        self.save_users()
        return True, "تم إنشاء المستخدم بنجاح"
    
    def authenticate(self, username, password):
        """Authenticate user credentials"""
        user = self.users.get(username)
        if user and self.verify_password(user.hashed_password, password):
            return True, user
        return False, "اسم المستخدم أو كلمة المرور غير صحيحة"
    
    def initialize_default_admin(self):
        """Create default admin user if no users exist"""
        if not self.users:
            success, message = self.create_user("admin", "admin123", "admin")
            return success, message
        return True, "المستخدمون موجودون بالفعل"

# Global auth manager instance
auth_manager = AuthManager()
