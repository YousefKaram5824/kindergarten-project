import datetime
import os
import shutil
import flet as ft
from view.message_handlers import show_error_message, show_success_message

# Local imports
from database import db_session
from logic.training_tool_logic import TrainingToolService
from DTOs.training_tool_dto import CreateTrainingToolDTO

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8


def create_add_inventory_dialog(page: ft.Page, on_success_callback):
    """Create and return the add inventory dialog components"""

    # Form fields
    item_name = ft.TextField(
        label="اسم الأداة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    item_number = ft.TextField(
        label="رقم الأداة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    department = ft.TextField(
        label="القسم",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    purchase_date = ft.TextField(
        label="تاريخ الشراء",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=210,
    )
    selected_purchase_date = None
    notes = ft.TextField(
        label="ملاحظات",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    # Photo upload variables
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

    def handle_date_picker(e):
        nonlocal selected_purchase_date
        if e.control.value:
            selected_purchase_date = e.control.value
            purchase_date.value = selected_purchase_date.strftime("%Y-%m-%d")
            page.update()

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الأداة",
        )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الأداة", icon=ft.Icons.UPLOAD_FILE, on_click=pick_photo
    )

    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal photo_path
        if e.files:
            # Create tool_photos directory if it doesn't exist
            photos_dir = "tool_photos"
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Copy the file to tool_photos directory
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

    # Date picker for purchase date
    date_picker = ft.DatePicker(
        on_change=handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(date_picker)

    def add_inventory_item():
        # Validate required fields
        if not item_name.value:
            show_error_message(page, "يجب إدخال اسم الأداة!")
            return

        # Set default purchase date if not selected
        purchase_date_value = None
        if purchase_date.value:
            try:
                purchase_date_value = datetime.datetime.strptime(
                    purchase_date.value, "%Y-%m-%d"
                ).date()
            except ValueError:
                show_error_message(page, "صيغة تاريخ الشراء غير صحيحة!")
                return
        else:
            purchase_date_value = datetime.date.today()

        # Create DTO
        tool_data = CreateTrainingToolDTO(
            tool_name=item_name.value,
            tool_number=item_number.value if item_number.value else None,
            tool_image=photo_path,
            department=department.value if department.value else None,
            purchase_date=purchase_date_value,
            notes=notes.value if notes.value else None,
        )

        with db_session() as db:
            try:
                new_tool = TrainingToolService.create_tool(db, tool_data)
                if new_tool:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Call success callback to refresh table
                    on_success_callback()

                    show_success_message(page, "تم إضافة الأداة بنجاح!")
                else:
                    show_error_message(page, "فشل في إضافة الأداة!")
            except Exception as ex:
                show_error_message(page, f"خطأ في إضافة الأداة: {str(ex)}")

    def reset_form():
        nonlocal photo_path, selected_purchase_date
        item_name.value = ""
        item_number.value = ""
        department.value = ""
        purchase_date.value = ""
        selected_purchase_date = None
        notes.value = ""
        photo_path = None
        photo_preview.src = ""
        photo_preview.visible = False
        photo_status.value = "لم يتم اختيار صورة"
        photo_status.color = ft.Colors.GREY

    def close_dialog():
        page.close(add_inventory_dialog)

    # Add inventory Dialog - Matching child dialog style
    add_inventory_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة أداة جديدة", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                item_name,
                item_number,
                department,
                ft.Row(
                    [date_picker_btn, purchase_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                notes,
                ft.Container(
                    ft.Text(
                        "صورة الأداة:",
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
            height=500,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_inventory_item()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_add_inventory_dialog(e):
        page.open(add_inventory_dialog)

    return add_inventory_dialog, open_add_inventory_dialog
