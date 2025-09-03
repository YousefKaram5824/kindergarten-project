import datetime
import os
import shutil
import flet as ft

# Local imports
from DTOs.child_dto import CreateChildDTO
from models import ChildTypeEnum

# Common Color Constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


# Common Snackbar Functions
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


# Common Age Control Components
def create_age_controls(age_counter, increment_callback, decrement_callback):
    age_field = ft.TextField(
        value=str(age_counter),
        text_align=ft.TextAlign.CENTER,
        width=60,
        height=40,
        content_padding=ft.padding.all(8),
        border_radius=ft.border_radius.all(BORDER_RADIUS),
        border_color=ft.Colors.BLUE,
        bgcolor=INPUT_BGCOLOR,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )

    controls = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=lambda e: decrement_callback(e, age_field),
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
            age_field,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=lambda e: increment_callback(e, age_field),
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    return age_field, controls


# Common Date Picker Components
def create_date_picker_components(selected_date, handle_date_callback):
    birth_date_field = ft.TextField(
        label="تاريخ الميلاد",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )

    date_picker = ft.DatePicker(
        on_change=lambda e: handle_date_callback(e, birth_date_field),
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )

    date_picker_btn = ft.ElevatedButton(
        "اختر التاريخ", on_click=lambda e: e.page.open(date_picker)
    )

    return birth_date_field, date_picker, date_picker_btn


# Common Photo Upload Components
def create_photo_upload_components(photo_path, handle_file_callback):
    photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    photo_status = ft.Text(
        "لم يتم اختيار صورة",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
    )

    file_picker = ft.FilePicker(
        on_result=lambda e: handle_file_callback(e, photo_preview, photo_status)
    )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        ),
    )

    return photo_preview, photo_status, file_picker, photo_upload_btn


# Common Child Type Dropdown
def create_child_type_dropdown(selected_child_type, on_change_callback):
    dropdown = ft.Dropdown(
        label="نوع الطالب",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        value=selected_child_type.name,
        options=[
            ft.dropdown.Option(
                key=ChildTypeEnum.FULL_DAY.name, text=ChildTypeEnum.FULL_DAY.value
            ),
            ft.dropdown.Option(
                key=ChildTypeEnum.SESSIONS.name, text=ChildTypeEnum.SESSIONS.value
            ),
        ],
        on_change=on_change_callback,
    )
    return dropdown


# Common Form Fields
def create_common_form_fields():
    child_id = ft.TextField(
        label="الرقم التعريفي للطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
        autofocus=True,
    )

    child_name = ft.TextField(
        label="اسم الطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    phone = ft.TextField(
        label="رقم التليفون",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    dad_job = ft.TextField(
        label="وظيفة الأب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    mum_job = ft.TextField(
        label="وظيفة الأم",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    problem = ft.TextField(
        label="المشكلة",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    additional_notes = ft.TextField(
        label="ملاحظات إضافية",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    return child_id, child_name, phone, dad_job, mum_job, problem, additional_notes


# Common File Picker Handler
def handle_file_picker_result(e, photo_preview, photo_status, photo_path_var):
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
        photo_path = os.path.join(photos_dir, new_filename)

        # Copy the file
        shutil.copy2(uploaded_file.path, photo_path)

        # Update UI
        photo_preview.src = photo_path
        photo_preview.visible = True
        photo_status.value = f"تم اختيار: {uploaded_file.name}"
        photo_status.color = ft.Colors.GREEN
        e.page.update()

        # Update the photo_path variable
        photo_path_var[0] = photo_path


# Common Form Validation
def validate_child_form(child_id, child_name, child_age, birth_date, page):
    if not child_id.value:
        show_error("يجب إدخال الرقم التعريفي للطالب!", page)
        return False

    if not child_name.value:
        show_error("يجب إدخال اسم الطالب!", page)
        return False

    if not child_age.value:
        show_error("يجب إدخال عمر صحيح للطالب!", page)
        return False

    try:
        age = int(child_age.value)
        if age <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!", page)
            return False
    except ValueError:
        show_error("يجب إدخال عمر صحيح للطالب!", page)
        return False

    if not birth_date.value:
        show_error("يجب اختيار تاريخ الميلاد!", page)
        return False

    return True


# Common Child DTO Creation
def create_child_dto(
    child_id,
    child_name,
    child_age,
    birth_date,
    phone,
    dad_job,
    mum_job,
    problem,
    photo_path,
    child_type,
):
    return CreateChildDTO(
        id=int(child_id.value),
        name=str(child_name.value),
        age=int(child_age.value),
        birth_date=datetime.datetime.strptime(birth_date.value, "%Y-%m-%d").date(),
        phone_number=str(phone.value) if phone.value else None,
        father_job=str(dad_job.value) if dad_job.value else None,
        mother_job=str(mum_job.value) if mum_job.value else None,
        notes=str(problem.value) if problem.value else None,
        child_image=photo_path,
        created_at=datetime.datetime.now(),
        child_type=child_type,
    )
