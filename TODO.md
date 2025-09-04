# TODO: Update Dashboard Inventory Count

# TODO: Add Users Count Container for Admins

## Tasks
- [x] Import additional inventory services in view/dashboard_ui.py
- [x] Modify update_dashboard_stats function to count all inventory items
- [ ] Test the dashboard to verify the total count displays correctly
- [x] Import UserService in view/dashboard_ui.py
- [x] Add conditional users stats card for admin users
- [x] Modify update_dashboard_stats to include users count for admins

## Details
- Current: Only counts ToolForSale items
- Target: Count TrainingTool, ToolForSale, UniformForSale, BookForSale
- File to edit: view/dashboard_ui.py
- Show users count only if current_user.role == 'admin'
- Add new stats card with icon and count
