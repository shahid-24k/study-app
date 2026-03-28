"""
PomodoroScreen — 25/5/15 minute timer with session logging.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.app import App
from datetime import datetime


MODES = {
    "focus": 25 * 60,
    "short": 5 * 60,
    "long": 15 * 60,
}


class PomodoroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._remaining = MODES["focus"]
        self._total = MODES["focus"]
        self._mode = "focus"
        self._running = False
        self._clock_event = None

    def on_enter(self):
        self.clear_widgets()
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme

        root = BoxLayout(orientation="vertical", padding=20, spacing=16)
        with root.canvas.before:
            Color(*t.get("bg"))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        # Back
        back = Button(text="← Back", size_hint_y=None, height=40, background_normal="",
                      background_color=(0,0,0,0), color=t.get("accent"), font_size="14sp", halign="left")
        back.bind(on_press=lambda b: setattr(self.manager, 'current', 'home'))
        root.add_widget(back)

        root.add_widget(Label(text="[b]Pomodoro Timer[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        self.mode_label = Label(text="Focus Session", font_size="14sp",
                                color=t.get("text_secondary"), size_hint_y=None, height=28)
        root.add_widget(self.mode_label)

        self.timer_label = Label(text=self._fmt(self._remaining),
                                 font_size="64sp", color=t.get("accent"),
                                 size_hint_y=None, height=120)
        root.add_widget(self.timer_label)

        # Progress bar
        pb_outer = BoxLayout(size_hint_y=None, height=10, padding=(0, 0, 0, 0))
        with pb_outer.canvas.before:
            Color(*t.get("border"))
            RoundedRectangle(pos=pb_outer.pos, size=pb_outer.size, radius=[5])
        pb_outer.bind(pos=lambda w,*a: self._redraw_pb(w, t), size=lambda w,*a: self._redraw_pb(w, t))
        self.pb_outer = pb_outer
        root.add_widget(pb_outer)

        # Control buttons
        controls = GridLayout(cols=2, size_hint_y=None, height=60, spacing=10)
        self.start_btn = Button(text="Start", background_normal="", background_color=t.get("accent"),
                                color=(0.04, 0.21, 0.17, 1), font_size="16sp", bold=True)
        self.start_btn.bind(on_press=lambda b: self._toggle())

        reset_btn = Button(text="Reset", background_normal="", background_color=t.get("card"),
                           color=t.get("text_primary"), font_size="16sp")
        reset_btn.bind(on_press=lambda b: self._reset())
        controls.add_widget(self.start_btn)
        controls.add_widget(reset_btn)
        root.add_widget(controls)

        # Mode selector
        modes_row = GridLayout(cols=3, size_hint_y=None, height=48, spacing=8)
        for label, key in [("Focus 25m", "focus"), ("Short 5m", "short"), ("Long 15m", "long")]:
            btn = Button(text=label, background_normal="", background_color=t.get("surface"),
                         color=t.get("text_primary"), font_size="12sp")
            btn.bind(on_press=lambda b, k=key: self._switch_mode(k))
            modes_row.add_widget(btn)
        root.add_widget(modes_row)

        # Session log
        root.add_widget(Label(text="Today's sessions", font_size="13sp",
                              color=t.get("text_secondary"), size_hint_y=None, height=28))

        self.log_label = Label(
            text=self._get_log_text(app),
            font_size="12sp",
            color=t.get("text_secondary"),
            text_size=(None, None),
            halign="center",
        )
        root.add_widget(self.log_label)

        self.add_widget(root)

    def _redraw_pb(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("border"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[5])

    def _fmt(self, secs):
        m = secs // 60
        s = secs % 60
        return f"{m:02d}:{s:02d}"

    def _toggle(self):
        if self._running:
            self._running = False
            if self._clock_event:
                self._clock_event.cancel()
            self.start_btn.text = "Resume"
        else:
            self._running = True
            self._clock_event = Clock.schedule_interval(self._tick, 1)
            self.start_btn.text = "Pause"

    def _tick(self, dt):
        if self._remaining <= 0:
            self._running = False
            self._clock_event.cancel()
            self.start_btn.text = "Start"
            self._session_done()
            return False
        self._remaining -= 1
        self.timer_label.text = self._fmt(self._remaining)

    def _reset(self):
        self._running = False
        if self._clock_event:
            self._clock_event.cancel()
        self._remaining = self._total
        self.timer_label.text = self._fmt(self._remaining)
        self.start_btn.text = "Start"

    def _switch_mode(self, key):
        self._running = False
        if self._clock_event:
            self._clock_event.cancel()
        self._mode = key
        self._total = MODES[key]
        self._remaining = self._total
        self.timer_label.text = self._fmt(self._remaining)
        self.start_btn.text = "Start"
        names = {"focus": "Focus Session", "short": "Short Break", "long": "Long Break"}
        self.mode_label.text = names[key]

    def _session_done(self):
        app = App.get_running_app()
        if self._mode == "focus":
            count = app.storage.get("pomo_count_today", 0) + 1
            app.storage.set("pomo_count_today", count)
            log = app.storage.get("pomo_log", [])
            log.append({"time": datetime.now().strftime("%H:%M"), "duration": self._total // 60})
            if len(log) > 20:
                log = log[-20:]
            app.storage.set("pomo_log", log)
            self.log_label.text = self._get_log_text(app)
        self.timer_label.text = "Done! ✓"

    def _get_log_text(self, app):
        log = app.storage.get("pomo_log", [])
        if not log:
            return "No sessions yet today."
        return "  ".join([f"[{e['time']}] {e['duration']}m" for e in log[-6:]])
