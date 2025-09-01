import datetime
import os
import shutil
import flet as ft
from sqlalchemy.orm import Session

# Local imports
from database import get_db, db_session
from DTOs.child_dto import CreateChildDTO
from logic.child_logic import ChildService

# Color constants
PAGE_BGCOLOR = "#E3DCCC"
INPUT_BGCOLOR = ft.colors.WHITE
INPUT_BORDER_COLOR = "#B58B18"  # Gold
BUTTON_BGCOLOR = "#B58B18"  # Gold
BUTTON_TEXT_COLOR = ft.colors.WHITE
TEXT_COLOR_GOLD = "#B58B18"  # Gold
TEXT_COLOR_DARK = "#262626"  # Slightly darker text for better contrast
TEXT_COLOR_TABLE_DATA = ft.colors.BLACK  # Explicitly black for table data cells
FONT_FAMILY_REGULAR = "Tajawal"
FONT_FAMILY_BOLD = "Tajawal-Bold"
BORDER_RADIUS = 8
TABLE_ROW_TEXT = TEXT_COLOR_DARK
DELETE_BUTTON_COLOR = ft.colors.RED_700
TABLE_BORDER_COLOR = ft.colors.with_opacity(0.5, ft.colors.BLACK45)
SEARCH_ICON_COLOR = "#6B6B6B"


