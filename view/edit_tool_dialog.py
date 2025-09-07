import flet as ft
from view.message_handlers import show_success_message, show_error_message
from database import db_session
from logic.tool_for_sale_logic import ToolForSaleService
from DTOs.tool_for_sale_dto import UpdateToolForSaleDTO


def create_edit_tool_dialog(page: ft.Page, update_callback):
    """Create and return the edit tool dialog and open function"""

    # Edit dialog variables
    current_edit_tool_id = None
    edit_item_name = ft.TextField(
        label="اسم الأداة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_item_number = ft.TextField(
        label="رقم الأداة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
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
    edit_inventory_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تعديل الأداة", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                edit_item_name,
                edit_item_number,
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
            ft.TextButton("حفظ", on_click=lambda e: update_inventory_item()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_edit_dialog(tool_id):
        nonlocal current_edit_tool_id
        with db_session() as db:
            tool = ToolForSaleService.get_tool(db, tool_id)
            if tool:
                current_edit_tool_id = tool_id
                edit_item_name.value = tool.tool_name or ""
                edit_item_number.value = tool.tool_number or ""
                edit_quantity.value = (
                    str(tool.quantity) if tool.quantity is not None else ""
                )
                edit_buy_price.value = (
                    str(tool.buy_price) if tool.buy_price is not None else ""
                )
                edit_sell_price.value = (
                    str(tool.sell_price) if tool.sell_price is not None else ""
                )
                edit_remaining.value = (
                    str(tool.remaining) if tool.remaining is not None else ""
                )
                edit_notes.value = tool.notes or ""
                page.open(edit_inventory_dialog)

    def close_edit_dialog():
        page.close(edit_inventory_dialog)

    def update_inventory_item():
        if current_edit_tool_id is None:
            show_error_message(page, "لم يتم العثور على الأداة المراد تعديلها")
            return

        try:
            # Parse the values
            quantity = int(edit_quantity.value) if edit_quantity.value else None
            buy_price = float(edit_buy_price.value) if edit_buy_price.value else None
            sell_price = float(edit_sell_price.value) if edit_sell_price.value else None
            remaining = int(edit_remaining.value) if edit_remaining.value else None

            tool_data = UpdateToolForSaleDTO(
                tool_name=(edit_item_name.value if edit_item_name.value else None),
                tool_number=(
                    edit_item_number.value if edit_item_number.value else None
                ),
                quantity=quantity,
                buy_price=buy_price,
                sell_price=sell_price,
                remaining=remaining,
                notes=edit_notes.value if edit_notes.value else None,
            )

            with db_session() as db:
                updated_tool = ToolForSaleService.update_tool(
                    db,
                    current_edit_tool_id,
                    tool_data,
                )

                if updated_tool:
                    close_edit_dialog()
                    update_callback()
                    show_success_message(page, "تم تحديث الأداة بنجاح!")
                else:
                    show_error_message(page, "فشل في تحديث الأداة")

        except ValueError as e:
            show_error_message(page, f"خطأ في البيانات المدخلة: {str(e)}")
        except Exception as e:
            show_error_message(page, f"خطأ غير متوقع: {str(e)}")

    return edit_inventory_dialog, open_edit_dialog
