# TODO: Extract Editing Feature from inventory_ui.py

## Completed Tasks
- [x] Created new file `view/edit_tool_dialog.py` with the extracted editing feature
- [x] Moved edit dialog UI components (text fields, dialog) to the new file
- [x] Moved edit dialog functions (open_edit_dialog, close_edit_dialog, update_inventory_item) to the new file
- [x] Added import for `create_edit_tool_dialog` in `view/inventory_ui.py`
- [x] Created instance of edit dialog in `inventory_ui.py` using `create_edit_tool_dialog(page, update_current_table)`
- [x] Removed old edit dialog code from `view/inventory_ui.py`
- [x] Ensured `open_edit_dialog` is still accessible for the edit button in the table
- [x] Created `view/edit_book_dialog.py` for editing books
- [x] Created `view/edit_uniform_dialog.py` for editing uniforms
- [x] Added imports for new edit dialogs in `inventory_ui.py`
- [x] Created instances of edit dialogs for books and uniforms
- [x] Added `confirm_delete_book` and `confirm_delete_uniform` functions
- [x] Updated `update_all_table` to show edit/delete buttons for books and uniforms in their respective categories and in "all" view

## Followup Steps
- [ ] Test the editing and deletion features for books and uniforms to ensure they work correctly
- [ ] Verify that the edit dialogs open with correct data populated
- [ ] Confirm that updates and deletions are successful and reflected in the table
- [ ] Check for any import or runtime errors in the updated code
