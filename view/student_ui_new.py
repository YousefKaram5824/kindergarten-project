import datetime
import os
import shutil
import flet as ft
from sqlalchemy.orm import Session

# Local imports
from database import get_db, db_session
from DTOs.child_dto import CreateChildDTO
from logic.child_logic import ChildService
from models import ChildTypeEnum
from view.student_detail_ui import show_student_details

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

    # Student table with database integration
    student_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الاسم")),
            ft.DataColumn(ft.Text("العمر")),
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
                            icon_color=ft.Colors.BLUE,
                            tooltip="عرض",
                            on_click=lambda e, child_id=child.id: show_student_details(
                               page, child_id
                            )
                        ),
                        # Edit icon
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.ORANGE,
                            tooltip="تعديل",
                            on_click=lambda e, child_id=child.id: edit_student(child_id)
                        ),
                        # Delete icon
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="حذف",
                            on_click=lambda e, child_id=child.id: delete_student(child_id)
                        ),
                    ],
                    spacing=5
                )

                student_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(child.name)),
                            ft.DataCell(ft.Text(str(child.age) if child.age else "-")),
                            ft.DataCell(action_icons),
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
     """Open a dialog to edit student info including photo"""
     with db_session() as db:
        child = ChildService.get_child_by_id(db, child_id)
        if not child:
            return

        # TextFields
        name_field = ft.TextField(label="اسم الطالب", value=child.name)
        age_field = ft.TextField(label="العمر", value=str(child.age))
        phone_field = ft.TextField(label="رقم التليفون", value=child.phone_number or "")
        dad_job_field = ft.TextField(label="وظيفة الأب", value=child.father_job or "")
        mum_job_field = ft.TextField(label="وظيفة الأم", value=child.mother_job or "")
        notes_field = ft.TextField(label="ملاحظات إضافية", multiline=True, value=child.notes or "")

        # Image preview
        photo_preview = ft.Image(
            src=child.child_image if child.child_image else "",
            width=150,
            height=150,
            fit=ft.ImageFit.COVER
        )
        photo_path = child.child_image  # current photo path

        # FilePicker to change photo
        def handle_file_picker_result(e: ft.FilePickerResultEvent):
            nonlocal photo_path
            if e.files:
                uploaded_file = e.files[0]
                photos_dir = "student_photos"
                if not os.path.exists(photos_dir):
                    os.makedirs(photos_dir)

                file_extension = os.path.splitext(uploaded_file.name)[1]
                new_filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                photo_path = os.path.join(photos_dir, new_filename)
                shutil.copy2(uploaded_file.path, photo_path)
                photo_preview.src = photo_path
                page.update()

        file_picker = ft.FilePicker(on_result=handle_file_picker_result)
        page.overlay.append(file_picker)

        def pick_photo(e):
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["jpg", "jpeg", "png", "gif"],
                dialog_title="اختر صورة الطالب",
            )

        photo_button = ft.ElevatedButton("تغيير الصورة", on_click=pick_photo)

        # Save button
        def save_edit(e):
            try:
                updated_data = CreateChildDTO(
                    name=name_field.value,
                    age=int(age_field.value),
                    birth_date=child.birth_date,
                    phone_number=phone_field.value,
                    father_job=dad_job_field.value,
                    mother_job=mum_job_field.value,
                    notes=notes_field.value,
                    child_image=photo_path,
                    created_at=child.created_at
                )
                ChildService.update_child(db, child_id, updated_data)
                update_student_table()
                page.update()
                page.close(dialog)
            except Exception as ex:
                snackbar = ft.SnackBar(
                    content=ft.Text(f"خطأ في التحديث: {ex}"),
                    bgcolor=ft.Colors.RED,
                    duration=3000,
                )
                page.overlay.append(snackbar)
                snackbar.open = True
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"تعديل بيانات الطالب: {child.name}"),
            content=ft.Column([
                name_field,
                age_field,
                phone_field,
                dad_job_field,
                mum_job_field,
                notes_field,
                ft.Row([photo_preview, photo_button], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            actions=[
                ft.TextButton("حفظ", on_click=save_edit),
                ft.TextButton("إلغاء", on_click=lambda e: page.close(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True
        )
        page.open(dialog)

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

    # Form fields
    student_name = ft.TextField(label="اسم الطالب", text_align=ft.TextAlign.RIGHT)
    student_age = ft.TextField(
        value="3", 
        text_align=ft.TextAlign.CENTER,
        width=60,
        height=40,
        content_padding=ft.padding.all(8),
        border_radius=ft.border_radius.all(BORDER_RADIUS),
        border_color=INPUT_BORDER_COLOR,
        bgcolor=INPUT_BGCOLOR,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string="")
    )
    age_counter = 3
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
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=decrement_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=BUTTON_BGCOLOR,
                    shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(BORDER_RADIUS))
                )
            ),
            student_age,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=increment_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=BUTTON_BGCOLOR,
                    shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(BORDER_RADIUS))
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    def handle_date_picker(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            birth_date.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=pick_photo
    )

    


    # Add Student Dialog - Matching auth dialog style
    add_student_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة طالب جديد", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                student_name,
                ft.Container(
                    ft.Text("العمر:", size=16, text_align=ft.TextAlign.RIGHT), padding=ft.padding.only(bottom=5)
                ),
                age_controls,
                birth_date,
                ft.Container(date_picker_btn, padding=ft.padding.only(bottom=10)),
                phone,
                dad_job,
                mum_job,
                problem,
                additional_notes,

               

                

                ft.Container(
                    ft.Text("صورة الطالب:", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
                    padding=ft.padding.only(top=10, bottom=5),
                ),
                photo_upload_btn,
                ft.Container(
                    ft.Row([photo_preview], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=5, bottom=5),
                ),
                ft.Container(photo_status, padding=ft.padding.only(bottom=10)),
            ],
            width=400,
            height=550,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_student()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Date picker for birth date
    date_picker = ft.DatePicker(
        on_change=handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(date_picker)

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

    # Photo upload functionality
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

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
            child_type=ChildTypeEnum[child_type_combo.value]
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
        nonlocal age_counter, photo_path, selected_date
        student_name.value = ""
        age_counter = 3
        student_age.value = "3"
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
