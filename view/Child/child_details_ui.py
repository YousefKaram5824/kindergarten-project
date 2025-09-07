import os
import flet as ft

# Local imports
from database import db_session
from logic.child_logic import ChildService


def show_child_details_page(page: ft.Page, child_id: int, current_user=None):
    """Show detailed page for a specific student"""
    # Fetch student data
    with db_session() as db:
        child = ChildService.get_child_by_id(db, child_id)
        if not child:
            # Show error and return to student table
            snackbar = ft.SnackBar(
                content=ft.Text("لم يتم العثور على الطالب"),
                bgcolor=ft.Colors.RED,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()
            return

    # Clear the page
    page.clean()

    # Create back button
    def go_back_to_student_table(e):
        """Navigate back to student table"""
        page.clean()
        # Import here to avoid circular imports
        from view.Child.child_ui import create_child_registration_tab
        from view.dashboard_ui import create_back_button

        student_tab = create_child_registration_tab(page, current_user)
        page.add(create_back_button(page, current_user))
        page.add(student_tab)
        page.update()

    back_button = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="العودة إلى قائمة الطلاب",
                on_click=go_back_to_student_table,
            ),
            ft.Text("العودة إلى قائمة الطلاب", size=16),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Student photo
    student_photo = ft.Image(
        src=(
            child.child_image
            if child.child_image and os.path.exists(child.child_image)
            else ""
        ),
        width=150,
        height=150,
        fit=ft.ImageFit.COVER,
        border_radius=ft.border_radius.all(10),
    )

    # Student details grouped by categories
    details_column = ft.Column(
        [
            ft.Text(
                "معلومات الطالب",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(),
            # Basic Information Section
            ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "المعلومات الأساسية",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "الاسم:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        child.name,
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "العمر:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        str(child.age) if child.age else "-",
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "تاريخ الميلاد:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        (
                                            child.birth_date.strftime("%Y-%m-%d")
                                            if child.birth_date
                                            else "-"
                                        ),
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                    ]
                ),
                padding=ft.padding.all(15),
                border=ft.border.all(1, ft.Colors.BLUE_100),
                border_radius=ft.border_radius.all(8),
                bgcolor=ft.Colors.BLUE_50,
                margin=ft.margin.only(bottom=10),
            ),
            # Contact Information Section
            ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "معلومات التواصل",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_700,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "رقم التليفون:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        (
                                            child.phone_number
                                            if child.phone_number
                                            else "-"
                                        ),
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                    ]
                ),
                padding=ft.padding.all(15),
                border=ft.border.all(1, ft.Colors.GREEN_100),
                border_radius=ft.border_radius.all(8),
                bgcolor=ft.Colors.GREEN_50,
                margin=ft.margin.only(bottom=10),
            ),
            # Family Information Section
            ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "معلومات العائلة",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ORANGE_700,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "وظيفة الأب:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        child.father_job if child.father_job else "-",
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "وظيفة الأم:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        child.mother_job if child.mother_job else "-",
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                    ]
                ),
                padding=ft.padding.all(15),
                border=ft.border.all(1, ft.Colors.ORANGE_100),
                border_radius=ft.border_radius.all(8),
                bgcolor=ft.Colors.ORANGE_50,
                margin=ft.margin.only(bottom=10),
            ),
            # Program Information Section
            ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "معلومات البرنامج",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PURPLE_700,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "نوع الطالب:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        (
                                            child.child_type.value
                                            if child.child_type
                                            else "-"
                                        ),
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "تاريخ التسجيل:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        (
                                            child.created_at.strftime("%Y-%m-%d")
                                            if child.created_at
                                            else "-"
                                        ),
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text(
                                        "وقت التسجيل:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                        width=120,
                                    ),
                                    ft.Text(
                                        (
                                            child.created_at.strftime("%H:%M")
                                            if child.created_at
                                            else "-"
                                        ),
                                        size=16,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                    ]
                ),
                padding=ft.padding.all(15),
                border=ft.border.all(1, ft.Colors.PURPLE_100),
                border_radius=ft.border_radius.all(8),
                bgcolor=ft.Colors.PURPLE_50,
                margin=ft.margin.only(bottom=10),
            ),
            # Additional Information Section
            ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "معلومات إضافية",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.TEAL_700,
                        ),
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(
                                        "الملاحظات:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            child.notes if child.notes else "-",
                                            size=14,
                                            text_align=ft.TextAlign.RIGHT,
                                        ),
                                        padding=ft.padding.all(10),
                                        border=ft.border.all(1, ft.Colors.GREY_300),
                                        border_radius=ft.border_radius.all(5),
                                        bgcolor=ft.Colors.WHITE,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(
                                        "المشكلة:",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            child.problems if child.problems else "-",
                                            size=14,
                                            text_align=ft.TextAlign.RIGHT,
                                        ),
                                        padding=ft.padding.all(10),
                                        border=ft.border.all(1, ft.Colors.GREY_300),
                                        border_radius=ft.border_radius.all(5),
                                        bgcolor=ft.Colors.WHITE,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=ft.padding.symmetric(vertical=5),
                        ),
                    ]
                ),
                padding=ft.padding.all(15),
                border=ft.border.all(1, ft.Colors.TEAL_100),
                border_radius=ft.border_radius.all(8),
                bgcolor=ft.Colors.TEAL_50,
                margin=ft.margin.only(bottom=10),
                expand=True,
            ),
        ],
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Main layout
    main_content = ft.Column(
        [
            back_button,
            ft.Divider(),
            ft.Row(
                [
                    ft.Container(
                        content=student_photo,
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20),
                    ),
                    ft.Container(
                        content=details_column,
                        expand=True,
                        padding=ft.padding.all(20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            ),
        ],
        spacing=20,
        expand=True,
    )

    # Add to page
    page.add(main_content)
    page.update()
