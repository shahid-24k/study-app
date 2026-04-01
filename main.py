"""
StudyApp - Personal Study Command Center for Shahid Khan
"""
import os
import sys

# Android-safe environment setup
os.environ["KIVY_NO_ENV_CONFIG"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

# Must set these BEFORE importing kivy
from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')
Config.set('graphics', 'multisamples', '0')  # fixes black screen on old GPUs
Config.set('graphics', 'allow_screensaver', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform

Window.softinput_mode = "below_target"

# Import screens — wrapped in try/except so crash shows error not black screen
try:
    from screens.lock_screen import LockScreen
    from screens.home_screen import HomeScreen
    from screens.pomodoro_screen import PomodoroScreen
    from screens.tasks_screen import TasksScreen
    from screens.subjects_screen import SubjectsScreen
    from screens.hadith_screen import HadithScreen
    from screens.prayer_screen import PrayerScreen
    from screens.exam_screen import ExamScreen
    from screens.settings_screen import SettingsScreen
    from utils.storage import SecureStorage
    from utils.theme import ThemeManager
    IMPORT_OK = True
    IMPORT_ERROR = None
except Exception as e:
    IMPORT_OK = False
    IMPORT_ERROR = str(e)


class StudyApp(App):
    title = "StudyApp"

    def build(self):
        if not IMPORT_OK:
            # Show error screen instead of crashing silently
            from kivy.uix.label import Label
            from kivy.uix.boxlayout import BoxLayout
            root = BoxLayout(orientation='vertical', padding=20)
            root.add_widget(Label(
                text=f"[b]Import Error:[/b]\n{IMPORT_ERROR}",
                markup=True,
                font_size='14sp',
                color=(1, 0.3, 0.3, 1),
                halign='center',
            ))
            return root

        self.storage = SecureStorage()
        self.theme = ThemeManager(self.storage)

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PomodoroScreen(name="pomodoro"))
        sm.add_widget(TasksScreen(name="tasks"))
        sm.add_widget(SubjectsScreen(name="subjects"))
        sm.add_widget(HadithScreen(name="hadith"))
        sm.add_widget(PrayerScreen(name="prayer"))
        sm.add_widget(ExamScreen(name="exams"))
        sm.add_widget(SettingsScreen(name="settings"))

        sm.current = "lock"
        self.sm = sm
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        if hasattr(self, 'sm'):
            self.sm.current = "lock"

    def on_stop(self):
        if hasattr(self, 'storage'):
            self.storage.flush()


if __name__ == "__main__":
    StudyApp().run()
