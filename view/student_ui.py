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
INPUT_BGCOLOR = ft.Colors.WHITE
INPUT_BORDER_COLOR = "#B58B18"  # Gold
BUTTON_BGCOLOR = "#B58B18"  # Gold
BUTTON_TEXT_COLOR = ft.Colors.WHITE
TEXT_COLOR_GOLD = "#B58B18"  # Gold
TEXT_COLOR_DARK = "#262626"  # Slightly darker text for better contrast
TEXT_COLOR_TABLE_DATA = ft.Colors.BLACK  # Explicitly black for table data cells
FONT_FAMILY_REGULAR = "Tajawal"
FONT_FAMILY_BOLD = "Tajawal-Bold"
BORDER_RADIUS = 8
TABLE_ROW_TEXT = TEXT_COLOR_DARK
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)
SEARCH_ICON_COLOR = "#6B6B6B"


def create_student_registration_tab(page: ft.Page):
    """Create and return the student registration tab"""
    # Student Registration Form in Arabic
    student_name = ft.TextField(label="اسم الطالب", text_align=ft.TextAlign.RIGHT)

    # Age counter
    student_age = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT)
    age_counter = 0

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
    birth_date = ft.TextField(label="تاريخ الميلاد", read_only=True, text_align=ft.TextAlign.RIGHT)
    selected_date = None

    def handle_date_picker(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            birth_date.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    date_picker = ft.DatePicker(
        on_change=handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(date_picker)

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    phone = ft.TextField(label="رقم التليفون")
    dad_job = ft.TextField(label="وظيفة الأب")
    mum_job = ft.TextField(label="وظيفة الأم")
    problem = ft.TextField(label="المشكلة", multiline=True)
    additional_notes = ft.TextField(label="ملاحظات إضافية", multiline=True)

    # Photo upload functionality
    photo_path = None
    photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    photo_status = ft.Text("لم يتم اختيار صورة", size=12, color=ft.Colors.GREY)

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

    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=pick_photo
    )

    def add_student(e):
        # Validate required fields
        if not student_name.value:
            snackbar = ft.SnackBar(
                content=ft.Text("يجب إدخال اسم الطالب!"),
                bgcolor=ft.Colors.RED,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()
            return

        if not student_age.value or int(student_age.value) <= 0:
            snackbar = ft.SnackBar(
                content=ft.Text("يجب إدخال عمر صحيح للطالب!"),
                bgcolor=ft.Colors.RED,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()
            return

        if not birth_date.value:
            snackbar = ft.SnackBar(
                content=ft.Text("يجب اختيار تاريخ الميلاد!"),
                bgcolor=ft.Colors.RED,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()
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
            created_at=datetime.datetime.now(),  # Set timestamp when user clicks add
        )

        # Add student to database with photo path using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.create_child(db, child_data)

                if child_dto:
                    # Clear form fields
                    student_name.value = ""
                    student_age.value = "0"
                    age_counter = 0
                    birth_date.value = ""
                    phone.value = ""
                    dad_job.value = ""
                    mum_job.value = ""
                    additional_notes.value = ""

                    # Refresh student table
                    update_student_table()

                    snackbar = ft.SnackBar(
                        content=ft.Text("تم إضافة الطالب بنجاح!"),
                        bgcolor=ft.Colors.GREEN,
                        duration=3000,
                    )
                    page.overlay.append(snackbar)
                    page.update()
                    snackbar.open = True
                    snackbar.update()
                    page.update()
                else:
                    snackbar = ft.SnackBar(
                        content=ft.Text("فشل في إضافة الطالب!"),
                        bgcolor=ft.Colors.RED,
                        duration=3000,
                    )
                    page.overlay.append(snackbar)
                    page.update()
                    snackbar.open = True
                    snackbar.update()
                    page.update()
            except Exception as ex:
                snackbar = ft.SnackBar(
                    content=ft.Text(f"خطأ في إضافة الطالب: {str(ex)}"),
                    bgcolor=ft.Colors.RED,
                    duration=3000,
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

    add_student_btn = ft.ElevatedButton("إضافة طالب", on_click=add_student)

    # Student table with database integration
    student_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الإجراءات")),
            ft.DataColumn(ft.Text("الاسم")),
            ft.DataColumn(ft.Text("العمر")),
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
                student_data_table.rows.clear()

            for child in children_dto:
                # Create action icons for each student
                action_icons = ft.Row(
                    [
                        # Display icon
                        ft.IconButton(
                            icon=ft.Icons.VISIBILITY,
                            icon_color=ft.colors.BLUE,
                            tooltip="عرض",
                            on_click=lambda e, child_id=child.id: display_student(child_id)
                        ),
                        # Edit icon
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.colors.ORANGE,
                            tooltip="تعديل",
                            on_click=lambda e, child_id=child.id: edit_student(child_id)
                        ),
                        # Delete icon
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.colors.RED,
                            tooltip="حذف",
                            on_click=lambda e, child_id=child.id: delete_student(child_id)
                        ),
                    ],
                    spacing=5
                )

                student_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(action_icons),
                            ft.DataCell(ft.Text(child.name)),
                            ft.DataCell(ft.Text(str(child.age) if child.age else "-")),
                        ]
                    )
                )
            page.update()

    # Action handlers for the icons
    def display_student(child_id):
        """Display student details"""
        with db_session() as db:
            child = ChildService.get_child_by_id(db, child_id)
            if child:
                # Show student details in a dialog or snackbar
                snackbar = ft.SnackBar(
                    content=ft.Text(f"عرض بيانات الطالب: {child.name}"),
                    bgcolor=ft.Colors.BLUE,
                    duration=2000,
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

    def edit_student(child_id):
        """Edit student details"""
        with db_session() as db:
            child = ChildService.get_child_by_id(db, child_id)
            if child:
                # Show edit dialog or form
                snackbar = ft.SnackBar(
                    content=ft.Text(f"تعديل بيانات الطالب: {child.name}"),
                    bgcolor=ft.Colors.ORANGE,
                    duration=2000,
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

    def delete_student(child_id):
        """Delete student"""
        with db_session() as db:
            child = ChildService.get_child_by_id(db, child_id)
            if child:
                # Show confirmation dialog
                def confirm_delete(e):
                    try:
                        success = ChildService.delete_child(db, child_id)
                        if success:
                            update_student_table()
                            snackbar = ft.SnackBar(
                                content=ft.Text(f"تم حذف الطالب: {child.name}"),
                                bgcolor=ft.Colors.GREEN,
                                duration=3000,
                            )
                        else:
                            snackbar = ft.SnackBar(
                                content=ft.Text("فشل في حذف الطالب"),
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
                    content=ft.Text(f"هل تريد حذف الطالب {child.name}؟"),
                    actions=[
                        ft.TextButton("نعم", on_click=confirm_delete),
                        ft.TextButton("لا", on_click=cancel_delete),
                    ],
                )
                page.open(dialog)

    # Load initial student data
    update_student_table()

    return ft.Column(
        [
            ft.Text("تسجيل الطلاب", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
            ft.Divider(),
            student_name,
            ft.Text("العمر:", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
            age_controls,
            birth_date,
            date_picker_btn,
            phone,
            dad_job,
            mum_job,
            problem,
            additional_notes,
            # Photo upload section
            ft.Text("صورة الطالب:", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
            photo_upload_btn,
            ft.Row([photo_preview], alignment=ft.MainAxisAlignment.CENTER),
            photo_status,
            ft.Row([add_student_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Row(
                [ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
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
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
