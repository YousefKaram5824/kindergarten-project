import flet as ft

# Local imports
from view.ui_helpers import (
    show_error,
    show_success,
    create_age_controls,
    create_date_picker_components,
    create_photo_upload_components,
    create_child_type_dropdown,
    create_common_form_fields,
    handle_file_picker_result,
)
from models import ChildTypeEnum
import datetime
import os
import shutil
from DTOs.child_dto import CreateChildDTO
from database import db_session
from logic.child_logic import ChildService

# Module-level variables for edit functionality
current_edit_child_id = None
edit_age_counter = 3
edit_selected_date = None
edit_photo_path = None  # Use list to allow modification in nested functions

# Edit form fields
edit_child_id = ft.TextField(
    label="الرقم التعريفي للطالب",
    text_align=ft.TextAlign.RIGHT,
    width=300,
    read_only=True,
)

# Create other form fields using helper
(
    edit_child_name,
    edit_phone,
    edit_dad_job,
    edit_mum_job,
    edit_problem,
    edit_additional_notes,
) = create_common_form_fields()[
    1:
]  # Skip child_id


# Create age controls
def edit_increment_age(e):
    global edit_age_counter
    edit_age_counter += 1
    edit_child_age.value = str(edit_age_counter)
    e.page.update()


def edit_decrement_age(e):
    global edit_age_counter
    if edit_age_counter > 0:
        edit_age_counter -= 1
        edit_child_age.value = str(edit_age_counter)
    e.page.update()


edit_child_age, edit_age_controls = create_age_controls(
    edit_age_counter, edit_increment_age, edit_decrement_age
)


# Create date picker components
def edit_handle_date_picker(e):
    global edit_selected_date
    if e.control.value:
        edit_selected_date = e.control.value
        edit_birth_date.value = edit_selected_date.strftime("%Y-%m-%d")
        e.page.update()


edit_birth_date, edit_date_picker, edit_date_picker_btn = create_date_picker_components(
    edit_selected_date, edit_handle_date_picker
)


# Create photo upload components
def edit_handle_file_picker(e):
    handle_file_picker_result(e, edit_photo_preview, edit_photo_status, edit_photo_path)


edit_photo_preview, edit_photo_status, edit_file_picker, edit_photo_upload_btn = (
    create_photo_upload_components(edit_photo_path, edit_handle_file_picker)
)

# Edit child type dropdown
edit_selected_child_type = ChildTypeEnum.FULL_DAY


def update_edit_selected_child_type(e):
    global edit_selected_child_type
    if e.control.value == ChildTypeEnum.FULL_DAY.name:
        edit_selected_child_type = ChildTypeEnum.FULL_DAY
    elif e.control.value == ChildTypeEnum.SESSIONS.name:
        edit_selected_child_type = ChildTypeEnum.SESSIONS


edit_child_type_dropdown = create_child_type_dropdown(
    edit_selected_child_type, update_edit_selected_child_type
)

