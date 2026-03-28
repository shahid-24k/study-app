"""
ThemeManager — manages dark/light mode colors across the app.
"""


THEMES = {
    "dark": {
        "bg": (0.08, 0.08, 0.10, 1),
        "surface": (0.13, 0.13, 0.16, 1),
        "card": (0.17, 0.17, 0.21, 1),
        "accent": (0.11, 0.62, 0.46, 1),       # Teal green
        "accent2": (0.47, 0.46, 0.87, 1),      # Purple
        "text_primary": (0.95, 0.95, 0.95, 1),
        "text_secondary": (0.60, 0.60, 0.65, 1),
        "danger": (0.89, 0.29, 0.29, 1),
        "warning": (0.73, 0.46, 0.09, 1),
        "border": (0.25, 0.25, 0.30, 1),
    },
    "light": {
        "bg": (0.96, 0.96, 0.97, 1),
        "surface": (1, 1, 1, 1),
        "card": (0.92, 0.92, 0.94, 1),
        "accent": (0.07, 0.56, 0.40, 1),
        "accent2": (0.40, 0.38, 0.80, 1),
        "text_primary": (0.08, 0.08, 0.10, 1),
        "text_secondary": (0.40, 0.40, 0.45, 1),
        "danger": (0.75, 0.18, 0.18, 1),
        "warning": (0.60, 0.35, 0.05, 1),
        "border": (0.80, 0.80, 0.83, 1),
    }
}


class ThemeManager:
    def __init__(self, storage):
        self.storage = storage
        mode = storage.get("theme", "dark")
        self._mode = mode if mode in THEMES else "dark"

    @property
    def mode(self):
        return self._mode

    @property
    def c(self):
        return THEMES[self._mode]

    def toggle(self):
        self._mode = "light" if self._mode == "dark" else "dark"
        self.storage.set("theme", self._mode)
        return self._mode

    def get(self, key):
        return THEMES[self._mode].get(key, (1, 1, 1, 1))
