#!/usr/bin/env python3
"""
Test script to verify database integration with kindergarten management system
"""

from kindergarten_management import auth_manager

def test_user_authentication():
    """Test user authentication with database"""
    print("Testing user authentication...")
    
    # Test existing user authentication
    success, result = auth_manager.authenticate("admin", "admin123")
    if success:
        print("✓ Admin authentication successful")
        print(f"  User: {result.username}, Role: {result.role}")
    else:
        print(f"✗ Admin authentication failed: {result}")
    
    # Test non-existent user
    success, result = auth_manager.authenticate("nonexistent", "password")
    if not success:
        print("✓ Non-existent user correctly rejected")
    else:
        print("✗ Non-existent user incorrectly accepted")
    
    # Test wrong password
    success, result = auth_manager.authenticate("admin", "wrongpassword")
    if not success:
        print("✓ Wrong password correctly rejected")
    else:
        print("✗ Wrong password incorrectly accepted")

def test_user_creation():
    """Test creating a new user"""
    print("\nTesting user creation...")
    
    # Create a new test user
    success, message = auth_manager.create_user("testuser_db", "testpass123", "user")
    if success:
        print(f"✓ User creation successful: {message}")
        
        # Verify the new user can authenticate
        success, user = auth_manager.authenticate("testuser_db", "testpass123")
        if success:
            print("✓ New user authentication successful")
        else:
            print("✗ New user authentication failed")
    else:
        print(f"✗ User creation failed: {message}")

def test_user_loading():
    """Test loading users from database"""
    print("\nTesting user loading...")
    
    users = auth_manager.load_users()
    print(f"Loaded {len(users)} users from database")
    
    for username, user in users.items():
        print(f"  - {username}: {user.role}")

if __name__ == "__main__":
    print("Database Integration Test")
    print("=" * 40)
    
    test_user_authentication()
    test_user_creation()
    test_user_loading()
    
    print("\n" + "=" * 40)
    print("Test completed!")
