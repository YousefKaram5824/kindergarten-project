import flet as ft
import time
import asyncio

# Local imports
from view.Authentication.auth_ui import set_show_main_system_callback, show_login_page
from database import db_session
from view.financial_ui import create_financial_tab
from view.Inventory.inventory_ui import create_inventory_tab
from view.reports_ui import create_reports_tab
from view.Child.child_ui import create_child_registration_tab
from view.daily_visit_ui import create_daily_visit_tab
from logic.child_logic import ChildService
from logic.tool_for_sale_logic import ToolForSaleService
from logic.training_tool_logic import TrainingToolService
from logic.uniform_for_sale_logic import UniformForSaleService
from logic.book_for_sale_logic import BookForSaleService
from logic.user_logic import UserService


class HoverNavigationRail(ft.Container):
    def __init__(self, destinations, on_change, **kwargs):
        super().__init__(**kwargs)
        self.destinations = destinations
        self.on_change = on_change
        self.is_expanded = False
        self.collapse_timer = None

        # Create the navigation rail
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE,
            min_width=60,
            min_extended_width=80,
            group_alignment=0.0,  # Center alignment
            destinations=destinations,
            on_change=on_change,
        )

        # Set initial content
        self.content = self.nav_rail
        self.width = 60
        self.bgcolor = ft.Colors.GREY_100
        self.padding = 0
        self.margin = 0
        self.border_radius = 0

        # Add hover functionality
        self.on_hover = self.handle_hover
        self.hovered = False  # Track hover state

    def handle_hover(self, e):
        if e.data == "true":
            # Mouse entered - expand
            self.hovered = True
            if self.collapse_timer:
                self.collapse_timer.cancel()
                self.collapse_timer = None
            self.expand_rail()
        else:
            # Mouse left - collapse after delay
            self.hovered = False
            self.collapse_rail()

    def expand_rail(self):
        if not self.is_expanded:
            self.is_expanded = True
            self.nav_rail.label_type = ft.NavigationRailLabelType.ALL
            self.width = 100
            self.animate = ft.Animation(
                duration=300, curve=ft.AnimationCurve.EASE_IN_OUT
            )
            self.update()

    def collapse_rail(self):
        if self.is_expanded:
            self.is_expanded = False
            self.nav_rail.label_type = ft.NavigationRailLabelType.NONE
            self.width = 60
            self.animate = ft.Animation(
                duration=300, curve=ft.AnimationCurve.EASE_IN_OUT_BACK
            )
            self.update()

    def did_mount(self):
        # Store page reference when control is mounted
        self._page = self.page


