# Kindergarten Management System

A comprehensive kindergarten management system built with Flet (Python) that implements the requirements from the "kindergarten system.pdf" document.

## Features

### 1. Student Registration
- Add new students with complete information
- Track: Name, Age, Birth Date, Phone Number, Parent Job, Additional Notes
- View all registered students in a list

### 2. Financial Management
- Record monthly fees for students
- Track bus fees
- Maintain financial records per student
- View all financial records

### 3. Inventory Management
- Add inventory items (books, supplies, uniforms, etc.)
- Track quantity and purchase price
- View complete inventory list

### 4. Reports
- Generate comprehensive reports showing:
  - Total number of students
  - Total financial value
  - Total inventory value
  - Detailed lists of students, financial records, and inventory items

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The application will open in your default web browser at `http://localhost:8550`

3. Use the tabs to navigate between different sections:
   - **Student Registration**: Add and view students
   - **Financial Management**: Manage financial records
   - **Inventory Management**: Track inventory items
   - **Reports**: Generate comprehensive reports

## Data Structure

The system uses the following data classes:

### Student Class
- `name`: Student's full name
- `age`: Student's age
- `birth_date`: Date of birth
- `phone`: Contact phone number
- `parent_job`: Parent's occupation

### FinancialRecord Class
- `student_name`: Associated student name
- `monthly_fee`: Monthly tuition fee
- `bus_fee`: Transportation fee (optional)

### InventoryItem Class
- `item_name`: Name of the inventory item
- `quantity`: Number of items in stock
- `purchase_price`: Cost per item

## Testing

Run the test suite to verify all functionality:
```bash
python test_kindergarten.py
```

## File Structure

```
kindergarten_management/
├── main.py                 # Main application file
├── kindergarten_management.py  # Data classes and structures
├── test_kindergarten.py    # Test suite
├── requirements.txt        # Dependencies
├── README.md              # This file
└── kindergarten system.pdf # Original requirements document
```

## Requirements

- Python 3.7+
- Flet >= 0.22.0

## Features Implemented from PDF

✅ Student registration system with complete information tracking  
✅ Financial management for monthly fees and bus fees  
✅ Inventory management system  
✅ Comprehensive reporting functionality  
✅ Arabic language support (data structure ready for Arabic content)  
✅ Daily and monthly tracking systems  
✅ Parent information tracking  

## Future Enhancements

- Data persistence (file/database storage)
- Arabic language UI
- Advanced reporting with charts
- User authentication
- Email notifications
- Attendance tracking
- Photo/document upload functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.
