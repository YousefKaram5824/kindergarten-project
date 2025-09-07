import datetime
import flet as ft

# Local imports
from database import get_db, db_session
from DTOs.daily_visit_dto import CreateDailyVisitDTO
from logic.daily_visit_logic import DailyVisitService
from logic.child_logic import ChildService

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


def create_daily_visit_tab(page: ft.Page, current_user=None):
    """Create and return the daily visit tab"""

    # Search field for filtering visits
    def on_search_change(e):
        update_visit_table(search_field.value or "")

    search_field = ft.TextField(
        label="بحث",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        hint_text="ابحث بالاسم، الميعاد، الغرض، أو الملاحظات",
        on_change=on_search_change,
        suffix_icon=ft.Icons.SEARCH,
    )

    # Visit table with database integration
    visit_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("اسم الطفل")),
            ft.DataColumn(ft.Text("الميعاد")),
            ft.DataColumn(ft.Text("التاريخ")),
            ft.DataColumn(ft.Text("الغرض")),
            ft.DataColumn(ft.Text("ملاحظات إضافية")),
            ft.DataColumn(ft.Text("القيمة")),
            ft.DataColumn(ft.Text("الإجراءات")),
        ],
        rows=[],
        border=ft.border.all(1, TABLE_BORDER_COLOR),
        border_radius=ft.border_radius.all(BORDER_RADIUS),
        vertical_lines=ft.border.BorderSide(1, TABLE_BORDER_COLOR),
        horizontal_lines=ft.border.BorderSide(1, TABLE_BORDER_COLOR),
        heading_row_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK12),
        heading_row_height=45,
        data_row_max_height=55,
        column_spacing=20,
    )

    def update_visit_table(search_query: str = ""):
        # Get visits from database using DailyVisitService
        with db_session() as db:
            visits_dto = DailyVisitService.get_all_visits(db)

            # Get all children for name lookup
            children_dto = ChildService.get_all_children(db)
            child_dict = {child.id: child.name for child in children_dto}

            if visit_data_table.rows is None:
                visit_data_table.rows = []
            else:
                visit_data_table.rows.clear()

            for visit in visits_dto:
                child_name = child_dict.get(visit.child_id, "غير معروف")

                # Filter by search query if provided
                if search_query:
                    search_lower = search_query.lower()
                    if not (
                        search_lower in child_name.lower() or
                        (visit.appointment and search_lower in visit.appointment.lower()) or
                        (visit.purpose and search_lower in visit.purpose.lower()) or
                        (visit.notes and search_lower in visit.notes.lower())
                    ):
                        continue

                # Create action icons for each visit
                action_icons = ft.Row(
                    [
                        # Edit icon
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.ORANGE,
                            tooltip="تعديل",
                            on_click=lambda e, visit_id=visit.id: edit_visit(
                                visit_id
                            ),
                        ),
                        # Delete icon
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="حذف",
                            on_click=lambda e, visit_id=visit.id: delete_visit(
                                visit_id
                            ),
                        ),
                    ],
                    spacing=5,
                )

                visit_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(child_name)),
                            ft.DataCell(ft.Text(visit.appointment or "-")),
                            ft.DataCell(ft.Text(visit.date.strftime("%Y-%m-%d") if visit.date else "-")),
                            ft.DataCell(ft.Text(visit.purpose or "-")),
                            ft.DataCell(ft.Text(visit.notes or "-")),
                            ft.DataCell(ft.Text(str(visit.value) if visit.value else "-")),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
            page.update()

    current_edit_visit_id = None

    def edit_visit(visit_id):
        """Edit visit details"""
        nonlocal current_edit_visit_id
        with db_session() as db:
            visit = DailyVisitService.get_visit(db, visit_id)
            if visit:
                current_edit_visit_id = visit_id
                # Populate edit form with visit data
                edit_child_dropdown.value = str(visit.child_id)
                edit_appointment.value = visit.appointment or ""
                edit_date.value = visit.date.strftime("%Y-%m-%d") if visit.date else ""
                edit_selected_date = visit.date if visit.date else None
                edit_purpose.value = visit.purpose or ""
                edit_notes.value = visit.notes or ""
                edit_value.value = str(visit.value) if visit.value else ""

                # Open edit dialog
                page.open(edit_visit_dialog)

    def delete_visit(visit_id):
        """Delete visit"""
        with db_session() as db:
            visit = DailyVisitService.get_visit(db, visit_id)
            if visit:
                # Get child name for confirmation
                child = ChildService.get_child_by_id(db, visit.child_id)
                child_name = child.name if child else "غير معروف"

                # Show confirmation dialog
                def confirm_delete(e):
                    try:
                        success = DailyVisitService.delete_visit(db, visit_id)
                        if success:
                            update_visit_table()
                            snackbar = ft.SnackBar(
                                content=ft.Text(f"تم حذف الزيارة للطفل: {child_name}"),
                                bgcolor=ft.Colors.GREEN,
                                duration=3000,
                            )
                        else:
                            snackbar = ft.SnackBar(
                                content=ft.Text("فشل في حذف الزيارة"),
                                bgcolor=ft.Colors.RED,
                                duration=3000,
                            )
                        page.overlay.append(snackbar)
                        page.update()
                        snackbar.open = True
                        snackbar.update()
                        page.update()
                        page.close(dialog)
                    except Exception as ex:
                        snackbar = ft.SnackBar(
                            content=ft.Text(f"خطأ في الحذف: {str(ex)}"),
                            bgcolor=ft.Colors.RED,
                            duration=3000,
                        )
                        page.overlay.append(snackbar)
                        page.update()
                        snackbar.open = True
                        snackbar.update()
                        page.update()

                def cancel_delete(e):
                    page.close(dialog)

                dialog = ft.AlertDialog(
                    title=ft.Text("تأكيد الحذف"),
                    content=ft.Text(f"هل تريد حذف زيارة الطفل {child_name}؟"),
                    actions=[
                        ft.TextButton("نعم", on_click=confirm_delete),
                        ft.TextButton("لا", on_click=cancel_delete),
                    ],
                )
                page.open(dialog)

    # Form fields for add visit
    child_dropdown = ft.Dropdown(
        label="اسم الطفل",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        options=[],  # Will be populated
    )

    appointment = ft.TextField(
        label="الميعاد",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )
    selected_time = None

    def handle_time_picker(e):

        if e.control.value:
            selected_time = e.control.value
            appointment.value = selected_time.strftime("%H:%M")
            page.update()

    def open_time_picker(e):
        page.open(time_picker)

    time_picker_btn = ft.ElevatedButton("اختر الوقت", on_click=open_time_picker)

    # Time picker for appointment
    time_picker = ft.TimePicker(
        on_change=handle_time_picker,
    )
    page.overlay.append(time_picker)

    date = ft.TextField(
        label="التاريخ",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )
    selected_date = None

    purpose = ft.TextField(
        label="الغرض",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    notes = ft.TextField(
        label="ملاحظات إضافية",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    def on_value_change(e):
        if value.value:
            egp_text.visible = True
        else:
            egp_text.visible = False
        page.update()

    egp_text = ft.Text("EGP", visible=False, size=14, weight=ft.FontWeight.BOLD)

    value = ft.TextField(
        label="القيمة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]*", replacement_string=""
        ),
        suffix=egp_text,
        
    )

    def handle_date_picker(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            date.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    # Add Visit Dialog
    add_visit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة زيارة جديدة", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                child_dropdown,
                ft.Row(
                    [time_picker_btn, appointment],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [date_picker_btn, date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                purpose,
                notes,
                value,
            ],
            width=400,
            height=400,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_visit()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Date picker for visit date
    date_picker = ft.DatePicker(
        on_change=handle_date_picker,
        first_date=datetime.datetime(2020, 1, 1),
        last_date=datetime.datetime.now() + datetime.timedelta(days=365),
    )
    page.overlay.append(date_picker)

    # Edit form fields (similar to add form)
    edit_child_dropdown = ft.Dropdown(
        label="اسم الطفل",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        options=[],  # Will be populated
    )

    edit_appointment = ft.TextField(
        label="الميعاد",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    edit_date = ft.TextField(
        label="التاريخ",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )
    edit_selected_date = None

    edit_purpose = ft.TextField(
        label="الغرض",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    edit_notes = ft.TextField(
        label="ملاحظات إضافية",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    edit_value = ft.TextField(
        label="القيمة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]*", replacement_string=""
        ),
    )

    def edit_handle_date_picker(e):
        nonlocal edit_selected_date
        if e.control.value:
            edit_selected_date = e.control.value
            edit_date.value = edit_selected_date.strftime("%Y-%m-%d")
            page.update()

    def edit_open_date_picker(e):
        page.open(edit_date_picker)

    edit_date_picker_btn = ft.ElevatedButton(
        "اختر التاريخ", on_click=edit_open_date_picker
    )

    # Edit Visit Dialog
    edit_visit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تعديل بيانات الزيارة", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                edit_child_dropdown,
                edit_appointment,
                ft.Row(
                    [edit_date_picker_btn, edit_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                edit_purpose,
                edit_notes,
                edit_value,
            ],
            width=400,
            height=400,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: close_edit_dialog()),
            ft.TextButton("حفظ", on_click=lambda e: save_edit_visit()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Edit Date picker
    edit_date_picker = ft.DatePicker(
        on_change=edit_handle_date_picker,
        first_date=datetime.datetime(2020, 1, 1),
        last_date=datetime.datetime.now() + datetime.timedelta(days=365),
    )
    page.overlay.append(edit_date_picker)

    def populate_child_dropdowns():
        """Populate child dropdowns with current children"""
        with db_session() as db:
            children = ChildService.get_all_children(db)
            options = [
                ft.dropdown.Option(key=str(child.id), text=child.name)
                for child in children
            ]
            child_dropdown.options = options
            edit_child_dropdown.options = options
            page.update()

    def save_edit_visit():
        nonlocal current_edit_visit_id
        if not current_edit_visit_id:
            show_error("لم يتم العثور على الزيارة المراد تعديلها!")
            return

        # Validate required fields
        if not edit_child_dropdown.value:
            show_error("يجب اختيار الطفل!")
            return

        if not edit_date.value:
            show_error("يجب اختيار التاريخ!")
            return

        # Create visit DTO with updated data
        visit_data = CreateDailyVisitDTO(
            child_id=int(edit_child_dropdown.value),
            appointment=edit_appointment.value if edit_appointment.value else None,
            date=datetime.datetime.strptime(edit_date.value, "%Y-%m-%d").date(),
            purpose=edit_purpose.value if edit_purpose.value else None,
            notes=edit_notes.value if edit_notes.value else None,
            value=float(edit_value.value) if edit_value.value else None,
        )

        # Update visit in database using DailyVisitService
        with db_session() as db:
            try:
                visit_dto = DailyVisitService.update_visit(
                    db, current_edit_visit_id, visit_data
                )

                if visit_dto:
                    # Close dialog and refresh table
                    close_edit_dialog()
                    update_visit_table()
                    show_success("تم تعديل بيانات الزيارة بنجاح!")
                else:
                    show_error("فشل في تعديل بيانات الزيارة!")
            except Exception as ex:
                show_error(f"خطأ في تعديل بيانات الزيارة: {str(ex)}")

    def close_edit_dialog():
        page.close(edit_visit_dialog)

    def add_visit():
        # Validate required fields
        if not child_dropdown.value:
            show_error("يجب اختيار الطفل!")
            return

        if not date.value:
            show_error("يجب اختيار التاريخ!")
            return

        # Create visit DTO
        visit_data = CreateDailyVisitDTO(
            child_id=int(child_dropdown.value),
            appointment=appointment.value if appointment.value else None,
            date=datetime.datetime.strptime(date.value, "%Y-%m-%d").date(),
            purpose=purpose.value if purpose.value else None,
            notes=notes.value if notes.value else None,
            value=float(value.value) if value.value else None,
        )

        # Add visit to database using DailyVisitService
        with db_session() as db:
            try:
                visit_dto = DailyVisitService.create_visit(db, visit_data)

                if visit_dto:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Refresh visit table
                    update_visit_table()

                    show_success("تم إضافة الزيارة بنجاح!")
                else:
                    show_error("فشل في إضافة الزيارة!")
            except Exception as ex:
                show_error(f"خطأ في إضافة الزيارة: {str(ex)}")

    def show_error(message):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED,
            duration=3000,
        )
        page.overlay.append(snackbar)
        page.update()
        snackbar.open = True
        snackbar.update()
        page.update()

    def show_success(message):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.GREEN,
            duration=3000,
        )
        page.overlay.append(snackbar)
        page.update()
        snackbar.open = True
        snackbar.update()
        page.update()

    def reset_form():
        nonlocal selected_date, selected_time
        child_dropdown.value = ""
        appointment.value = ""
        date.value = ""
        selected_date = None
        selected_time = None
        purpose.value = ""
        notes.value = ""
        value.value = ""

    def open_add_visit_dialog(e):
        populate_child_dropdowns()
        page.open(add_visit_dialog)

    def close_dialog():
        page.close(add_visit_dialog)

    # Add Visit button
    add_visit_btn = ft.ElevatedButton(
        "إضافة زيارة جديدة", icon=ft.Icons.ADD, on_click=open_add_visit_dialog
    )

    # Load initial visit data
    populate_child_dropdowns()
    update_visit_table()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("إدارة الزيارات اليومية", size=24, weight=ft.FontWeight.BOLD),
                    add_visit_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Row(
                [
                    search_field,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Text("الزيارات المسجلة:", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([visit_data_table], scroll=ft.ScrollMode.AUTO),
                height=500,
                padding=10,
                alignment=ft.alignment.center,
                margin=10,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
