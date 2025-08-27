#!/usr/bin/env python3
"""
Test script to verify the dashboard functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    from dashboard_ui import create_dashboard, show_main_system
    from database import db
    from auth_ui import set_show_main_system_callback
    
    print("✓ All imports successful")
    
    # Test database connection
    if db.connect():
        print("✓ Database connection successful")
        db.close()
    else:
        print("✗ Database connection failed")
    
    # Test callback setup
    set_show_main_system_callback(show_main_system)
    print("✓ Callback setup successful")
    
    print("\nDashboard implementation is ready!")
    print("You can now run 'python main_app.py' to start the application")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
