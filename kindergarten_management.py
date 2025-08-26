import hashlib
import json
import os
import secrets

# Local imports
from database import db

class User:
    def __init__(self, username, hashed_password, role="admin"):
        self.username = username
        self.hashed_password = hashed_password
        self.role = role

class Student:
    def __init__(self, name, age, birth_date, phone, dad_job, mum_job):
        self.name = name
        self.age = age
        self.birth_date = birth_date
        self.phone = phone
        self.dad_job = dad_job
        self.mum_job = mum_job

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
        """Load users from database"""
        users_data = db.get_all_users()
        return {user_data['username']: User(user_data['username'], user_data['hashed_password'], user_data['role']) 
                for user_data in users_data}
    
    def create_user(self, username, password, role="admin"):
        """Create a new user in database"""
        if username in self.users:
            return False, "اسم المستخدم موجود مسبقاً"
        
        hashed_password = self.hash_password(password)
        success = db.create_user(username, hashed_password, role)
        if success:
            self.users[username] = User(username, hashed_password, role)
            return True, "تم إنشاء المستخدم بنجاح"
        return False, "فشل في إنشاء المستخدم"
    
    def authenticate(self, username, password):
        """Authenticate user credentials"""
        user_data = db.get_user(username)
        if user_data and self.verify_password(user_data['hashed_password'], password):
            user = User(user_data['username'], user_data['hashed_password'], user_data['role'])
            return True, user
        return False, "اسم المستخدم أو كلمة المرور غير صحيحة"
    
    def initialize_default_admin(self):
        """Create default admin user if no users exist"""
        users = db.get_all_users()
        if not users:
            success, message = self.create_user("admin", "admin123", "admin")
            return success, message
        return True, "المستخدمون موجودون بالفعل"
    
    def reset_password(self, username, new_password, admin_username, admin_password):
        """Reset user password with admin verification"""
        # Verify admin credentials first
        admin_auth, admin_msg = self.authenticate(admin_username, admin_password)
        if not admin_auth:
            return False, "كلمة مرور المدير غير صحيحة"
        
        # Check if admin user has admin role
        admin_user = self.users.get(admin_username)
        if not admin_user or admin_user.role != "admin":
            return False, "ليست لديك صلاحية لإعادة تعيين كلمات المرور"
        
        # Check if target user exists
        if username not in self.users:
            return False, "اسم المستخدم غير موجود"
        
        # Reset the password in database
        hashed_password = self.hash_password(new_password)
        # For now, we'll create a new user with updated password
        # In a real implementation, we'd have an update_user method in the database
        success = db.create_user(username, hashed_password, self.users[username].role)
        if success:
            self.users[username].hashed_password = hashed_password
            return True, "تم إعادة تعيين كلمة المرور بنجاح"
        return False, "فشل في إعادة تعيين كلمة المرور"
    
    def verify_admin(self, username, password):
        """Verify if user is an admin with correct credentials"""
        auth_result, user_or_msg = self.authenticate(username, password)
        if not auth_result:
            return False, "اسم المستخدم أو كلمة المرور غير صحيحة"
        
        # Check if user_or_msg is a User object (not an error message)
        if isinstance(user_or_msg, str):
            return False, user_or_msg
        
        if user_or_msg.role != "admin":
            return False, "ليست لديك صلاحية المدير"
        
        return True, "تم التحقق من هوية المدير بنجاح"

# Global auth manager instance
auth_manager = AuthManager()
