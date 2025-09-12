import flet as ft
import time
import asyncio
import math

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
from models import ChildTypeEnum


class AnimatedNavigationRail(ft.Container):
    def __init__(self, destinations, on_change, **kwargs):
        super().__init__(**kwargs)
        self.destinations = destinations
        self.on_change = on_change
        self.is_expanded = False
        self.selected_index = 0

        # Create gradient background
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.Colors.with_opacity(0.95, "#1e3c72"),
                ft.Colors.with_opacity(0.95, "#2a5298"),
                ft.Colors.with_opacity(0.95, "#1e3c72"),
            ],
        )

        # Create custom navigation items
        self.nav_items = []
        for i, dest in enumerate(destinations):
            item = self.create_nav_item(i, dest)
            self.nav_items.append(item)

        # Main content
        self.content = ft.Column(
            self.nav_items,
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
        )

        self.width = 80
        self.bgcolor = None
        self.gradient = self.gradient
        self.padding = ft.padding.symmetric(vertical=20, horizontal=10)
        self.border_radius = ft.border_radius.only(top_right=25, bottom_right=25)
        self.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(3, 0),
        )

        # Add hover functionality
        self.on_hover = self.handle_hover

    def create_nav_item(self, index, destination):
        is_selected = index == self.selected_index

        # Create animated container
        item_container = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        destination.selected_icon if is_selected else destination.icon,
                        size=28,
                        color=(
                            ft.Colors.WHITE
                            if is_selected
                            else ft.Colors.with_opacity(0.7, ft.Colors.WHITE)
                        ),
                    ),
                    ft.Text(
                        destination.label,
                        size=10,
                        weight=(
                            ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
                        ),
                        color=(
                            ft.Colors.WHITE
                            if is_selected
                            else ft.Colors.with_opacity(0.7, ft.Colors.WHITE)
                        ),
                        text_align=ft.TextAlign.CENTER,
                        visible=False,  # Initially hidden
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            width=60,
            height=60,
            border_radius=15,
            bgcolor=(
                ft.Colors.with_opacity(0.2, ft.Colors.WHITE) if is_selected else None
            ),
            border=(
                ft.border.all(2, ft.Colors.with_opacity(0.3, ft.Colors.WHITE))
                if is_selected
                else ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE))
            ),
            alignment=ft.alignment.center,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=lambda e, idx=index: self.select_item(idx),
            on_hover=lambda e, idx=index: self.hover_item(e, idx),
        )

        return item_container

    def hover_item(self, e, index):
        item = self.nav_items[index]
        if e.data == "true":
            item.scale = 1.05
            item.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.WHITE)
        else:
            item.scale = 1.0
            if index != self.selected_index:
                item.bgcolor = None
        item.update()

    def select_item(self, index):
        # Update selection
        old_index = self.selected_index
        self.selected_index = index

        # Update visual state
        self.update_selection(old_index, index)

        # Trigger callback
        class MockEvent:
            def __init__(self, control):
                self.control = control

        mock_event = MockEvent(self)
        mock_event.control.selected_index = index
        self.on_change(mock_event)

    def update_selection(self, old_index, new_index):
        # Update old item
        if 0 <= old_index < len(self.nav_items):
            old_item = self.nav_items[old_index]
            old_item.bgcolor = None
            old_item.border = ft.border.all(
                1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
            # Update icon and text colors
            icon_control = old_item.content.controls[0]
            text_control = old_item.content.controls[1]
            icon_control.color = ft.Colors.with_opacity(0.7, ft.Colors.WHITE)
            text_control.color = ft.Colors.with_opacity(0.7, ft.Colors.WHITE)
            text_control.weight = ft.FontWeight.NORMAL

        # Update new item
        if 0 <= new_index < len(self.nav_items):
            new_item = self.nav_items[new_index]
            new_item.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
            new_item.border = ft.border.all(
                2, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
            )
            # Update icon and text colors
            icon_control = new_item.content.controls[0]
            text_control = new_item.content.controls[1]
            icon_control.color = ft.Colors.WHITE
            text_control.color = ft.Colors.WHITE
            text_control.weight = ft.FontWeight.BOLD

        self.update()

    def handle_hover(self, e):
        if e.data == "true":
            self.expand_rail()
        else:
            self.collapse_rail()

    def expand_rail(self):
        if not self.is_expanded:
            self.is_expanded = True
            self.width = 120
            # Show labels
            for item in self.nav_items:
                item.content.controls[1].visible = True
            self.animate = ft.Animation(400, ft.AnimationCurve.EASE_OUT)
            self.update()

    def collapse_rail(self):
        if self.is_expanded:
            self.is_expanded = False
            self.width = 80
            # Hide labels
            for item in self.nav_items:
                item.content.controls[1].visible = False
            self.animate = ft.Animation(400, ft.AnimationCurve.EASE_IN)
            self.update()


class GlowingClock(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time_text = ft.Text(
            time.strftime("%H:%M"),
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        )

        self.seconds_text = ft.Text(
            time.strftime("%S"),
            size=18,
            weight=ft.FontWeight.W_300,
            color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
            text_align=ft.TextAlign.CENTER,
        )

        self.date_text = ft.Text(
            time.strftime("%A, %d %B"),
            size=14,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
            text_align=ft.TextAlign.CENTER,
        )

        # Gradient background container
        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.time_text,
                            ft.Text(
                                ":",
                                size=32,
                                color=ft.Colors.WHITE,
                                animate_opacity=ft.Animation(1000),
                            ),
                            self.seconds_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    self.date_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.with_opacity(0.2, "#667eea"),
                    ft.Colors.with_opacity(0.3, "#764ba2"),
                ],
            ),
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.2, ft.Colors.PURPLE),
                offset=ft.Offset(0, 4),
            ),
        )

        self.border_radius = 20

    def did_mount(self):
        self._page = self.page
        if self.page is not None:
            self.page.run_task(self.update_clock)

    async def update_clock(self):
        while True:
            current_time = time.strftime("%H:%M")
            current_seconds = time.strftime("%S")
            current_date = time.strftime("%A, %d %B")

            self.time_text.value = current_time
            self.seconds_text.value = current_seconds
            self.date_text.value = current_date

            # Animate colon blinking
            colon = self.content.content.controls[0].controls[1]
            colon.opacity = 0.3 if colon.opacity == 1.0 else 1.0

            self.update()
            await asyncio.sleep(1)


