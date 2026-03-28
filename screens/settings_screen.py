"""
SettingsScreen — dark/light mode toggle, PIN change, data reset.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from utils.storage import hash_pin


class SettingsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme

        root = BoxLayout(orientation="vertical", padding=20, spacing=14)
        with root.canvas.before:
            Color(*t.get("bg"))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        back = Button(text="← Back", size_hint_y=None, height=40, background_normal="",
                      background_color=(0,0,0,0), color=t.get("accent"), font_size="14sp")
        back.bind(on_press=lambda b: setattr(self.manager, 'current', 'home'))
        root.add_widget(back)

        root.add_widget(Label(text="[b]Settings[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        # Theme toggle
        self._add_section(root, "Appearance", t)
        mode_text = "Switch to Light Mode" if t.mode == "dark" else "Switch to Dark Mode"
        theme_btn = Button(text=mode_text, size_hint_y=None, height=50,
                           background_normal="", background_color=t.get("surface"),
                           color=t.get("text_primary"), font_size="15sp")
        theme_btn.bind(on_press=lambda b: self._toggle_theme())
        root.add_widget(theme_btn)

        # PIN change
        self._add_section(root, "Security — Change PIN", t)
        self.old_pin = TextInput(hint_text="Current PIN (4 digits)", multiline=False, password=True,
                                  font_size="15sp", background_color=t.get("surface"),
                                  foreground_color=t.get("text_primary"),
                                  size_hint_y=None, height=44)
        self.new_pin = TextInput(hint_text="New PIN (4 digits)", multiline=False, password=True,
                                  font_size="15sp", background_color=t.get("surface"),
                                  foreground_color=t.get("text_primary"),
                                  size_hint_y=None, height=44)
        change_btn = Button(text="Change PIN", size_hint_y=None, height=48,
                            background_normal="", background_color=t.get("accent"),
                            color=(0.04, 0.21, 0.17, 1), font_size="15sp")
        change_btn.bind(on_press=lambda b: self._change_pin())
        root.add_widget(self.old_pin)
        root.add_widget(self.new_pin)
        root.add_widget(change_btn)

        self.status_lbl = Label(text="", font_size="13sp",
                                 color=t.get("danger"), size_hint_y=None, height=28)
        root.add_widget(self.status_lbl)

        # Security info
        self._add_section(root, "Security Info", t)
        root.add_widget(Label(
            text="✓ All data stored locally on device only\n"
                 "✓ No internet access by this app\n"
                 "✓ PIN stored as SHA-256 hash (not plain text)\n"
                 "✓ App locks on minimize/background\n"
                 "✓ Storage file is obfuscated",
            font_size="12sp",
            color=t.get("text_secondary"),
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=110,
        ))

        # Reset
        self._add_section(root, "Danger Zone", t)
        reset_btn = Button(text="Reset All Data", size_hint_y=None, height=48,
                           background_normal="", background_color=t.get("danger"),
                           color=(1, 1, 1, 1), font_size="15sp")
        reset_btn.bind(on_press=lambda b: self._reset_all())
        root.add_widget(reset_btn)

        self.add_widget(root)

    def _add_section(self, parent, title, t):
        parent.add_widget(Label(
            text=title.upper(),
            font_size="11sp",
            color=t.get("text_secondary"),
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=24,
        ))

    def _toggle_theme(self):
        app = App.get_running_app()
        app.theme.toggle()
        self.on_enter()

    def _change_pin(self):
        app = App.get_running_app()
        old = self.old_pin.text.strip()
        new = self.new_pin.text.strip()
        stored_hash = app.storage.get("pin_hash", "")

        if hash_pin(old) != stored_hash:
            self.status_lbl.color = app.theme.get("danger")
            self.status_lbl.text = "Current PIN is incorrect."
            return
        if len(new) != 4 or not new.isdigit():
            self.status_lbl.color = app.theme.get("danger")
            self.status_lbl.text = "New PIN must be exactly 4 digits."
            return
        app.storage.set("pin_hash", hash_pin(new))
        self.status_lbl.color = app.theme.get("accent")
        self.status_lbl.text = "PIN changed successfully!"
        self.old_pin.text = ""
        self.new_pin.text = ""

    def _reset_all(self):
        app = App.get_running_app()
        for key in ["tasks", "exams", "subjects", "pomo_log", "pomo_count_today", "streak"]:
            app.storage.delete(key)
        self.status_lbl.color = app.theme.get("accent")
        self.status_lbl.text = "Data reset. PIN kept."
