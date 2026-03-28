"""
SubjectsScreen — track study progress per subject with tap-to-increment.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App


DEFAULT_SUBJECTS = [
    {"name": "Computer Networks", "pct": 0, "color": (0.22, 0.54, 0.87, 1)},
    {"name": "Artificial Intelligence", "pct": 0, "color": (0.11, 0.62, 0.46, 1)},
    {"name": ".NET Programming", "pct": 0, "color": (0.47, 0.46, 0.87, 1)},
    {"name": "Software Engineering", "pct": 0, "color": (0.83, 0.33, 0.49, 1)},
    {"name": "DBMS", "pct": 0, "color": (0.73, 0.46, 0.09, 1)},
    {"name": "IoT", "pct": 0, "color": (0.60, 0.29, 0.58, 1)},
    {"name": "Data Science", "pct": 0, "color": (0.23, 0.62, 0.77, 1)},
]


class SubjectsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)
        with root.canvas.before:
            Color(*t.get("bg"))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        back = Button(text="← Back", size_hint_y=None, height=40, background_normal="",
                      background_color=(0,0,0,0), color=t.get("accent"), font_size="14sp")
        back.bind(on_press=lambda b: setattr(self.manager, 'current', 'home'))
        root.add_widget(back)

        root.add_widget(Label(text="[b]Subject Progress[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        root.add_widget(Label(text="Tap +5 or -5 to update. Long-press to reset.",
                              font_size="12sp", color=t.get("text_secondary"),
                              size_hint_y=None, height=24))

        scroll = ScrollView()
        box = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None, padding=(0, 4))
        box.bind(minimum_height=box.setter("height"))

        subjects = app.storage.get("subjects", DEFAULT_SUBJECTS)
        for i, subj in enumerate(subjects):
            card = self._subject_card(subj, i, t)
            box.add_widget(card)

        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _subject_card(self, subj, idx, t):
        card = BoxLayout(orientation="vertical", size_hint_y=None, height=90, padding=12, spacing=6)
        with card.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
        card.bind(pos=lambda w, *a: self._redraw(w, t), size=lambda w, *a: self._redraw(w, t))

        top_row = BoxLayout(size_hint_y=None, height=28)
        top_row.add_widget(Label(text=subj["name"], font_size="14sp",
                                 color=t.get("text_primary"), halign="left", text_size=(None, None)))
        top_row.add_widget(Label(text=f"{subj['pct']}%", font_size="14sp",
                                 color=t.get("accent"), halign="right", text_size=(None, None)))
        card.add_widget(top_row)

        # Progress bar background
        bar_bg = BoxLayout(size_hint_y=None, height=8)
        with bar_bg.canvas.before:
            Color(*t.get("border"))
            RoundedRectangle(pos=bar_bg.pos, size=bar_bg.size, radius=[4])
            # Filled portion
            Color(*subj.get("color", t.get("accent")))
            pct = max(0, min(100, subj["pct"])) / 100.0
            # Will be drawn dynamically via bind
        self._setup_bar(bar_bg, subj, t)
        card.add_widget(bar_bg)

        btn_row = BoxLayout(size_hint_y=None, height=32, spacing=8)
        minus_btn = Button(text="-5", size_hint_x=None, width=60,
                           background_normal="", background_color=t.get("card"),
                           color=t.get("text_primary"), font_size="13sp")
        minus_btn.bind(on_press=lambda b, i=idx: self._adjust(i, -5))
        plus_btn = Button(text="+5", size_hint_x=None, width=60,
                          background_normal="", background_color=t.get("accent"),
                          color=(0.04, 0.21, 0.17, 1), font_size="13sp")
        plus_btn.bind(on_press=lambda b, i=idx: self._adjust(i, 5))
        reset_btn = Button(text="Reset", size_hint_x=None, width=70,
                           background_normal="", background_color=t.get("danger"),
                           color=(1,1,1,1), font_size="12sp")
        reset_btn.bind(on_press=lambda b, i=idx: self._adjust(i, -999))
        btn_row.add_widget(minus_btn)
        btn_row.add_widget(plus_btn)
        btn_row.add_widget(reset_btn)
        btn_row.add_widget(Label())  # spacer
        card.add_widget(btn_row)

        return card

    def _setup_bar(self, bar_bg, subj, t):
        def update(*args):
            bar_bg.canvas.before.clear()
            with bar_bg.canvas.before:
                Color(*t.get("border"))
                RoundedRectangle(pos=bar_bg.pos, size=bar_bg.size, radius=[4])
                Color(*subj.get("color", t.get("accent")))
                pct = max(0, min(100, subj["pct"])) / 100.0
                w = bar_bg.width * pct
                if w > 0:
                    RoundedRectangle(pos=bar_bg.pos, size=(w, bar_bg.height), radius=[4])
        bar_bg.bind(pos=update, size=update)

    def _redraw(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[10])

    def _adjust(self, idx, delta):
        app = App.get_running_app()
        subjects = app.storage.get("subjects", DEFAULT_SUBJECTS)
        if 0 <= idx < len(subjects):
            current = subjects[idx]["pct"]
            if delta < -100:
                subjects[idx]["pct"] = 0
            else:
                subjects[idx]["pct"] = max(0, min(100, current + delta))
            app.storage.set("subjects", subjects)
        self.on_enter()
