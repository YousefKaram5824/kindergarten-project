import flet as ft
from view.message_handlers import show_success_message, show_error_message
from database import db_session
from logic.uniform_for_sale_logic import UniformForSaleService
from DTOs.uniform_for_sale_dto import UpdateUniformForSaleDTO


def create_edit_uniform_dialog(page: ft.Page, update_callback):
    """Create and return the edit uniform dialog and open function"""

    # Edit dialog variables
    current_edit_uniform_id = None
    edit_quantity = ft.TextField(
        label="الكمية",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_buy_price = ft.TextField(
        label="سعر الشراء",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_sell_price = ft.TextField(
        label="سعر البيع",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_remaining = ft.TextField(
        label="المتبقي",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_notes = ft.TextField(
        label="ملاحظات",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    # Edit inventory Dialog
    edit_uniform_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تعديل الزي", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                edit_quantity,
                edit_buy_price,
                edit_sell_price,
                edit_remaining,
                edit_notes,
            ],
            width=400,
            height=500,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: close_edit_dialog()),
            ft.TextButton("حفظ", on_click=lambda e: update_uniform_item()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_edit_dialog(uniform_id):
        nonlocal current_edit_uniform_id
        with db_session() as db:
            uniform = UniformForSaleService.get_uniform(db, uniform_id)
            if uniform:
                current_edit_uniform_id = uniform_id
                edit_quantity.value = (
                    str(uniform.quantity) if uniform.quantity is not None else ""
                )
                edit_buy_price.value = (
                    str(uniform.buy_price) if uniform.buy_price is not None else ""
                )
                edit_sell_price.value = (
                    str(uniform.sell_price) if uniform.sell_price is not None else ""
                )
                edit_remaining.value = (
                    str(uniform.remaining) if uniform.remaining is not None else ""
                )
                edit_notes.value = uniform.notes or ""
                page.open(edit_uniform_dialog)

    def close_edit_dialog():
        page.close(edit_uniform_dialog)

    def update_uniform_item():
        if current_edit_uniform_id is None:
            show_error_message(page, "لم يتم العثور على الزي المراد تعديله")
            return

        try:
            # Parse the values
            quantity = int(edit_quantity.value) if edit_quantity.value else None
            buy_price = float(edit_buy_price.value) if edit_buy_price.value else None
            sell_price = float(edit_sell_price.value) if edit_sell_price.value else None
            remaining = int(edit_remaining.value) if edit_remaining.value else None

            uniform_data = UpdateUniformForSaleDTO(
                quantity=quantity,
                buy_price=buy_price,
                sell_price=sell_price,
                remaining=remaining,
                notes=edit_notes.value if edit_notes.value else None,
            )

            with db_session() as db:
                updated_uniform = UniformForSaleService.update_uniform(
                    db,
                    current_edit_uniform_id,
                    uniform_data,
                )

                if updated_uniform:
                    close_edit_dialog()
                    update_callback()
                    show_success_message(page, "تم تحديث الزي بنجاح!")
                else:
                    show_error_message(page, "فشل في تحديث الزي")

        except ValueError as e:
            show_error_message(page, f"خطأ في البيانات المدخلة: {str(e)}")
        except Exception as e:
            show_error_message(page, f"خطأ غير متوقع: {str(e)}")

    return edit_uniform_dialog, open_edit_dialog