# Edit child Dialog
edit_child_dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("تعديل بيانات الطالب", text_align=ft.TextAlign.CENTER),
    content=ft.Column(
        [
            edit_child_id,
            edit_child_name,
            ft.Container(
                ft.Text("العمر:", size=16, text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            edit_age_controls,
            ft.Row(
                [edit_date_picker_btn, edit_birth_date],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            edit_phone,
            edit_dad_job,
            edit_mum_job,
            edit_child_type_dropdown,
            edit_problem,
            edit_additional_notes,
            ft.Container(
                ft.Text(
                    "صورة الطالب:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.RIGHT,
                ),
                padding=ft.padding.only(top=10, bottom=5),
            ),
            edit_photo_upload_btn,
            ft.Container(
                ft.Row([edit_photo_preview], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(top=5, bottom=5),
            ),
            ft.Container(edit_photo_status, padding=ft.padding.only(bottom=10)),
        ],
        width=400,
        height=550,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    ),
    actions=[
        ft.TextButton("إلغاء", on_click=lambda e: close_edit_dialog(e.page)),
        ft.TextButton("حفظ", on_click=lambda e: save_edit_child(e.page)),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

# Edit Date picker
edit_date_picker = ft.DatePicker(
    on_change=edit_handle_date_picker,
    first_date=datetime.datetime(2000, 1, 1),
    last_date=datetime.datetime.now(),
)


def edit_handle_file_picker_result(e: ft.FilePickerResultEvent):
    global edit_photo_path
    if e.files:
        # Create child_photos directory if it doesn't exist
        photos_dir = "child_photos"
        if not os.path.exists(photos_dir):
            os.makedirs(photos_dir)

        # Copy the file to child_photos directory
        uploaded_file = e.files[0]
        file_extension = os.path.splitext(uploaded_file.name)[1]
        new_filename = (
            f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        )
        edit_photo_path = os.path.join(photos_dir, new_filename)

        # Copy the file
        shutil.copy2(uploaded_file.path, edit_photo_path)

        # Update UI
        edit_photo_preview.src = edit_photo_path
        edit_photo_preview.visible = True
        edit_photo_status.value = f"تم اختيار: {uploaded_file.name}"
        edit_photo_status.color = ft.Colors.GREEN
        e.page.update()


# Edit Photo upload functionality
edit_file_picker = ft.FilePicker(on_result=edit_handle_file_picker_result)


def save_edit_child(page):
    global current_edit_child_id
    if not current_edit_child_id:
        show_error("لم يتم العثور على الطالب المراد تعديله!", page)
        return

    # Validate required fields
    if not edit_child_name.value:
        show_error("يجب إدخال اسم الطالب!", page)
        return

    if not edit_child_age.value:
        show_error("يجب إدخال عمر صحيح للطالب!", page)
        return

    try:
        age = int(edit_child_age.value)
        if age <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!", page)
            return
    except ValueError:
        show_error("يجب إدخال عمر صحيح للطالب!", page)
        return

    if not edit_birth_date.value:
        show_error("يجب اختيار تاريخ الميلاد!", page)
        return

    # Validate ID
    if not edit_child_id.value:
        show_error("الرقم التعريفي مفقود!", page)
        return

    # Create child DTO with updated data
    child_data = CreateChildDTO(
        id=int(edit_child_id.value),
        name=str(edit_child_name.value),
        age=int(edit_child_age.value),
        birth_date=datetime.datetime.strptime(edit_birth_date.value, "%Y-%m-%d").date(),
        phone_number=str(edit_phone.value) if edit_phone.value else None,
        father_job=str(edit_dad_job.value) if edit_dad_job.value else None,
        mother_job=str(edit_mum_job.value) if edit_mum_job.value else None,
        notes=str(edit_problem.value) if edit_problem.value else None,
        child_image=edit_photo_path,
        created_at=datetime.datetime.now(),  # Keep original created_at or update?
        child_type=edit_selected_child_type,
    )

    # Update child in database using ChildService
    with db_session() as db:
        try:
            child_dto = ChildService.update_child(db, current_edit_child_id, child_data)

            if child_dto:
                # Close dialog and refresh table
                close_edit_dialog(page)
                show_success("تم تعديل بيانات الطالب بنجاح!", page)
                # Call callback to refresh the table
                if on_save_callback_global:
                    on_save_callback_global()
            else:
                show_error("فشل في تعديل بيانات الطالب!", page)
        except Exception as ex:
            show_error(f"خطأ في تعديل بيانات الطالب: {str(ex)}", page)


def close_edit_dialog(page):
    page.close(edit_child_dialog)


def open_edit_child_dialog(page, child_id, on_save_callback=None):
    global current_edit_child_id, edit_age_counter, edit_selected_date, edit_photo_path, on_save_callback_global
    on_save_callback_global = on_save_callback
    with db_session() as db:
        child = ChildService.get_child_by_id(db, child_id)
        if child:
            current_edit_child_id = child_id
            # Populate edit form with child data
            edit_child_id.value = str(child.id)
            edit_child_name.value = child.name
            edit_age_counter = child.age or 3
            edit_child_age.value = str(edit_age_counter)
            edit_birth_date.value = (
                child.birth_date.strftime("%Y-%m-%d") if child.birth_date else ""
            )
            edit_selected_date = child.birth_date if child.birth_date else None
            edit_phone.value = child.phone_number or ""
            edit_dad_job.value = child.father_job or ""
            edit_mum_job.value = child.mother_job or ""
            edit_problem.value = child.notes or ""
            edit_additional_notes.value = ""
            edit_photo_path = child.child_image
            if edit_photo_path and os.path.exists(edit_photo_path):
                edit_photo_preview.src = edit_photo_path
                edit_photo_preview.visible = True
                edit_photo_status.value = (
                    f"تم اختيار: {os.path.basename(edit_photo_path)}"
                )
                edit_photo_status.color = ft.Colors.GREEN
            else:
                edit_photo_preview.src = ""
                edit_photo_preview.visible = False
                edit_photo_status.value = "لم يتم اختيار صورة"
                edit_photo_status.color = ft.Colors.GREY
            edit_selected_child_type = child.child_type or ChildTypeEnum.FULL_DAY
            edit_child_type_dropdown.value = edit_selected_child_type.name

            # Add overlays if not already added
            if edit_date_picker not in page.overlay:
                page.overlay.append(edit_date_picker)
            if edit_file_picker not in page.overlay:
                page.overlay.append(edit_file_picker)

            # Open edit dialog
            page.open(edit_child_dialog)


def show_error(message, page):
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


def show_success(message, page):
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
