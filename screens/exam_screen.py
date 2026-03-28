"""
ExamScreen — add exam dates and see live countdowns.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from datetime import date, datetime


class ExamScreen(Screen):
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

        root.add_widget(Label(text="[b]Exam Countdown[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        # Add exam form
        form = BoxLayout(orientation="vertical", size_hint_y=None, height=130, spacing=8)
        self.exam_name_input = TextInput(hint_text="Exam name (e.g. Computer Networks)", multiline=False,
                                         font_size="14sp", background_color=t.get("surface"),
                                         foreground_color=t.get("text_primary"), size_hint_y=None, height=44)
        self.exam_date_input = TextInput(hint_text="Date (YYYY-MM-DD)", multiline=False,
                                          font_size="14sp", background_color=t.get("surface"),
                                          foreground_color=t.get("text_primary"), size_hint_y=None, height=44)
        add_btn = Button(text="Add Exam", size_hint_y=None, height=44,
                         background_normal="", background_color=t.get("accent"),
                         color=(0.04, 0.21, 0.17, 1), font_size="14sp")
        add_btn.bind(on_press=lambda b: self._add_exam())
        form.add_widget(self.exam_name_input)
        form.add_widget(self.exam_date_input)
        form.add_widget(add_btn)
        root.add_widget(form)

        self.status_lbl = Label(text="", font_size="12sp",
                                 color=t.get("danger"), size_hint_y=None, height=22)
        root.add_widget(self.status_lbl)

        scroll = ScrollView()
        box = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None, padding=(0, 4))
        box.bind(minimum_height=box.setter("height"))

        exams = app.storage.get("exams", [])
        today = date.today()
        if not exams:
            box.add_widget(Label(text="No exams added yet.", font_size="14sp",
                                 color=t.get("text_secondary"), size_hint_y=None, height=50))
        else:
            for i, exam in enumerate(exams):
                card = self._exam_card(exam, i, today, t)
                box.add_widget(card)

        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _exam_card(self, exam, idx, today, t):
        try:
            exam_date = date.fromisoformat(exam["date"])
            delta = (exam_date - today).days
            if delta < 0:
                countdown = "Past"
                color = t.get("text_secondary")
            elif delta == 0:
                countdown = "TODAY!"
                color = t.get("danger")
            elif delta <= 3:
                countdown = f"{delta} day{'s' if delta != 1 else ''} left!"
                color = t.get("warning")
            else:
                countdown = f"{delta} days left"
                color = t.get("accent")
        except Exception:
            countdown = "Invalid date"
            color = t.get("danger")

        card = BoxLayout(size_hint_y=None, height=70, padding=(14, 0), spacing=10)
        with card.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
        card.bind(pos=lambda w, *a: self._redraw(w, t), size=lambda w, *a: self._redraw(w, t))

        info = BoxLayout(orientation="vertical")
        info.add_widget(Label(text=exam["name"], font_size="15sp",
                               color=t.get("text_primary"), halign="left", text_size=(None, None)))
        info.add_widget(Label(text=exam["date"], font_size="12sp",
                               color=t.get("text_secondary"), halign="left", text_size=(None, None)))
        card.add_widget(info)

        card.add_widget(Label(text=countdown, font_size="14sp", color=color,
                               halign="right", text_size=(None, None)))

        del_btn = Button(text="✕", size_hint_x=None, width=40, background_normal="",
                         background_color=t.get("danger"), color=(1, 1, 1, 1), font_size="14sp")
        del_btn.bind(on_press=lambda b, i=idx: self._delete_exam(i))
        card.add_widget(del_btn)
        return card

    def _redraw(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[10])

    def _add_exam(self):
        app = App.get_running_app()
        name = self.exam_name_input.text.strip()
        date_str = self.exam_date_input.text.strip()
        if not name or not date_str:
            self.status_lbl.text = "Fill in both fields."
            return
        try:
            date.fromisoformat(date_str)
        except ValueError:
            self.status_lbl.text = "Use format YYYY-MM-DD (e.g. 2026-04-15)"
            return
        exams = app.storage.get("exams", [])
        exams.append({"name": name, "date": date_str})
        app.storage.set("exams", exams)
        self.on_enter()

    def _delete_exam(self, idx):
        app = App.get_running_app()
        exams = app.storage.get("exams", [])
        if 0 <= idx < len(exams):
            exams.pop(idx)
            app.storage.set("exams", exams)
        self.on_enter()
