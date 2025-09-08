# TODO: Implement New Page for Child Type Data with Back Button

## Steps to Complete

- [x] Create new file: view/Child/child_type_data_ui.py
  - Implemented show_child_type_data_page function
  - Handles page cleaning and navigation
  - Displays child's basic info and type-specific data (full day or sessions)
  - Adds back button to return to children table

- [x] Modify view/Child/child_ui.py
  - Updated view_child_type_data function to call new page instead of dialog
  - Imported the new show_child_type_data_page function

- [x] Test the new page navigation
  - Verified back button returns to children table
  - Ensured data displays correctly for both child types