def create_student_registration_tab(page: ft.Page):
    """Create and return the student registration tab"""

    # Student table with database integration
    student_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الاسم")),
            ft.DataColumn(ft.Text("العمر")),
            ft.DataColumn(ft.Text("تاريخ الميلاد")),
            ft.DataColumn(ft.Text("رقم التليفون")),
            ft.DataColumn(ft.Text("وظيفة الأب")),
            ft.DataColumn(ft.Text("وظيفة الأم")),
            ft.DataColumn(ft.Text("المشكلة")),
            ft.DataColumn(ft.Text("تاريخ الزيارة")),
        ],
        rows=[],
        border=ft.border.all(1, TABLE_BORDER_COLOR),
        border_radius=ft.border_radius.all(BORDER_RADIUS),
        vertical_lines=ft.border.BorderSide(1, TABLE_BORDER_COLOR),
        horizontal_lines=ft.border.BorderSide(1, TABLE_BORDER_COLOR),
        heading_row_color=ft.colors.with_opacity(0.05, ft.colors.BLACK12),
        heading_row_height=45,
        data_row_max_height=55,
        column_spacing=20,
    )

    def update_student_table():
        # Get students from database using ChildService
        with db_session() as db:
            children_dto = ChildService.get_all_children(db)

            if student_data_table.rows is None:
                student_data_table.rows = []
            else:
                student极able.rows.clear()

            for child in children_dto:
                student_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(child.name)),
                            ft.DataCell(ft.Text(str(child.age) if child.age else "-")),
                            ft.DataCell(
                                ft.Text(
                                    child.birth_date.strftime("%Y-%m-%d")
                                    if child.birth_date
                                    else "-"
                                )
                            ),
                            ft.DataCell(ft.Text(child.phone_number or "-")),
                            ft.DataCell(ft.Text(child.father_job or "-")),
                            ft.DataCell(ft.Text(child.mother_job or "-")),
                            ft.DataCell(ft.Text(child.notes or "-")),
                            ft.DataCell(
                                ft.Text(
                                    child.created_at.strftime("%Y-%m-%d %H:%极")
                                    if child.created_at
                                    else "-"
                                )
                            ),
                        ]
                    )
                )
            page.update()

    # Add Student Dialog
    add_student_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة طالب جديد"),
        content=ft.Container(
            width=500,
            height=600,
            content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True),
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_student()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Form fields
    student_name = ft.TextField(label="اسم الطالب", text_align=ft.TextAlign.RIGHT)
    student_age = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT)
    age_counter = 0
    birth_date = ft.TextField(label="تاريخ الميلاد", read_only=True, text_align=ft.TextAlign.RIGHT)
    selected_date = None
    phone = ft.TextField(label="رقم التليفون", text_align=ft.TextAlign.RIGHT)
    dad_job = ft.TextField(label="وظيفة الأب", text_align=ft.TextAlign.RIGHT)
    mum_job = ft.TextField(label="وظيفة الأم", text_align=ft.TextAlign.RIGHT)
    problem = ft.TextField(label="المشكلة", multiline=True, text_align=ft.TextAlign.RIGHT)
    additional_notes = ft.TextField(label="ملاحظات إضافية", multiline=True, text_align=ft.TextAlign.RIGHT)
    photo_path = None
    photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    photo_status = ft.Text("لم يتم اختيار صورة", size=12, color=ft.Colors.GREY, text_align=ft.TextAlign.RIGHT)

    def increment_age(e):
        nonlocal age_counter
        age_counter += 1
        student_age.value = str(age_counter)
        page.update()

    def decrement_age(e):
        nonlocal age_counter
        if age_counter > 0:
            age_counter -= 1
            student_age.value = str(age_counter)
        page.update()

    age_controls = ft.Row(
        [
            ft.ElevatedButton("-", on_click=decrement_age, width=40),
            student_age,
            ft.ElevatedButton("+", on_click=increment_age, width=40),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Date picker for birth date
    date_picker = ft.DatePicker(
        on_change=handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(date_picker)

    def handle_date_picker(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            birth_date.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    # Photo upload functionality
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal photo_path
        if e.files:
            # Create student_photos directory if it doesn't exist
            photos_dir = "student_photos"
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Copy the file to student_photos directory
            uploaded_file = e.files[0]
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = (
                f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            )
            photo_path = os.path.join(photos_dir, new_filename)

            # Copy the file
            shutil.copy2(uploaded_file.path, photo_path)

            # Update UI
            photo_preview.src = photo_path
            photo_preview.visible = True
            photo_status.value = f"تم اختيار: {uploaded_file.name}"
            photo_status.color = ft.Colors.GREEN
            page.update()

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=pick_photo
    )

    def add_student():
        # Validate required fields
        if not student_name.value:
            show_error("يجب إدخال اسم الطالب!")
            return

        if not student_age.value or int(student_age.value) <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!")
            return

        if not birth_date.value:
            show_error("يجب اختيار تاريخ الميلاد!")
            return

        # Create child DTO with current timestamp
        child_data = CreateChildDTO(
            name=str(student_name.value),
            age=int(student_age.value),
            birth_date=datetime.datetime.strptime(birth_date.value, "%Y-%m-%d").date(),
            phone_number=str(phone.value),
            father_job=str(dad_job.value),
            mother_job=str(mum_job.value),
            notes=str(problem.value),
            child_image=photo_path,
            created_at=datetime.datetime.now(),
        )

        # Add student to database with photo path using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.create_child(db, child_data)

                if child_dto:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Refresh student table
                    update_student_table()

                    show_success("تم إضافة الطالب بنجاح!")
                else:
                    show_error("فشل في إضافة الطالب!")
            except Exception as ex:
                show_error(f"خطأ في إضافة الطالب: {str(ex)}")

    def show_error(message):
        snackbar = ft极nackBar(
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
        nonlocal age_counter, photo_path, selected_date
        student_name.value = ""
        age_counter = 0
        student_age.value = "0"
        birth_date.value = ""
        selected_date = None
        phone.value = ""
        dad_job.value = ""
        mum_job.value = ""
        problem.value = ""
        additional_notes.value = ""
        photo_path = None
        photo_preview.src = ""
        photo_preview.visible = False
        photo_status.value = "لم يتم اختيار صورة"
        photo_status.color = ft.Colors.GREY

    def open_add_student_dialog(e):
        # Build the dialog content
        add_student_dialog.content.content.controls = [
            student_name,
            ft.Text("العمر:", size=16, text_align=ft.TextAlign.RIGHT),
            age_controls,
            ft.Row([birth_date, date_picker_btn], spacing=10),
            phone,
            dad_job,
            mum_job,
            problem,
            additional_notes,
            ft.Text("صورة الطالب:", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
            photo_upload_btn,
            ft.Row([photo_preview], alignment=ft.MainAxisAlignment.CENTER),
            photo_status,
        ]
        page.open(add_student_dialog)

    def close_dialog():
        page.close(add_student_dialog)

    # Add Student button
    add_student_btn = ft.ElevatedButton(
        "إضافة طالب جديد", icon=ft.Icons.ADD, on_click=open_add_student_dialog
    )

    # Load initial student data
    update_student_table()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("إدارة الطلاب", size=24, weight=ft.FontWeight.BOLD),
                    add_student_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([student_data_table], scroll=ft.ScrollMode.AUTO),
                height=500,
                padding=10,
                alignment=ft.alignment.center,
                margin=10,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
