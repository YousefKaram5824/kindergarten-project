# Student UI Age Control Updates

## Tasks to Complete:
- [x] Replace age text display with textbox input field
- [x] Replace text buttons with icon buttons (plus/minus icons)
- [x] Set initial age to 3 instead of 0
- [x] Update increment/decrement functions to work with text field
- [x] Add input validation for numeric values only
- [x] Ensure proper UI layout and styling

## Files to Modify:
- view/student_ui_new.py (primary)

## Changes Made:
- Changed `student_age` from `ft.Text` to `ft.TextField` with proper styling
- Replaced text buttons with `ft.IconButton` using `ft.icons.ADD` and `ft.icons.REMOVE`
- Set initial age to 3 in both variable and text field
- Updated `reset_form()` function to reset age to 3
- Added input filter to only allow numeric input
- Improved UI styling with proper spacing and button styling
