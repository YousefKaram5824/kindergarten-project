#!/usr/bin/env python3
import datetime

# Get the current time from the system clock
current_time = datetime.datetime.now()

# Assign it to a created_at variable
created_at = current_time

# Display the result
print(f"Current time: {current_time}")
print(f"Created at variable: {created_at}")

# If you want to format it as a string (similar to how it's stored in the database)
created_at_str = created_at.isoformat()
print(f"Created at (ISO format): {created_at_str}")

# If you want to format it in a more readable way
created_at_formatted = created_at.strftime("%Y-%m-%d %H:%M:%S")
print(f"Created at (formatted): {created_at_formatted}")
