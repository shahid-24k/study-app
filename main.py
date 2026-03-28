"""
StudyApp - Personal Study Command Center for Shahid Khan
Secure, local-only, no external data leakage.
"""

import os
os.environ["KIVY_NO_ENV_CONFIG"] = "1"  # Disable env-based config injection

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform

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

Window.softinput_mode = "below_target"


class StudyApp(App):
    title = "StudyApp"
    icon = "assets/icon.png"

    def build(self):
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

        # Always start at lock screen
        sm.current = "lock"
        self.sm = sm
        return sm

    def on_pause(self):
        # Lock app when minimized (security: re-lock on resume)
        return True

    def on_resume(self):
        self.sm.current = "lock"

    def on_stop(self):
        self.storage.flush()


if __name__ == "__main__":
    StudyApp().run()
