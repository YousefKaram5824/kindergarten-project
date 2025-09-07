import datetime
import os
import shutil
import flet as ft

# Local imports
from database import db_session
from DTOs.child_dto import CreateChildDTO
from models import ChildTypeEnum
from logic.child_logic import ChildService

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8


def create_add_child_dialog(page: ft.Page, update_table_callback):
    """Create and return the add child dialog and button"""

    # Form fields
    child_id = ft.TextField(
        label="رقم التعريفي للطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        hint_text="أدخل رقم أكبر من 100",
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )
    child_name = ft.TextField(
        label="اسم الطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    child_age = ft.TextField(
        value="3",
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
    age_counter = 3
    birth_date = ft.TextField(
        label="تاريخ الميلاد",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=210,
    )
    selected_date = None
    created_at_date = ft.TextField(
        label="تاريخ التسجيل",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=170,
    )
    created_at_time = ft.TextField(
        label="وقت التسجيل",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=170,
    )
    selected_created_at_date = None
    selected_created_at_time = None
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
    photo_path = None
    photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    photo_status = ft.Text(
        "لم يتم اختيار صورة",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
    )

    def increment_age(e):
        nonlocal age_counter
        age_counter += 1
        child_age.value = str(age_counter)
        page.update()

    def decrement_age(e):
        nonlocal age_counter
        if age_counter > 0:
            age_counter -= 1
            child_age.value = str(age_counter)
        page.update()

    age_controls = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=decrement_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
            child_age,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=increment_age,
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

    def handle_date_picker(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            birth_date.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    def handle_created_at_date_picker(e):
        nonlocal selected_created_at_date
        if e.control.value:
            selected_created_at_date = e.control.value
            created_at_date.value = selected_created_at_date.strftime("%Y-%m-%d")
            page.update()

    def open_created_at_date_picker(e):
        page.open(created_at_date_picker)

    created_at_date_picker_btn = ft.ElevatedButton(
        "اختر تاريخ التسجيل", on_click=open_created_at_date_picker
    )

    def handle_created_at_time_picker(e):
        nonlocal selected_created_at_time
        if e.control.value:
            selected_created_at_time = e.control.value
            created_at_time.value = selected_created_at_time.strftime("%H:%M")
            page.update()

    def open_created_at_time_picker(e):
        page.open(created_at_time_picker)

    created_at_time_picker_btn = ft.ElevatedButton(
        "اختر وقت التسجيل", on_click=open_created_at_time_picker
    )

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=pick_photo
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
                ft.Row(
                    [created_at_date_picker_btn, created_at_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [created_at_time_picker_btn, created_at_time],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                phone,
                dad_job,
                mum_job,
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
            height=800,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_child()),
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

    # Date picker for created_at
    created_at_date_picker = ft.DatePicker(
        on_change=handle_created_at_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(created_at_date_picker)

    # Time picker for created_at
    created_at_time_picker = ft.TimePicker(
        on_change=handle_created_at_time_picker,
    )
    page.overlay.append(created_at_time_picker)

    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal photo_path
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
            page.update()

    # Photo upload functionality
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    def add_child():
        # Validate required fields
        if not child_id.value:
            show_error("يجب إدخال رقم التعريفي!")
            return

        try:
            child_id_int = int(child_id.value)
        except ValueError:
            show_error("الرقم التعريفي يجب أن يكون رقماً صحيحاً!")
            return

        if child_id_int <= 100:
            show_error("الرقم التعريفي يجب أن يكون أكبر من 100!")
            return

        # Check uniqueness
        with db_session() as db:
            if not ChildService.is_id_available(db, child_id_int):
                show_error("الرقم التعريفي مستخدم من قبل طفل آخر!")
                return

        if not child_name.value:
            show_error("يجب إدخال اسم الطالب!")
            return

        if not child_age.value or int(child_age.value) <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!")
            return

        if not birth_date.value:
            show_error("يجب اختيار تاريخ الميلاد!")
            return

        # Validate created_at date and time if provided
        created_at_value = None
        if created_at_date.value and created_at_time.value:
            try:
                created_at_value = datetime.datetime.strptime(
                    f"{created_at_date.value} {created_at_time.value}", "%Y-%m-%d %H:%M"
                )
                if created_at_value > datetime.datetime.now():
                    show_error("تاريخ ووقت التسجيل لا يمكن أن يكون في المستقبل!")
                    return
            except ValueError:
                show_error("صيغة تاريخ أو وقت التسجيل غير صحيحة!")
                return
        else:
            created_at_value = datetime.datetime.now()

        # Create child DTO with created_at value
        child_data = CreateChildDTO(
            id=child_id_int,
            name=str(child_name.value),
            age=int(child_age.value),
            birth_date=datetime.datetime.strptime(birth_date.value, "%Y-%m-%d").date(),
            phone_number=str(phone.value) if phone.value else None,
            father_job=str(dad_job.value) if dad_job.value else None,
            mother_job=str(mum_job.value) if mum_job.value else None,
            notes=str(additional_notes.value) if additional_notes.value else None,
            problems=str(problem.value) if problem.value else None,
            child_image=photo_path,
            created_at=created_at_value,
            child_type=ChildTypeEnum.NONE,
        )

        # Add child to database with photo path using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.create_child(db, child_data)

                if child_dto:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Refresh child table
                    update_table_callback()

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
        nonlocal age_counter, photo_path, selected_date, selected_created_at_date, selected_created_at_time
        child_id.value = ""
        child_name.value = ""
        age_counter = 3
        child_age.value = "3"
        birth_date.value = ""
        selected_date = None
        created_at_date.value = ""
        selected_created_at_date = None
        created_at_time.value = ""
        selected_created_at_time = None
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

    def open_add_child_dialog(e):
        page.open(add_child_dialog)

    def close_dialog():
        page.close(add_child_dialog)

    # Add child button
    add_child_btn = ft.ElevatedButton(
        "إضافة طالب جديد", icon=ft.Icons.ADD, on_click=open_add_child_dialog
    )

    return add_child_dialog, add_child_btn
