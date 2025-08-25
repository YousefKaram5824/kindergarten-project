import flet as ft
from kindergarten_management import Student, FinancialRecord, InventoryItem

def test_student_creation():
    """Test student creation functionality"""
    student = Student("John Doe", "5", "2020-01-01", "123-456-7890", "Engineer")
    assert student.name == "John Doe"
    assert student.age == "5"
    assert student.birth_date == "2020-01-01"
    assert student.phone == "123-456-7890"
    assert student.parent_job == "Engineer"
    print("✓ Student creation test passed")

def test_financial_record_creation():
    """Test financial record creation functionality"""
    record = FinancialRecord("John Doe", "100", "20")
    assert record.student_name == "John Doe"
    assert record.monthly_fee == "100"
    assert record.bus_fee == "20"
    print("✓ Financial record creation test passed")

def test_inventory_item_creation():
    """Test inventory item creation functionality"""
    item = InventoryItem("Books", "50", "10")
    assert item.item_name == "Books"
    assert item.quantity == "50"
    assert item.purchase_price == "10"
    print("✓ Inventory item creation test passed")

def test_data_structures():
    """Test all data structures together"""
    students = []
    financial_records = []
    inventory_items = []
    
    # Add sample data
    students.append(Student("Alice", "4", "2021-03-15", "555-1234", "Teacher"))
    financial_records.append(FinancialRecord("Alice", "120", "25"))
    inventory_items.append(InventoryItem("Crayons", "100", "5"))
    
    # Verify data
    assert len(students) == 1
    assert len(financial_records) == 1
    assert len(inventory_items) == 1
    assert students[0].name == "Alice"
    assert financial_records[0].student_name == "Alice"
    assert inventory_items[0].item_name == "Crayons"
    print("✓ Data structures integration test passed")

if __name__ == "__main__":
    print("Running kindergarten management system tests...")
    test_student_creation()
    test_financial_record_creation()
    test_inventory_item_creation()
    test_data_structures()
    print("All tests passed! ✅")