def create_glowing_stat_card(icon, value, title, gradient_colors, icon_color):
    """Create an enhanced glowing statistics card"""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(icon, size=50, color=icon_color),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.1, icon_color),
                    border_radius=25,
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.3, icon_color),
                        offset=ft.Offset(0, 5),
                    ),
                ),
                ft.Container(height=10),
                ft.Text(
                    str(value),
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    title,
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        width=190,
        height=180,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=gradient_colors,
        ),
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(0, 8),
        ),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        on_hover=lambda e: handle_card_hover(e),
    )


def handle_card_hover(e):
    """Handle hover effects on stat cards"""
    if e.data == "true":
        e.control.scale = 1.05
        e.control.shadow = ft.BoxShadow(
            spread_radius=4,
            blur_radius=25,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            offset=ft.Offset(0, 12),
        )
    else:
        e.control.scale = 1.0
        e.control.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(0, 8),
        )
    e.control.update()


def create_enhanced_button(text, icon, on_click, gradient_colors):
    """Create enhanced action buttons with gradients"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, size=20, color=ft.Colors.WHITE),
                ft.Text(
                    text, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        width=200,
        height=50,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=gradient_colors,
        ),
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, gradient_colors[0]),
            offset=ft.Offset(0, 4),
        ),
        on_click=on_click,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        on_hover=lambda e: handle_button_hover(e, gradient_colors),
    )


def handle_button_hover(e, gradient_colors):
    """Handle button hover effects"""
    if e.data == "true":
        e.control.scale = 1.02
        e.control.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.4, gradient_colors[0]),
            offset=ft.Offset(0, 6),
        )
    else:
        e.control.scale = 1.0
        e.control.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, gradient_colors[0]),
            offset=ft.Offset(0, 4),
        )
    e.control.update()


def create_dashboard(page: ft.Page, current_user):
    """Create the enhanced artistic dashboard"""
    page.clean()
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.with_opacity(0.95, "#0f0f23")

    # Set page title
    if current_user:
        page.title = f"نظام إدارة رياض الأطفال - {current_user.username}"
    else:
        page.title = "نظام إدارة رياض الأطفال"

    # Data storage
    financial_records = []
    inventory_items = []

    # Navigation destinations
    nav_destinations = [
        ft.NavigationRailDestination(
            icon=ft.Icons.DASHBOARD_OUTLINED,
            selected_icon=ft.Icons.DASHBOARD,
            label="الرئيسية",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SCHOOL_OUTLINED, selected_icon=ft.Icons.SCHOOL, label="الطلاب"
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.EVENT_OUTLINED, selected_icon=ft.Icons.EVENT, label="الزيارات"
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
            selected_icon=ft.Icons.ACCOUNT_BALANCE_WALLET,
            label="المالية",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.INVENTORY_2_OUTLINED,
            selected_icon=ft.Icons.INVENTORY_2,
            label="المخزون",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ANALYTICS_OUTLINED,
            selected_icon=ft.Icons.ANALYTICS,
            label="التقارير",
        ),
    ]

    # Enhanced navigation rail
    nav_rail = AnimatedNavigationRail(
        destinations=nav_destinations,
        on_change=lambda e: handle_navigation_change(
            e, page, current_user, financial_records, inventory_items
        ),
    )

    # Enhanced header with glassmorphism effect
    header = ft.Container(
        content=ft.Row(
            [
                # Logo and title section
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.CHILD_CARE, size=40, color=ft.Colors.WHITE
                            ),
                            width=60,
                            height=60,
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                            border_radius=30,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "نظام إدارة رياض الأطفال",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    "لوحة التحكم الذكية",
                                    size=12,
                                    color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(expand=True),
                # User info and clock section
                ft.Row(
                    [
                        GlowingClock(),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.PERSON,
                                                size=20,
                                                color=ft.Colors.WHITE,
                                            ),
                                            ft.Text(
                                                f"{current_user.username if current_user else 'زائر'}",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.WHITE,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(
                                        f"المستوى: {current_user.role if current_user else 'غير محدد'}",
                                        size=12,
                                        color=ft.Colors.with_opacity(
                                            0.8, ft.Colors.WHITE
                                        ),
                                    ),
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                            padding=15,
                            border_radius=15,
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_size=24,
                            icon_color=ft.Colors.WHITE,
                            tooltip="تسجيل الخروج",
                            on_click=lambda e: back_to_login(page),
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED),
                            hover_color=ft.Colors.with_opacity(0.3, ft.Colors.RED),
                        ),
                    ],
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[
                ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            ],
        ),
        padding=25,
        border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            offset=ft.Offset(0, 5),
        ),
    )

    # Enhanced statistics cards
    stats_cards = [
        create_glowing_stat_card(
            ft.Icons.SCHOOL,
            0,
            "الطلاب المسجلين",
            ["#667eea", "#764ba2"],
            ft.Colors.BLUE,
        ),
        create_glowing_stat_card(
            ft.Icons.ATTACH_MONEY,
            0,
            "الإيرادات الشهرية",
            ["#f093fb", "#f5576c"],
            ft.Colors.PINK,
        ),
        create_glowing_stat_card(
            ft.Icons.INVENTORY_2,
            0,
            "عناصر المخزون",
            ["#4facfe", "#00f2fe"],
            ft.Colors.CYAN,
        ),
        create_glowing_stat_card(
            ft.Icons.WB_SUNNY,
            0,
            "اليوم الكامل",
            ["#43e97b", "#38f9d7"],
            ft.Colors.GREEN,
        ),
        create_glowing_stat_card(
            ft.Icons.ACCESS_TIME,
            0,
            "الجلسات الفردية",
            ["#fa709a", "#fee140"],
            ft.Colors.ORANGE,
        ),
    ]

    # Add admin card if user is admin
    if current_user and current_user.role == "admin":
        stats_cards.append(
            create_glowing_stat_card(
                ft.Icons.ADMIN_PANEL_SETTINGS,
                0,
                "المستخدمين",
                ["#a8edea", "#fed6e3"],
                ft.Colors.PURPLE,
            )
        )

    # Enhanced quick actions
    quick_actions = ft.Column(
        [
            ft.Text(
                "الإجراءات السريعة",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            ft.Container(height=15),
            ft.Row(
                [
                    create_enhanced_button(
                        "تسجيل طالب جديد",
                        ft.Icons.PERSON_ADD,
                        lambda e: show_child_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                        ["#667eea", "#764ba2"],
                    ),
                    create_enhanced_button(
                        "إضافة سجل مالي",
                        ft.Icons.ADD_BUSINESS,
                        lambda e: show_financial_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                        ["#f093fb", "#f5576c"],
                    ),
                    create_enhanced_button(
                        "إدارة المخزون",
                        ft.Icons.INVENTORY,
                        lambda e: show_inventory_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                        ["#4facfe", "#00f2fe"],
                    ),
                ],
                spacing=20,
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
    )

    # Welcome section with animation
    welcome_section = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"أهلاً وسهلاً {current_user.username if current_user else 'بك'} 👋",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "إدارة شاملة ومتطورة لرياض الأطفال",
                                size=16,
                                color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=30,
                    border_radius=25,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[
                            ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                            ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                        ],
                    ),
                ),
                ft.Container(height=30),
                quick_actions,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
    )

    # Statistics section
    stats_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "إحصائيات النظام",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.Row(
                    stats_cards,
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
    )

    # Main content with enhanced scrolling
    content_area = ft.Column(
        [
            welcome_section,
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=2),
            stats_section,
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
    )

    # Main layout with enhanced background
    main_layout = ft.Container(
        content=ft.Row(
            [
                nav_rail,
                ft.Container(
                    content=ft.Column(
                        [
                            header,
                            ft.Container(
                                content=content_area,
                                expand=True,
                                padding=ft.padding.only(top=10),
                            ),
                        ],
                        spacing=0,
                    ),
                    expand=True,
                ),
            ],
            spacing=0,
        ),
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.2,
            colors=[
                ft.Colors.with_opacity(0.95, "#1a1a2e"),
                ft.Colors.with_opacity(0.98, "#16213e"),
                ft.Colors.with_opacity(1.0, "#0f0f23"),
            ],
        ),
        expand=True,
    )

    # Update statistics
    update_dashboard_stats(stats_cards)

    return main_layout


def update_dashboard_stats(stats_cards):
    """Update dashboard statistics with real data"""
    try:
        with db_session() as db:
            childs = ChildService.get_all_children(db)
            childs_count = len(childs)

            # Get inventory counts
            training_tools = TrainingToolService.get_all_tools(db)
            tools_for_sale = ToolForSaleService.get_all_tools(db)
            uniforms = UniformForSaleService.get_all_uniforms(db)
            books = BookForSaleService.get_all_books(db)
            inventory_count = (
                len(training_tools) + len(tools_for_sale) + len(uniforms) + len(books)
            )

            # Get counts by type
            full_day_count = ChildService.get_full_day_children_count(db)
            sessions_count = ChildService.get_sessions_children_count(db)

            # Update cards
            stats_cards[0].content.controls[1].controls[1].value = str(childs_count)
            stats_cards[2].content.controls[1].controls[1].value = str(inventory_count)
            stats_cards[3].content.controls[1].controls[1].value = str(full_day_count)
            stats_cards[4].content.controls[1].controls[1].value = str(sessions_count)

            # Update users count if admin card exists
            if len(stats_cards) > 5:
                users = UserService.get_all_users(db)
                users_count = len(users)
                stats_cards[5].content.controls[1].controls[1].value = str(users_count)

    except Exception as e:
        print(f"Error updating dashboard stats: {e}")


def handle_navigation_change(e, page, current_user, financial_records, inventory_items):
    index = e.control.selected_index
    if index == 0:  # Home
        show_dashboard(page, current_user)
    elif index == 1:  # Students
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
    page.bgcolor = ft.Colors.with_opacity(0.95, "#0f0f23")
    page.padding = ft.padding.only(right=20)
    child_tab = create_child_registration_tab(page)
    page.add(create_enhanced_back_button(page, current_user))
    page.add(child_tab)
    page.update()


def show_daily_visit_tab(page, current_user, financial_records, inventory_items):
    """Show daily visit management tab"""
    page.clean()
    page.bgcolor = ft.Colors.with_opacity(0.95, "#0f0f23")
    page.padding = ft.padding.only(right=20)
    daily_visit_tab = create_daily_visit_tab(page, current_user)
    page.add(create_enhanced_back_button(page, current_user))
    page.add(daily_visit_tab)
    page.update()


def show_financial_tab(page, current_user, financial_records, inventory_items):
    """Show financial management tab"""
    page.clean()
    page.bgcolor = ft.Colors.with_opacity(0.95, "#0f0f23")
    page.padding = ft.padding.only(right=20)
    financial_tab = create_financial_tab(page)
    page.add(create_enhanced_back_button(page, current_user))
    page.add(financial_tab)
    page.update()


def show_inventory_tab(page, current_user, financial_records, inventory_items):
    """Show inventory management tab"""
    page.clean()
    page.bgcolor = ft.Colors.with_opacity(0.95, "#0f0f23")
    page.padding = ft.padding.only(right=20)
    inventory_tab = create_inventory_tab(page)
    page.add(create_enhanced_back_button(page, current_user))
    page.add(inventory_tab)
    page.update()


def show_reports_tab(page, current_user, financial_records, inventory_items):
    """Show reports tab"""
    page.clean()
    page.bgcolor = ft.Colors.with_opacity(0.95, "#0f0f23")
    page.padding = ft.padding.only(right=20)
    reports_tab = create_reports_tab(page, financial_records, inventory_items)
    page.add(create_enhanced_back_button(page, current_user))
    page.add(reports_tab)
    page.update()


def create_enhanced_back_button(page, current_user):
    """Create enhanced back button with artistic styling"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ARROW_BACK, size=20, color=ft.Colors.WHITE
                            ),
                            ft.Text(
                                "العودة إلى لوحة التحكم",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=12,
                    border_radius=25,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=["#667eea", "#764ba2"],
                    ),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.3, "#667eea"),
                        offset=ft.Offset(0, 4),
                    ),
                    on_click=lambda e: show_dashboard(page, current_user),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    on_hover=lambda e: handle_back_button_hover(e),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
    )


