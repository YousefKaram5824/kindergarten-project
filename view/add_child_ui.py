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
    validate_child_form,
    create_child_dto,
)
from models import ChildTypeEnum
import datetime
from database import db_session
from logic.child_logic import ChildService

# Module-level variables for add functionality
age_counter = 3
selected_date = None
photo_path = [None]  # Use list to allow modification in nested functions

# Create form fields using helper
child_id, child_name, phone, dad_job, mum_job, problem, additional_notes = (
    create_common_form_fields()
)


# Create age controls
def increment_age(e):
    global age_counter
    age_counter += 1
    child_age.value = str(age_counter)
    e.page.update()


def decrement_age(e):
    global age_counter
    if age_counter > 0:
        age_counter -= 1
        child_age.value = str(age_counter)
    e.page.update()


child_age, age_controls = create_age_controls(age_counter, increment_age, decrement_age)


# Create date picker components
def handle_date_picker(e):
    global selected_date
    if e.control.value:
        selected_date = e.control.value
        birth_date.value = selected_date.strftime("%Y-%m-%d")
        e.page.update()


birth_date, date_picker, date_picker_btn = create_date_picker_components(
    selected_date, handle_date_picker
)


# Create photo upload components
def handle_file_picker(e):
    handle_file_picker_result(e, photo_preview, photo_status, photo_path)


photo_preview, photo_status, file_picker, photo_upload_btn = (
    create_photo_upload_components(photo_path[0], handle_file_picker)
)

# Child type dropdown
selected_child_type = ChildTypeEnum.FULL_DAY


def update_selected_child_type(e):
    global selected_child_type
    if e.control.value == ChildTypeEnum.FULL_DAY.name:
        selected_child_type = ChildTypeEnum.FULL_DAY
    elif e.control.value == ChildTypeEnum.SESSIONS.name:
        selected_child_type = ChildTypeEnum.SESSIONS


child_type_dropdown = create_child_type_dropdown(
    selected_child_type, update_selected_child_type
)

# Add child Dialog - Matching auth dialog style
add_child_dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("إضافة طالب جديد", text_align=ft.TextAlign.CENTER),
    content=ft.Column(
        [
            child_id,
            child_name,
            ft.Container(
                ft.Text("العمر:", size=16, text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            age_controls,
            ft.Row(
                [date_picker_btn, birth_date],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            phone,
            dad_job,
            mum_job,
            child_type_dropdown,
            problem,
            additional_notes,
            ft.Container(
                ft.Text(
                    "صورة الطالب:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.RIGHT,
                ),
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
        ft.TextButton(
            "إلغاء", on_click=lambda e: [reset_form(e.page), close_dialog(e.page)]
        ),
        ft.TextButton("إضافة", on_click=lambda e: add_child(e.page)),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

# Date picker for birth date
date_picker = ft.DatePicker(
    on_change=handle_date_picker,
    first_date=datetime.datetime(2000, 1, 1),
    last_date=datetime.datetime.now(),
)

# Photo upload functionality
file_picker = ft.FilePicker(on_result=handle_file_picker)


def add_child(page):
    global on_save_callback
    # Validate required fields using helper
    if not validate_child_form(child_id, child_name, child_age, birth_date, page):
        return

    # Create child DTO using helper
    child_data = create_child_dto(
        child_id,
        child_name,
        child_age,
        birth_date,
        phone,
        dad_job,
        mum_job,
        problem,
        photo_path,
        selected_child_type,
    )

    # Add child to database with photo path using ChildService
    with db_session() as db:
        try:
            child_dto = ChildService.create_child(db, child_data)

            if child_dto:
                # Clear form and close dialog
                reset_form(page)
                close_dialog(page)

                # Refresh child table
                if on_save_callback:
                    on_save_callback()

                show_success("تم إضافة الطالب بنجاح!", page)
            else:
                show_error("فشل في إضافة الطالب!", page)
        except Exception as ex:
            show_error(f"خطأ في إضافة الطالب: {str(ex)}", page)


def reset_form(page):
    global age_counter, photo_path, selected_date, selected_child_type
    child_name.value = ""
    age_counter = 3
    child_age.value = "3"
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
    selected_child_type = ChildTypeEnum.FULL_DAY
    child_type_dropdown.value = ChildTypeEnum.FULL_DAY.name
    page.update()


def close_dialog(page):
    page.close(add_child_dialog)


# Global callback for refreshing table
on_save_callback = None


def open_add_child_dialog(page, on_save_callback_param=None):
    global on_save_callback
    on_save_callback = on_save_callback_param

    # Add overlays if not already added
    if date_picker not in page.overlay:
        page.overlay.append(date_picker)
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)

    # Open add dialog
    page.open(add_child_dialog)
