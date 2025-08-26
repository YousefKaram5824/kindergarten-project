# Kindergarten Management System Database Documentation

## Overview
The kindergarten management system now uses SQLite as its database backend, replacing the previous JSON-based storage system. This provides better data integrity, scalability, and performance.

## Database Structure

### Tables

#### 1. Users Table
Stores system users and their authentication information.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique user ID |
| username | TEXT UNIQUE NOT NULL | Username for login |
| hashed_password | TEXT NOT NULL | Hashed password with salt |
| role | TEXT NOT NULL DEFAULT 'user' | User role (admin/user) |
| created_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

#### 2. Students Table
Stores student information.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique student ID |
| name | TEXT NOT NULL | Student's full name |
| age | INTEGER NOT NULL | Student's age |
| birth_date | TEXT NOT NULL | Date of birth |
| phone | TEXT | Contact phone number |
| dad_job | TEXT | Father's occupation |
| mum_job | TEXT | Mother's occupation |
| created_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

#### 3. Parents Table
Stores parent information linked to students.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique parent ID |
| student_id | INTEGER NOT NULL | Foreign key to students table |
| name | TEXT NOT NULL | Parent's name |
| job | TEXT | Parent's occupation |
| relationship | TEXT NOT NULL | Relationship to student ('father'/'mother') |
| created_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

#### 4. Financial Records Table
Stores financial information for students.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique record ID |
| student_id | INTEGER NOT NULL | Foreign key to students table |
| monthly_fee | DECIMAL(10, 2) NOT NULL | Monthly tuition fee |
| bus_fee | DECIMAL(10, 2) DEFAULT 0 | Transportation fee |
| month_year | TEXT NOT NULL | Month and year (YYYY-MM format) |
| paid | BOOLEAN DEFAULT FALSE | Payment status |
| payment_date | TIMESTAMP | Date of payment |
| created_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

#### 5. Inventory Table
Stores inventory items.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique item ID |
| item_name | TEXT NOT NULL | Item name |
| quantity | INTEGER NOT NULL DEFAULT 0 | Quantity in stock |
| purchase_price | DECIMAL(10, 2) NOT NULL | Purchase price per unit |
| description | TEXT | Item description |
| created_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

## Database Operations

### Initialization
To initialize the database and migrate existing data:
```python
from database import initialize_database

if initialize_database():
    print("Database setup completed successfully!")
else:
    print("Database setup failed!")
```

### Common Operations

#### User Management
```python
from database import db

# Create a new user
db.create_user("username", "hashed_password", "role")

# Get user by username
user = db.get_user("username")

# Get all users
users = db.get_all_users()
```

#### Student Management
```python
# Create a new student
student_id = db.create_student("Name", 5, "2020-01-01", "123456789", "Engineer", "Teacher")

# Get all students
students = db.get_all_students()
```

#### Financial Records
```python
# Add financial record
db.add_financial_record(student_id, 500.00, 100.00, "2024-08")
```

#### Inventory Management
```python
# Add inventory item
db.add_inventory_item("Pencils", 100, 2.50, "Colored pencils for students")
```

## Migration Process
The system automatically migrates existing user data from `users.json` to the database during initialization. All new data will be stored in the SQLite database (`kindergarten.db`).

## Backup and Maintenance
- The database file (`kindergarten.db`) should be regularly backed up
- SQLite databases are portable and can be easily copied or moved
- Use SQLite browser tools for manual inspection and maintenance

## Performance Considerations
- SQLite provides ACID compliance and transaction support
- All database operations are optimized for performance
- The system uses connection pooling and proper resource management

## Security
- Passwords are hashed using SHA256 with salt
- Database connections are properly closed after each operation
- SQL injection protection is implemented through parameterized queries
