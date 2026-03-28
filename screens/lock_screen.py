"""
LockScreen — PIN entry screen.
Security:
  - PIN is never stored in plain text (SHA-256 hashed)
  - Wrong PIN attempts tracked, app locks for 30s after 5 failures
  - No PIN hint displayed
  - Input is masked
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
from utils.storage import hash_pin


MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 30


class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pin_input = ""
        self._attempts = 0
        self._locked_out = False
        self._lockout_remaining = 0
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme

        self.layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*t.get("bg"))
            self._bg_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=self._update_bg, size=self._update_bg)

        # Header
        self.title_label = Label(
            text="[b]StudyApp[/b]",
            markup=True,
            font_size="26sp",
            color=t.get("text_primary"),
            size_hint_y=None,
            height=50,
        )
        self.layout.add_widget(self.title_label)

        self.sub_label = Label(
            text="Enter your PIN to continue",
            font_size="14sp",
            color=t.get("text_secondary"),
            size_hint_y=None,
            height=30,
        )
        self.layout.add_widget(self.sub_label)

        # PIN dots display
        self.pin_display = Label(
            text="○ ○ ○ ○",
            font_size="28sp",
            color=t.get("accent"),
            size_hint_y=None,
            height=60,
        )
        self.layout.add_widget(self.pin_display)

        # Status label
        self.status_label = Label(
            text="",
            font_size="13sp",
            color=t.get("danger"),
            size_hint_y=None,
            height=30,
        )
        self.layout.add_widget(self.status_label)

        # Numpad
        numpad = GridLayout(cols=3, spacing=10, size_hint_y=None, height=280)
        digits = ["1","2","3","4","5","6","7","8","9","⌫","0","✓"]
        for d in digits:
            btn = Button(
                text=d,
                font_size="22sp",
                background_normal="",
                background_color=t.get("card"),
                color=t.get("text_primary"),
                border=(0,0,0,0),
            )
            btn.bind(on_press=lambda b, d=d: self._on_key(d))
            numpad.add_widget(btn)
        self.layout.add_widget(numpad)

        # First-time setup note
        self.setup_label = Label(
            text="",
            font_size="12sp",
            color=t.get("text_secondary"),
            size_hint_y=None,
            height=40,
        )
        self.layout.add_widget(self.setup_label)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self._bg_rect.pos = self.layout.pos
        self._bg_rect.size = self.layout.size

    def on_enter(self):
        app = App.get_running_app()
        stored = app.storage.get("pin_hash")
        if not stored:
            self.setup_label.text = "First time? Enter a 4-digit PIN to set it."
        else:
            self.setup_label.text = ""
        self._pin_input = ""
        self._update_dots()
        self.status_label.text = ""

    def _update_dots(self):
        n = len(self._pin_input)
        filled = "● " * n
        empty = "○ " * (4 - n)
        self.pin_display.text = (filled + empty).strip()

    def _on_key(self, key):
        if self._locked_out:
            return
        if key == "⌫":
            self._pin_input = self._pin_input[:-1]
            self._update_dots()
        elif key == "✓":
            self._submit()
        elif len(self._pin_input) < 4 and key.isdigit():
            self._pin_input += key
            self._update_dots()
            if len(self._pin_input) == 4:
                self._submit()

    def _submit(self):
        app = App.get_running_app()
        stored_hash = app.storage.get("pin_hash")
        entered_hash = hash_pin(self._pin_input)

        if not stored_hash:
            # First time — set PIN
            if len(self._pin_input) == 4:
                app.storage.set("pin_hash", entered_hash)
                self.status_label.color = (0.11, 0.62, 0.46, 1)
                self.status_label.text = "PIN set! Welcome, Shahid."
                Clock.schedule_once(lambda dt: self._go_home(), 0.8)
            else:
                self.status_label.text = "Enter exactly 4 digits."
        else:
            if entered_hash == stored_hash:
                self._attempts = 0
                self.status_label.text = ""
                self._go_home()
            else:
                self._attempts += 1
                remaining = MAX_ATTEMPTS - self._attempts
                if self._attempts >= MAX_ATTEMPTS:
                    self._start_lockout()
                else:
                    self.status_label.color = app.theme.get("danger")
                    self.status_label.text = f"Wrong PIN. {remaining} attempts left."
                self._pin_input = ""
                self._update_dots()

    def _start_lockout(self):
        self._locked_out = True
        self._lockout_remaining = LOCKOUT_SECONDS
        self._update_lockout_label()
        Clock.schedule_interval(self._tick_lockout, 1)

    def _tick_lockout(self, dt):
        self._lockout_remaining -= 1
        if self._lockout_remaining <= 0:
            self._locked_out = False
            self._attempts = 0
            self.status_label.text = "Try again."
            return False
        self._update_lockout_label()

    def _update_lockout_label(self):
        self.status_label.text = f"Too many attempts. Wait {self._lockout_remaining}s."

    def _go_home(self):
        self.manager.current = "home"
