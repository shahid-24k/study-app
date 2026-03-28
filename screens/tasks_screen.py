"""
TasksScreen — add, complete, and delete study tasks. Stored locally.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App


class TasksScreen(Screen):
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

        root.add_widget(Label(text="[b]Study Tasks[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        # Input row
        input_row = BoxLayout(size_hint_y=None, height=48, spacing=8)
        self.task_input = TextInput(
            hint_text="Type a task and press Add...",
            multiline=False,
            font_size="14sp",
            background_color=t.get("surface"),
            foreground_color=t.get("text_primary"),
            cursor_color=t.get("accent"),
        )
        self.task_input.bind(on_text_validate=lambda *a: self._add_task())
        add_btn = Button(text="Add", size_hint_x=None, width=80,
                         background_normal="", background_color=t.get("accent"),
                         color=(0.04, 0.21, 0.17, 1), font_size="14sp")
        add_btn.bind(on_press=lambda b: self._add_task())
        input_row.add_widget(self.task_input)
        input_row.add_widget(add_btn)
        root.add_widget(input_row)

        # Task list
        self.scroll = ScrollView()
        self.task_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None, padding=(0, 4))
        self.task_box.bind(minimum_height=self.task_box.setter("height"))
        self.scroll.add_widget(self.task_box)
        root.add_widget(self.scroll)

        self._render_tasks()
        self.add_widget(root)

    def _render_tasks(self):
        app = App.get_running_app()
        t = app.theme
        self.task_box.clear_widgets()
        tasks = app.storage.get("tasks", [])
        if not tasks:
            self.task_box.add_widget(Label(
                text="No tasks yet. Add one above!",
                font_size="14sp",
                color=t.get("text_secondary"),
                size_hint_y=None, height=50,
            ))
            return
        for i, task in enumerate(tasks):
            row = self._task_row(task, i, t)
            self.task_box.add_widget(row)

    def _task_row(self, task, idx, t):
        row = BoxLayout(size_hint_y=None, height=52, spacing=8)
        with row.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=row.pos, size=row.size, radius=[8])
        row.bind(pos=lambda w, *a: self._redraw_row(w, t), size=lambda w, *a: self._redraw_row(w, t))

        done = task.get("done", False)
        color = t.get("text_secondary") if done else t.get("text_primary")
        text = ("[s]" + task["text"] + "[/s]") if done else task["text"]
        lbl = Label(text=text, markup=True, font_size="14sp", color=color,
                    halign="left", text_size=(None, None), padding=(10, 0))
        row.add_widget(lbl)

        done_btn = Button(
            text="✓" if not done else "↺",
            size_hint_x=None, width=44,
            background_normal="", background_color=t.get("accent") if not done else t.get("card"),
            color=(0.04, 0.21, 0.17, 1) if not done else t.get("text_primary"),
            font_size="16sp",
        )
        done_btn.bind(on_press=lambda b, i=idx: self._toggle_done(i))

        del_btn = Button(text="✕", size_hint_x=None, width=44,
                         background_normal="", background_color=t.get("danger"),
                         color=(1, 1, 1, 1), font_size="14sp")
        del_btn.bind(on_press=lambda b, i=idx: self._delete_task(i))

        row.add_widget(done_btn)
        row.add_widget(del_btn)
        return row

    def _redraw_row(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[8])

    def _add_task(self):
        app = App.get_running_app()
        text = self.task_input.text.strip()
        if not text:
            return
        tasks = app.storage.get("tasks", [])
        tasks.append({"text": text, "done": False})
        app.storage.set("tasks", tasks)
        self.task_input.text = ""
        self._render_tasks()

    def _toggle_done(self, idx):
        app = App.get_running_app()
        tasks = app.storage.get("tasks", [])
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = not tasks[idx].get("done", False)
            app.storage.set("tasks", tasks)
        self._render_tasks()

    def _delete_task(self, idx):
        app = App.get_running_app()
        tasks = app.storage.get("tasks", [])
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            app.storage.set("tasks", tasks)
        self._render_tasks()
