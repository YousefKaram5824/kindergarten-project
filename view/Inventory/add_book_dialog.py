import flet as ft
from view.message_handlers import show_error_message, show_success_message

# Local imports
from database import db_session
from logic.book_for_sale_logic import BookForSaleService
from DTOs.book_for_sale_dto import CreateBookForSaleDTO

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8


def create_add_book_dialog(page: ft.Page, on_success_callback):
    """Create and return the add book dialog components"""

    # Form fields
    book_name = ft.TextField(
        label="اسم الكتاب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
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

    def add_book_item():
        # Validate required fields
        if not book_name.value:
            show_error_message(page, "يجب إدخال اسم الكتاب!")
            return

        # Create DTO
        book_data = CreateBookForSaleDTO(
            book_name=book_name.value,
            quantity=int(quantity.value) if quantity.value else None,
            buy_price=float(buy_price.value) if buy_price.value else None,
            sell_price=float(sell_price.value) if sell_price.value else None,
            remaining=int(remaining.value) if remaining.value else None,
            notes=notes.value if notes.value else None,
        )

        with db_session() as db:
            try:
                new_book = BookForSaleService.create_book(db, book_data)
                if new_book:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Call success callback to refresh table
                    on_success_callback()

                    show_success_message(page, "تم إضافة الكتاب بنجاح!")
                else:
                    show_error_message(page, "فشل في إضافة الكتاب!")
            except Exception as ex:
                show_error_message(page, f"خطأ في إضافة الكتاب: {str(ex)}")

    def reset_form():
        book_name.value = ""
        quantity.value = ""
        buy_price.value = ""
        sell_price.value = ""
        remaining.value = ""
        notes.value = ""

    def close_dialog():
        page.close(add_book_dialog)

    # Add book Dialog
    add_book_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة كتاب جديد", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                book_name,
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
            ft.TextButton("إضافة", on_click=lambda e: add_book_item()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_add_book_dialog(e):
        page.open(add_book_dialog)

    return add_book_dialog, open_add_book_dialog