class DigitalClock(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_text = ft.Text(
            time.strftime("%Y-%m-%d"),
            size=16,
            weight=ft.FontWeight.NORMAL,
            color=ft.Colors.GREY_600,
        )
        self.clock_text = ft.Text(
            time.strftime("%H:%M:%S"),
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREY_600,
        )
        self.content = ft.Column([self.date_text, self.clock_text], spacing=0)
        self.padding = ft.padding.only(right=10)

    def did_mount(self):
        # Store page reference when control is mounted
        self._page = self.page
        # Start timer when control is mounted to the page
        if self.page is not None:
            self.page.run_task(self.update_clock)

    async def update_clock(self):
        while True:
            current_time = time.strftime("%H:%M:%S")
            current_date = time.strftime("%Y-%m-%d")
            self.clock_text.value = current_time
            self.date_text.value = current_date
            self.update()
            await asyncio.sleep(1)


def create_dashboard(page: ft.Page, current_user):
    """Create and return the main dashboard"""
    # Clear login page
    page.clean()
    # Remove page padding and margins
    page.padding = 0
    page.spacing = 0

    # Set page title with current user info
    if current_user:
        page.title = f"لوحة تحكم نظام إدارة رياض الأطفال - {current_user.username}"
    else:
        page.title = "لوحة تحكم نظام إدارة رياض الأطفال - غير مسجل الدخول"

    # Data storage
    financial_records = []
    inventory_items = []

    # Create navigation destinations
    nav_destinations = [
        ft.NavigationRailDestination(
            icon=ft.Icons.HOME,
            selected_icon=ft.Icons.HOME,
            label="الرئيسية",
            padding=ft.padding.symmetric(vertical=5),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.PERSON,
            selected_icon=ft.Icons.PERSON,
            label="الأطفال",
            padding=ft.padding.symmetric(vertical=5),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.CALENDAR_TODAY,
            selected_icon=ft.Icons.CALENDAR_TODAY,
            label="الزيارات",
            padding=ft.padding.symmetric(vertical=5),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ACCOUNT_BALANCE,
            selected_icon=ft.Icons.ACCOUNT_BALANCE,
            label="المالية",
            padding=ft.padding.symmetric(vertical=5),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.INVENTORY,
            selected_icon=ft.Icons.INVENTORY,
            label="المخزون",
            padding=ft.padding.symmetric(vertical=5),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ANALYTICS,
            selected_icon=ft.Icons.ANALYTICS,
            label="التقارير",
            padding=ft.padding.symmetric(vertical=5),
        ),
    ]

    # Create custom hover navigation rail
    nav_rail = HoverNavigationRail(
        destinations=nav_destinations,
        on_change=lambda e: handle_navigation_change(
            e, page, current_user, financial_records, inventory_items
        ),
    )

    # Dashboard header with user info and clock
    header = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                icon_size=24,
                tooltip="العودة إلى تسجيل الدخول",
                on_click=lambda e: back_to_login(page),
            ),
            ft.Text(
                "لوحة تحكم نظام إدارة رياض الأطفال",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Container(expand=True),
            DigitalClock(),  # Digital clock added here
            ft.Text(
                f"مرحباً: {current_user.username if current_user else 'زائر'}",
                size=16,
                color=ft.Colors.GREY_600,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Dashboard statistics cards with RTL alignment
    stats_cards = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PEOPLE, size=40, color=ft.Colors.BLUE),
                    ft.Text(
                        "0",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "الأطفال المسجلين", size=14, text_align=ft.TextAlign.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=160,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(1, ft.Colors.BLUE_100),
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.ACCOUNT_BALANCE_WALLET,
                        size=40,
                        color=ft.Colors.GREEN,
                    ),
                    ft.Text(
                        "0",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "الإيرادات الشهرية", size=14, text_align=ft.TextAlign.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=160,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.GREEN_50,
            border=ft.border.all(1, ft.Colors.GREEN_100),
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.INVENTORY_2, size=40, color=ft.Colors.ORANGE),
                    ft.Text(
                        "0",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text("عناصر المخزون", size=14, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=160,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.ORANGE_50,
            border=ft.border.all(1, ft.Colors.ORANGE_100),
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.SCHOOL, size=40, color=ft.Colors.TEAL),
                    ft.Text(
                        "0",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "أطفال اليوم الكامل", size=14, text_align=ft.TextAlign.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=160,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.TEAL_50,
            border=ft.border.all(1, ft.Colors.TEAL_100),
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ACCESS_TIME, size=40, color=ft.Colors.AMBER),
                    ft.Text(
                        "0",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text("أطفال الجلسات", size=14, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=160,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.AMBER_50,
            border=ft.border.all(1, ft.Colors.AMBER_100),
        ),
    ]

    # Add users card for admin users
    if current_user and current_user.role == "admin":
        stats_cards.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.ADMIN_PANEL_SETTINGS,
                            size=40,
                            color=ft.Colors.PURPLE,
                        ),
                        ft.Text(
                            "0",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text("المستخدمين", size=14, text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=160,
                height=160,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.PURPLE_50,
                border=ft.border.all(1, ft.Colors.PURPLE_100),
            )
        )

    stats_row = ft.Row(
        stats_cards,
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    # Main content area - restructured to stick everything at the top
    content_area = ft.Column(
        [
            ft.Text("مرحباً بك في لوحة التحكم", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("هنا يمكنك إدارة جميع جوانب رياض الأطفال بسهولة", size=16),
            ft.Divider(),
            ft.Text("الإجراءات السريعة:", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "تسجيل طفل جديد",
                        icon=ft.Icons.PERSON_ADD,
                        on_click=lambda e: show_child_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                    ),
                    ft.ElevatedButton(
                        "إضافة سجل مالي",
                        icon=ft.Icons.ADD_BUSINESS,
                        on_click=lambda e: show_financial_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                    ),
                    ft.ElevatedButton(
                        "إدارة المخزون",
                        icon=ft.Icons.INVENTORY,
                        on_click=lambda e: show_inventory_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(),
            stats_row,
        ],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.START,  # ✅ stick to top
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # Main layout
    main_layout = ft.Row(
        [
            nav_rail,
            ft.Container(
                content=ft.Column(
                    [header, ft.Divider(), content_area],
                    alignment=ft.MainAxisAlignment.START,  # ✅ stick to top
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=0,
                margin=0,
            ),
        ],
        expand=True,
    )

    # Update statistics
    update_dashboard_stats(stats_row)

    return main_layout


def update_dashboard_stats(stats_row):
    """Update dashboard statistics with real data"""
    try:
        # Get childs count using ChildService
        with db_session() as db:
            childs = ChildService.get_all_children(db)
            childs_count = len(childs)

            # Get total inventory count from all categories
            training_tools = TrainingToolService.get_all_tools(db)
            tools_for_sale = ToolForSaleService.get_all_tools(db)
            uniforms = UniformForSaleService.get_all_uniforms(db)
            books = BookForSaleService.get_all_books(db)
            inventory_count = (
                len(training_tools) + len(tools_for_sale) + len(uniforms) + len(books)
            )

            # Get counts by child type
            full_day_count = ChildService.get_full_day_children_count(db)
            sessions_count = ChildService.get_sessions_children_count(db)

            # Update stats cards
            stats_row.controls[0].content.controls[1].value = str(childs_count)
            stats_row.controls[2].content.controls[1].value = str(inventory_count)
            stats_row.controls[3].content.controls[1].value = str(full_day_count)
            stats_row.controls[4].content.controls[1].value = str(sessions_count)

            # Update users count for admin users (if users card exists)
            if len(stats_row.controls) > 5:
                users = UserService.get_all_users(db)
                users_count = len(users)
                stats_row.controls[5].content.controls[1].value = str(users_count)

    except Exception as e:
        print(f"Error updating dashboard stats: {e}")


def handle_navigation_change(e, page, current_user, financial_records, inventory_items):

    index = e.control.selected_index
    if index == 0:  # Home
        show_dashboard(page, current_user)
    elif index == 1:  # childs
        show_child_tab(page, current_user, financial_records, inventory_items)
    elif index == 2:  # Daily Visits
        show_daily_visit_tab(page, current_user, financial_records, inventory_items)
    elif index == 3:  # Financial
        show_financial_tab(page, current_user, financial_records, inventory_items)
    elif index == 4:  # Inventory
        show_inventory_tab(page, current_user, financial_records, inventory_items)
    elif index == 5:  # Reports
        show_reports_tab(page, current_user, financial_records, inventory_items)


def show_dashboard(page, current_user):
    """Show the main dashboard"""
    page.clean()
    dashboard = create_dashboard(page, current_user)
    page.add(dashboard)
    page.update()


def show_child_tab(page, current_user, financial_records, inventory_items):
    """Show child registration tab"""
    page.clean()
    page.padding = ft.padding.only(right=20)
    child_tab = create_child_registration_tab(page)
    page.add(create_back_button(page, current_user))
    page.add(child_tab)
    page.update()


def show_daily_visit_tab(page, current_user, financial_records, inventory_items):
    """Show daily visit management tab"""
    page.clean()
    page.padding = ft.padding.only(right=20)
    daily_visit_tab = create_daily_visit_tab(page, current_user)
    page.add(create_back_button(page, current_user))
    page.add(daily_visit_tab)
    page.update()


def show_financial_tab(page, current_user, financial_records, inventory_items):
    """Show financial management tab"""
    page.clean()
    page.padding = ft.padding.only(right=20)
    financial_tab = create_financial_tab(page)
    page.add(create_back_button(page, current_user))
    page.add(financial_tab)
    page.update()


def show_inventory_tab(page, current_user, financial_records, inventory_items):
    """Show inventory management tab"""
    page.clean()
    page.padding = ft.padding.only(right=20)
    inventory_tab = create_inventory_tab(page)
    page.add(create_back_button(page, current_user))
    page.add(inventory_tab)
    page.update()


def show_reports_tab(page, current_user, financial_records, inventory_items):
    """Show reports tab"""
    page.clean()
    page.padding = ft.padding.only(right=20)
    reports_tab = create_reports_tab(page, financial_records, inventory_items)
    page.add(create_back_button(page, current_user))
    page.add(reports_tab)
    page.update()


def create_back_button(page, current_user):
    """Create back button to return to dashboard"""
    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="العودة إلى لوحة التحكم",
                on_click=lambda e: show_dashboard(page, current_user),
            ),
            ft.Text("العودة إلى لوحة التحكم", size=16),
        ]
    )


def back_to_login(page: ft.Page):
    """Return to login page"""
    page.clean()
    show_login_page(page)


def show_main_system(page: ft.Page, current_user):
    """Show the main system with dashboard"""
    show_dashboard(page, current_user)


# Set the callback for showing main system
set_show_main_system_callback(show_main_system)
