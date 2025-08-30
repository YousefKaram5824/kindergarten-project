import flet as ft
from database import db_session
from logic.child_logic import ChildService

PAGE_BGCOLOR = "#E3DCCC"
TEXT_COLOR = "#262626"
CARD_COLOR = ft.Colors.WHITE
CARD_BORDER_COLOR = ft.Colors.BLACK12
CARD_RADIUS = 12

def show_student_details(page: ft.Page, child_id: int):
    """Display the student details page"""
    page.clean()  

    with db_session() as db:
        child = ChildService.get_child_by_id(db, child_id)

    if not child:
        page.add(ft.Text("الطالب غير موجود!", size=20, color=ft.Colors.RED))
        page.update()
        return

    # Student photo
    photo = ft.Image(
        src=child.child_image if child.child_image else "",
        width=150,
        height=150,
        fit=ft.ImageFit.COVER,
        border_radius=ft.border_radius.all(CARD_RADIUS),
    )

    # Info cards
    info_cards = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"الاسم: {child.name}", size=18, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                        ft.Text(f"العمر: {child.age}", size=16, color=TEXT_COLOR),
                        ft.Text(f"تاريخ الميلاد: {child.birth_date}", size=16, color=TEXT_COLOR),
                        ft.Text(f"رقم التليفون: {child.phone_number}", size=16, color=TEXT_COLOR),
                        ft.Text(f"وظيفة الأب: {child.father_job}", size=16, color=TEXT_COLOR),
                        ft.Text(f"وظيفة الأم: {child.mother_job}", size=16, color=TEXT_COLOR),
                        ft.Text(f"ملاحظات: {child.notes}", size=16, color=TEXT_COLOR),
                    ],
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=20,
                bgcolor=CARD_COLOR,
                border=ft.border.all(1, CARD_BORDER_COLOR),
                border_radius=ft.border_radius.all(CARD_RADIUS),
                expand=True,
            )
        ],
        spacing=20,
    )

    # Back button
    back_button = ft.ElevatedButton(
        "العودة للطلاب",
        on_click=lambda e: page.go("/students")  
    )

    # Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    back_button,
                    ft.Row([photo, info_cards], spacing=30, alignment=ft.MainAxisAlignment.START),
                ],
                spacing=30,
            ),
            padding=20,
            expand=True,
        )
    )
    page.update()
