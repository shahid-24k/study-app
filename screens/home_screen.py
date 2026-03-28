"""
HomeScreen — main dashboard with navigation tiles.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from datetime import datetime


NAV_TILES = [
    ("🍅", "Pomodoro", "pomodoro"),
    ("✅", "Tasks", "tasks"),
    ("📚", "Subjects", "subjects"),
    ("📖", "Hadith", "hadith"),
    ("🕌", "Prayer Times", "prayer"),
    ("📅", "Exam Countdown", "exams"),
    ("⚙️", "Settings", "settings"),
]


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.clear_widgets()
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme

        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*t.get("bg"))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        # Header
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=110, padding=(20, 20, 20, 10))
        now = datetime.now()
        greeting = "Assalamu Alaikum" if now.hour < 12 else ("Good afternoon" if now.hour < 17 else "Good evening")
        header.add_widget(Label(
            text=f"[b]{greeting}, Shahid[/b]",
            markup=True, font_size="22sp",
            color=t.get("text_primary"),
            halign="left", text_size=(None, None),
        ))
        header.add_widget(Label(
            text=now.strftime("%A, %d %B %Y"),
            font_size="13sp",
            color=t.get("text_secondary"),
            halign="left", text_size=(None, None),
        ))
        root.add_widget(header)

        # Scroll area
        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", spacing=16, padding=(16, 8, 16, 24), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        # Stats row
        stats_row = GridLayout(cols=3, size_hint_y=None, height=90, spacing=10)
        stats_data = [
            ("Pomodoros", str(app.storage.get("pomo_count_today", 0))),
            ("Tasks Done", self._tasks_stat(app)),
            ("Streak", f"{app.storage.get('streak', 0)}d"),
        ]
        for lbl, val in stats_data:
            card = self._stat_card(val, lbl, t)
            stats_row.add_widget(card)
        content.add_widget(stats_row)

        # Nav grid
        nav = GridLayout(cols=2, spacing=12, size_hint_y=None)
        nav.bind(minimum_height=nav.setter("height"))
        for icon, name, screen in NAV_TILES:
            btn = self._nav_tile(icon, name, screen, t)
            nav.add_widget(btn)
        content.add_widget(nav)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def _tasks_stat(self, app):
        tasks = app.storage.get("tasks", [])
        done = sum(1 for t in tasks if t.get("done"))
        return f"{done}/{len(tasks)}"

    def _stat_card(self, value, label, t):
        box = BoxLayout(orientation="vertical", padding=8)
        with box.canvas.before:
            Color(*t.get("card"))
            RoundedRectangle(pos=box.pos, size=box.size, radius=[10])
        box.bind(
            pos=lambda w, p: self._redraw(w),
            size=lambda w, s: self._redraw(w),
        )
        box.add_widget(Label(text=f"[b]{value}[/b]", markup=True, font_size="20sp", color=t.get("accent")))
        box.add_widget(Label(text=label, font_size="11sp", color=t.get("text_secondary")))
        return box

    def _redraw(self, w):
        w.canvas.before.clear()
        app = App.get_running_app()
        t = app.theme
        with w.canvas.before:
            Color(*t.get("card"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[10])

    def _nav_tile(self, icon, name, screen_name, t):
        btn = Button(
            text=f"{icon}\n[b]{name}[/b]",
            markup=True,
            font_size="15sp",
            background_normal="",
            background_color=t.get("surface"),
            color=t.get("text_primary"),
            size_hint_y=None,
            height=100,
            border=(0, 0, 0, 0),
        )
        btn.bind(on_press=lambda b: self._goto(screen_name))
        return btn

    def _goto(self, name):
        self.manager.current = name