def handle_back_button_hover(e):
    """Handle back button hover effects"""
    if e.data == "true":
        e.control.scale = 1.05
        e.control.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.4, "#667eea"),
            offset=ft.Offset(0, 6),
        )
    else:
        e.control.scale = 1.0
        e.control.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, "#667eea"),
            offset=ft.Offset(0, 4),
        )
    e.control.update()


def back_to_login(page: ft.Page):
    """Return to login page with transition effect"""

    # Create fade out effect
    def fade_and_redirect():
        page.clean()
        page.bgcolor = ft.Colors.BLACK
        show_login_page(page)
        page.update()

    # Add a small delay for smooth transition
    page.run_task(lambda: asyncio.sleep(0.2))
    fade_and_redirect()


def show_main_system(page: ft.Page, current_user):
    """Show the main system with enhanced dashboard"""
    show_dashboard(page, current_user)


# تكملة الكود من النسخة الأصلية مع التحسينات الفنية


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


# Set the callback for showing main system
set_show_main_system_callback(show_main_system)

# Additional helper functions for enhanced UI


def create_floating_notification(page, message, notification_type="info"):
    """Create floating notification with artistic styling"""
    colors = {
        "success": {
            "bg": ["#43e97b", "#38f9d7"],
            "icon": ft.Icons.CHECK_CIRCLE,
            "icon_color": ft.Colors.GREEN,
        },
        "error": {
            "bg": ["#ff6b6b", "#ee5a24"],
            "icon": ft.Icons.ERROR,
            "icon_color": ft.Colors.RED,
        },
        "warning": {
            "bg": ["#feca57", "#ff9ff3"],
            "icon": ft.Icons.WARNING,
            "icon_color": ft.Colors.ORANGE,
        },
        "info": {
            "bg": ["#74b9ff", "#0984e3"],
            "icon": ft.Icons.INFO,
            "icon_color": ft.Colors.BLUE,
        },
    }

    style = colors.get(notification_type, colors["info"])

    notification = ft.Container(
        content=ft.Row(
            [
                ft.Icon(style["icon"], color=ft.Colors.WHITE, size=24),
                ft.Text(
                    message,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=16,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=style["bg"],
        ),
        border_radius=25,
        padding=ft.padding.symmetric(horizontal=20, vertical=15),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, style["icon_color"]),
            offset=ft.Offset(0, 5),
        ),
        animate_position=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
    )

    # Add to page overlay
    page.overlay.append(notification)
    notification.top = 100
    notification.right = 20
    notification.opacity = 1.0
    page.update()

    # Auto hide after 3 seconds
    async def hide_notification():
        await asyncio.sleep(3)
        notification.opacity = 0.0
        page.update()
        await asyncio.sleep(0.5)
        if notification in page.overlay:
            page.overlay.remove(notification)
        page.update()

    page.run_task(hide_notification)


