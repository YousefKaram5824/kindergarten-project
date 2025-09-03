import flet as ft
from dataclasses import dataclass

# Local imports


@dataclass
class FinancialRecord:
    child_name: str
    monthly_fee: str
    bus_fee: str = "0"


def create_financial_tab(page: ft.Page):
    """Create and return the financial management tab"""
    # Financial Management Form in Arabic
    financial_child_name = ft.TextField(
        label="اسم الطالب", text_align=ft.TextAlign.RIGHT
    )
    monthly_fee = ft.TextField(
        label="المصروفات الشهرية",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
    )
    bus_fee = ft.TextField(
        label="أجرة الباص",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
    )

    # Data storage
    financial_records = []

    def add_financial_record(e):
        if financial_child_name.value and monthly_fee.value:
            record = FinancialRecord(
                child_name=financial_child_name.value,
                monthly_fee=monthly_fee.value,
                bus_fee=bus_fee.value,  # type: ignore
            )
            financial_records.append(record)
            financial_child_name.value = ""
            monthly_fee.value = ""
            bus_fee.value = ""
            update_financial_list()
            snackbar = ft.SnackBar(
                content=ft.Text("تم إضافة السجل المالي بنجاح!"),
                bgcolor=ft.Colors.GREEN,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()

    add_financial_btn = ft.ElevatedButton(
        "إضافة سجل مالي", on_click=add_financial_record
    )

    financial_list = ft.Column()

    def update_financial_list():
        financial_list.controls.clear()
        for record in financial_records:
            financial_list.controls.append(
                ft.ListTile(
                    title=ft.Text(record.child_name),
                    subtitle=ft.Text(
                        f"شهري: ${record.monthly_fee}, باص: ${record.bus_fee}"
                    ),
                )
            )

    return ft.Column(
        [
            ft.Text(
                "الإدارة المالية",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.RIGHT,
            ),
            ft.Divider(),
            financial_child_name,
            monthly_fee,
            bus_fee,
            ft.Row([add_financial_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text(
                "السجلات المالية:",
                size=18,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.RIGHT,
            ),
            financial_list,
        ],
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
