import flet as ft
from view.message_handlers import show_error_message, show_success_message

# Local imports
from database import db_session
from logic.uniform_for_sale_logic import UniformForSaleService
from DTOs.uniform_for_sale_dto import CreateUniformForSaleDTO

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8


def create_add_uniform_dialog(page: ft.Page, on_success_callback):
    """Create and return the add uniform dialog components"""

    # Form fields
    quantity = ft.TextField(
        label="الكمية",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    buy_price = ft.TextField(
        label="سعر الشراء",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    sell_price = ft.TextField(
        label="سعر البيع",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    remaining = ft.TextField(
        label="المتبقي",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    notes = ft.TextField(
        label="ملاحظات",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    def add_uniform_item():
        # Validate required fields
        # Create DTO
        uniform_data = CreateUniformForSaleDTO(
            quantity=int(quantity.value) if quantity.value else None,
            buy_price=float(buy_price.value) if buy_price.value else None,
            sell_price=float(sell_price.value) if sell_price.value else None,
            remaining=int(remaining.value) if remaining.value else None,
            notes=notes.value if notes.value else None,
        )

        with db_session() as db:
            try:
                new_uniform = UniformForSaleService.create_uniform(db, uniform_data)
                if new_uniform:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Call success callback to refresh table
                    on_success_callback()

                    show_success_message(page, "تم إضافة الزي بنجاح!")
                else:
                    show_error_message(page, "فشل في إضافة الزي!")
            except Exception as ex:
                show_error_message(page, f"خطأ في إضافة الزي: {str(ex)}")

    def reset_form():
        quantity.value = ""
        buy_price.value = ""
        sell_price.value = ""
        remaining.value = ""
        notes.value = ""

    def close_dialog():
        page.close(add_uniform_dialog)

    # Add uniform Dialog
    add_uniform_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة زي جديد", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                quantity,
                buy_price,
                sell_price,
                remaining,
                notes,
            ],
            width=400,
            height=400,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_uniform_item()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_add_uniform_dialog(e):
        page.open(add_uniform_dialog)

    return add_uniform_dialog, open_add_uniform_dialog