def create_loading_overlay(page, message="جاري التحميل..."):
    """Create artistic loading overlay"""
    loading_container = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(
                    width=60,
                    height=60,
                    stroke_width=4,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=20),
                ft.Text(
                    message,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=page.width,
        height=page.height,
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
        alignment=ft.alignment.center,
    )

    return loading_container


def create_enhanced_dialog(title, content, actions=None, dialog_type="info"):
    """Create enhanced dialog with artistic styling"""
    colors = {
        "success": ["#43e97b", "#38f9d7"],
        "error": ["#ff6b6b", "#ee5a24"],
        "warning": ["#feca57", "#ff9ff3"],
        "info": ["#74b9ff", "#0984e3"],
    }

    gradient_colors = colors.get(dialog_type, colors["info"])

    dialog_content = ft.Container(
        content=ft.Column(
            [
                # Title section with gradient background
                ft.Container(
                    content=ft.Text(
                        title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=gradient_colors,
                    ),
                    padding=20,
                    border_radius=ft.border_radius.only(top_left=20, top_right=20),
                ),
                # Content section
                ft.Container(
                    content=content,
                    padding=25,
                    bgcolor=ft.Colors.WHITE,
                ),
                # Actions section
                ft.Container(
                    content=ft.Row(
                        actions or [],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                    ),
                    padding=ft.padding.only(bottom=20, left=20, right=20),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.border_radius.only(
                        bottom_left=20, bottom_right=20
                    ),
                ),
            ],
            spacing=0,
        ),
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=3,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 10),
        ),
    )

    return ft.AlertDialog(
        content=dialog_content,
        content_padding=0,
    )


