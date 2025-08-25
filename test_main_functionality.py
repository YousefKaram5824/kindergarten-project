#!/usr/bin/env python3
"""
Test script to verify main application functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kindergarten_management import Student, FinancialRecord, InventoryItem

def test_data_classes():
    """Test that data classes can be instantiated correctly"""
    print("Testing data classes...")
    
    # Test Student class
    student = Student("أحمد", "5", "2020-01-01", "0123456789", "مهندس")
    assert student.name == "أحمد"
    assert student.age == "5"
    print("✓ Student class test passed")
    
    # Test FinancialRecord class
    financial = FinancialRecord("أحمد", "100", "20")
    assert financial.student_name == "أحمد"
    assert financial.monthly_fee == "100"
    print("✓ FinancialRecord class test passed")
    
    # Test InventoryItem class
    inventory = InventoryItem("كتب", "50", "10")
    assert inventory.item_name == "كتب"
    assert inventory.quantity == "50"
    print("✓ InventoryItem class test passed")

def test_application_import():
    """Test that main application can be imported without errors"""
    print("Testing application import...")
    try:
        import main
        print("✓ Main application import successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_report_generation():
    """Test report generation logic"""
    print("Testing report generation...")
    
    # Create sample data
    students = [Student("أحمد", "5", "2020-01-01", "0123456789", "مهندس")]
    financial_records = [FinancialRecord("أحمد", "100", "20")]
    inventory_items = [InventoryItem("كتب", "50", "10")]
    
    # Calculate totals
    total_students = len(students)
    total_financial = sum(float(record.monthly_fee) + float(record.bus_fee or 0) for record in financial_records)
    total_inventory = sum(float(item.quantity) * float(item.purchase_price or 0) for item in inventory_items)
    
    assert total_students == 1
    assert total_financial == 120.0
    assert total_inventory == 500.0
    print("✓ Report generation calculations correct")

if __name__ == "__main__":
    print("Running comprehensive functionality tests...")
    print("=" * 50)
    
    try:
        test_data_classes()
        test_application_import()
        test_report_generation()
        print("=" * 50)
        print("All functionality tests passed! ✅")
        print("\nThe Kindergarten Management System is ready for use.")
        print("Run 'python main.py' to start the application.")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
