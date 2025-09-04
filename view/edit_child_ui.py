import datetime
import os
import shutil
import flet as ft

from database import db_session
from DTOs.child_dto import CreateChildDTO
from models import ChildTypeEnum
from logic.child_logic import ChildService

INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8


def create_edit_child_dialog(page: ft.Page, update_child_table):
    current_edit_child_id = None

    # Edit form fields
    edit_child_id = ft.TextField(
        label="رقم التعريفي للطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )
    edit_child_name = ft.TextField(
        label="اسم الطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_child_age = ft.TextField(
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
    edit_age_counter = 3
    edit_birth_date = ft.TextField(
        label="تاريخ الميلاد",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )
    edit_selected_date = None
    edit_phone = ft.TextField(
        label="رقم التليفون",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_dad_job = ft.TextField(
        label="وظيفة الأب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_mum_job = ft.TextField(
        label="وظيفة الأم",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_problem = ft.TextField(
        label="المشكلة",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_additional_notes = ft.TextField(
        label="ملاحظات إضافية",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_photo_path = None
    edit_photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    edit_photo_status = ft.Text(
        "لم يتم اختيار صورة",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
    )

    # Edit child type dropdown
    edit_selected_child_type = ChildTypeEnum.FULL_DAY
    edit_child_type_dropdown = ft.Dropdown(
        label="نوع الطالب",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        value=ChildTypeEnum.FULL_DAY.name,
        options=[
            ft.dropdown.Option(
                key=ChildTypeEnum.FULL_DAY.name, text=ChildTypeEnum.FULL_DAY.value
            ),
            ft.dropdown.Option(
                key=ChildTypeEnum.SESSIONS.name, text=ChildTypeEnum.SESSIONS.value
            ),
        ],
        on_change=lambda e: update_edit_selected_child_type(e),
    )

    def update_edit_selected_child_type(e):
        nonlocal edit_selected_child_type
        if e.control.value == ChildTypeEnum.FULL_DAY.name:
            edit_selected_child_type = ChildTypeEnum.FULL_DAY
        elif e.control.value == ChildTypeEnum.SESSIONS.name:
            edit_selected_child_type = ChildTypeEnum.SESSIONS

    def edit_increment_age(e):
        nonlocal edit_age_counter
        edit_age_counter += 1
        edit_child_age.value = str(edit_age_counter)
        page.update()

    def edit_decrement_age(e):
        nonlocal edit_age_counter
        if edit_age_counter > 0:
            edit_age_counter -= 1
            edit_child_age.value = str(edit_age_counter)
        page.update()

    edit_age_controls = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=edit_decrement_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
            edit_child_age,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=edit_increment_age,
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

    def edit_handle_date_picker(e):
        nonlocal edit_selected_date
        if e.control.value:
            edit_selected_date = e.control.value
            edit_birth_date.value = edit_selected_date.strftime("%Y-%m-%d")
            page.update()

    def edit_open_date_picker(e):
        page.open(edit_date_picker)

    edit_date_picker_btn = ft.ElevatedButton(
        "اختر التاريخ", on_click=edit_open_date_picker
    )

    def edit_pick_photo(e):
        edit_file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    edit_photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=edit_pick_photo
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
            ft.TextButton("إلغاء", on_click=lambda e: close_edit_dialog()),
            ft.TextButton("حفظ", on_click=lambda e: save_edit_child()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Edit Date picker
    edit_date_picker = ft.DatePicker(
        on_change=edit_handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(edit_date_picker)

    def edit_handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal edit_photo_path
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
            page.update()

    # Edit Photo upload functionality
    edit_file_picker = ft.FilePicker(on_result=edit_handle_file_picker_result)
    page.overlay.append(edit_file_picker)

    def save_edit_child():
        nonlocal current_edit_child_id
        if not current_edit_child_id:
            show_error("لم يتم العثور على الطالب المراد تعديله!")
            return

        # Validate required fields
        if not edit_child_id.value:
            show_error("يجب إدخال رقم التعريفي!")
            return

        if not edit_child_name.value:
            show_error("يجب إدخال اسم الطالب!")
            return

        if not edit_child_age.value or int(edit_child_age.value) <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!")
            return

        if not edit_birth_date.value:
            show_error("يجب اختيار تاريخ الميلاد!")
            return

        # Create child DTO with updated data
        child_data = CreateChildDTO(
            id=int(edit_child_id.value),
            name=str(edit_child_name.value),
            age=int(edit_child_age.value),
            birth_date=datetime.datetime.strptime(
                edit_birth_date.value, "%Y-%m-%d"
            ).date(),
            phone_number=str(edit_phone.value) if edit_phone.value else None,
            father_job=str(edit_dad_job.value) if edit_dad_job.value else None,
            mother_job=str(edit_mum_job.value) if edit_mum_job.value else None,
            notes=(
                str(edit_additional_notes.value)
                if edit_additional_notes.value
                else None
            ),
            problems=str(edit_problem.value) if edit_problem.value else None,
            child_image=edit_photo_path,
            created_at=datetime.datetime.now(),  # Keep original created_at or update?
            child_type=edit_selected_child_type,
        )

        # Update child in database using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.update_child(
                    db, current_edit_child_id, child_data
                )

                if child_dto:
                    # Close dialog and refresh table
                    close_edit_dialog()
                    update_child_table()
                    show_success("تم تعديل بيانات الطالب بنجاح!")
                else:
                    show_error("فشل في تعديل بيانات الطالب!")
            except Exception as ex:
                show_error(f"خطأ في تعديل بيانات الطالب: {str(ex)}")

    def close_edit_dialog():
        page.close(edit_child_dialog)

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

    def open_edit_dialog(child_id):
        nonlocal current_edit_child_id
        current_edit_child_id = child_id
        with db_session() as db:
            child = ChildService.get_child_by_id(db, child_id)
            if child:
                # Populate edit form with child data
                edit_child_id.value = str(child.id)
                edit_child_name.value = child.name
                age_val = child.age or 3
                nonlocal edit_age_counter
                edit_age_counter = age_val
                edit_child_age.value = str(edit_age_counter)
                edit_birth_date.value = (
                    child.birth_date.strftime("%Y-%m-%d") if child.birth_date else ""
                )
                nonlocal edit_selected_date
                edit_selected_date = child.birth_date if child.birth_date else None
                edit_phone.value = child.phone_number or ""
                edit_dad_job.value = child.father_job or ""
                edit_mum_job.value = child.mother_job or ""
                edit_problem.value = child.problems or ""
                edit_additional_notes.value = child.notes or ""
                edit_additional_notes.value = ""
                nonlocal edit_photo_path
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
                nonlocal edit_selected_child_type
                edit_selected_child_type = child.child_type or ChildTypeEnum.FULL_DAY
                edit_child_type_dropdown.value = edit_selected_child_type.name

                page.open(edit_child_dialog)

    return edit_child_dialog, open_edit_dialog
