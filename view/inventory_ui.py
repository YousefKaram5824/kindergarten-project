import flet as ft
from dataclasses import dataclass

# Local imports


@dataclass
class InventoryItem:
    item_name: str
    quantity: str
    purchase_price: str


def create_inventory_tab(page: ft.Page):
    """Create and return the inventory management tab"""
    # Inventory Management Form in Arabic
    item_name = ft.TextField(label="اسم الأداة", text_align=ft.TextAlign.RIGHT)
    item_quantity = ft.TextField(
        label="الكمية",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
    )
    purchase_price = ft.TextField(
        label="سعر الشراء",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
    )

    inventory_items = []

    def add_inventory_item(e):
        if item_name.value and item_quantity.value:
            item = InventoryItem(
                item_name=item_name.value,
                quantity=item_quantity.value,
                purchase_price=purchase_price.value,
            )
            inventory_items.append(item)
            item_name.value = ""
            item_quantity.value = ""
            purchase_price.value = ""
            update_inventory_list()
            snackbar = ft.SnackBar(
                content=ft.Text("تم إضافة العنصر بنجاح!"),
                bgcolor=ft.Colors.GREEN,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()

    add_inventory_btn = ft.ElevatedButton("إضافة عنصر", on_click=add_inventory_item)

    inventory_list = ft.Column()

    def update_inventory_list():
        inventory_list.controls.clear()
        for item in inventory_items:
            inventory_list.controls.append(
                ft.ListTile(
                    title=ft.Text(item.item_name),
                    subtitle=ft.Text(
                        f"الكمية: {item.quantity}, السعر: ${item.purchase_price}"
                    ),
                )
            )

    return ft.Column(
        [
            ft.Text(
                "إدارة المخزون",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.RIGHT,
            ),
            ft.Divider(),
            item_name,
            item_quantity,
            purchase_price,
            ft.Row([add_inventory_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text(
                "عناصر المخزون:",
                size=18,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.RIGHT,
            ),
            inventory_list,
        ],
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