def create_animated_fab(icon, tooltip, on_click, gradient_colors):
    """Create animated floating action button"""
    return ft.FloatingActionButton(
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        bgcolor=gradient_colors[
            0
        ],  # Flet doesn't support gradients for FAB, use primary color
        foreground_color=ft.Colors.WHITE,
        shape=ft.RoundedRectangleBorder(radius=15),
        animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        on_hover=lambda e: handle_fab_hover(e, gradient_colors),
    )


def handle_fab_hover(e, gradient_colors):
    """Handle FAB hover effects"""
    if e.data == "true":
        e.control.scale = 1.1
        e.control.bgcolor = gradient_colors[1]
    else:
        e.control.scale = 1.0
        e.control.bgcolor = gradient_colors[0]
    e.control.update()


def create_data_table_enhanced(headers, rows, on_row_click=None):
    """Create enhanced data table with artistic styling"""
    # Create header
    header_cells = []
    for header in headers:
        header_cells.append(
            ft.DataColumn(
                ft.Container(
                    content=ft.Text(
                        header,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        size=14,
                    ),
                    padding=10,
                )
            )
        )

    # Create rows
    data_rows = []
    for i, row in enumerate(rows):
        cells = []
        for cell_data in row:
            cells.append(
                ft.DataCell(
                    ft.Container(
                        content=ft.Text(
                            str(cell_data),
                            color=ft.Colors.GREY_800,
                            size=13,
                        ),
                        padding=8,
                    )
                )
            )

        data_row = ft.DataRow(
            cells=cells,
            on_select_changed=lambda e, row_data=row: (
                on_row_click(row_data) if on_row_click else None
            ),
        )

        # Alternate row colors
        if i % 2 == 0:
            data_row.color = ft.Colors.with_opacity(0.05, ft.Colors.BLUE)

        data_rows.append(data_row)

    # Create table container
    table = ft.DataTable(
        columns=header_cells,
        rows=data_rows,
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY)),
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
        heading_row_height=60,
        data_row_height=50,
    )

    return ft.Container(
        content=table,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
        border_radius=15,
    )


def create_search_bar_enhanced(hint_text, on_change, on_submit=None):
    """Create enhanced search bar with artistic styling"""
    search_field = ft.TextField(
        hint_text=hint_text,
        prefix_icon=ft.Icons.SEARCH,
        border_radius=25,
        filled=True,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border_color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
        focused_border_color=ft.Colors.WHITE,
        hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE)),
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        cursor_color=ft.Colors.WHITE,
        on_change=on_change,
        on_submit=on_submit,
    )

    return ft.Container(
        content=search_field,
        width=400,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 3),
        ),
    )


def create_sidebar_menu(page, current_user, menu_items):
    """Create enhanced sidebar menu"""
    menu_controls = []

    for item in menu_items:
        menu_item = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(item.get("icon"), color=ft.Colors.WHITE, size=20),
                    ft.Text(
                        item.get("title", ""),
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W500,
                    ),
                ],
                spacing=15,
            ),
            padding=15,
            border_radius=12,
            on_click=item.get("on_click"),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e: handle_sidebar_item_hover(e),
        )
        menu_controls.append(menu_item)

    return ft.Container(
        content=ft.Column(menu_controls, spacing=8),
        width=250,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.with_opacity(0.9, "#1e3c72"),
                ft.Colors.with_opacity(0.9, "#2a5298"),
            ],
        ),
        padding=20,
        border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(3, 0),
        ),
    )


def handle_sidebar_item_hover(e):
    """Handle sidebar menu item hover effects"""
    if e.data == "true":
        e.control.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
        e.control.scale = 1.02
    else:
        e.control.bgcolor = None
        e.control.scale = 1.0
    e.control.update()


def create_progress_card(title, current_value, max_value, color_scheme):
    """Create enhanced progress card"""
    progress_percentage = (current_value / max_value) * 100 if max_value > 0 else 0

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            f"{current_value}/{max_value}",
                            size=14,
                            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                        ),
                    ]
                ),
                ft.Container(height=10),
                ft.ProgressBar(
                    value=progress_percentage / 100,
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                    color=ft.Colors.WHITE,
                    height=8,
                ),
                ft.Container(height=5),
                ft.Text(
                    f"{progress_percentage:.1f}%",
                    size=12,
                    color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                ),
            ]
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=color_scheme,
        ),
        padding=20,
        border_radius=15,
        width=250,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, color_scheme[0]),
            offset=ft.Offset(0, 5),
        ),
    )


# Enhanced theme configurations
def get_enhanced_theme():
    """Get enhanced theme configuration"""
    return ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        use_material3=True,
        visual_density=ft.VisualDensity.COMFORTABLE,
    )


def apply_page_animations(page):
    """Apply page-level animations and transitions"""
    page.theme = get_enhanced_theme()
    page.window.frameless = False
    page.window.title_bar_hidden = False
    page.window.title_bar_buttons_hidden = False
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Add custom CSS-like effects (if supported in future Flet versions)
    # This is a placeholder for future enhancements
    pass


# Enhanced utility functions
def format_currency(amount):
    """Format currency with Arabic locale"""
    if amount is None:
        return "0 جنيه"
    return f"{amount:,.0f} جنيه"


def format_date_arabic(date_obj):
    """Format date in Arabic"""
    if date_obj is None:
        return "غير محدد"

    months_arabic = {
        1: "يناير",
        2: "فبراير",
        3: "مارس",
        4: "أبريل",
        5: "مايو",
        6: "يونيو",
        7: "يوليو",
        8: "أغسطس",
        9: "سبتمبر",
        10: "أكتوبر",
        11: "نوفمبر",
        12: "ديسمبر",
    }

    return f"{date_obj.day} {months_arabic.get(date_obj.month, '')} {date_obj.year}"


def create_empty_state(icon, title, description, action_button=None):
    """Create artistic empty state display"""
    controls = [
        ft.Icon(
            icon,
            size=80,
            color=ft.Colors.with_opacity(0.5, ft.Colors.GREY),
        ),
        ft.Container(height=20),
        ft.Text(
            title,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.with_opacity(0.7, ft.Colors.GREY),
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(height=10),
        ft.Text(
            description,
            size=16,
            color=ft.Colors.with_opacity(0.6, ft.Colors.GREY),
            text_align=ft.TextAlign.CENTER,
        ),
    ]

    if action_button:
        controls.extend([ft.Container(height=30), action_button])

    return ft.Container(
        content=ft.Column(
            controls,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        padding=40,
        alignment=ft.alignment.center,
    )
