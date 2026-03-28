"""
PrayerScreen — Prayer times for Krishnagiri, Tamil Nadu.
Uses offline astronomical calculation (no API, no network calls).
Based on Muslim World League calculation method.
"""

import math
from datetime import datetime, date
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App


# Krishnagiri, Tamil Nadu coordinates
LAT = 12.5186
LON = 78.2138
TIMEZONE = 5.5  # IST UTC+5:30

PRAYER_NAMES = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
PRAYER_ICONS = ["🌙", "🌅", "☀️", "🕓", "🌇", "🌃"]


def _deg(r): return math.degrees(r)
def _rad(d): return math.radians(d)


def calculate_prayer_times(lat, lon, tz, year, month, day):
    """Offline prayer time calculation — Muslim World League method."""
    jd = _julian_day(year, month, day)
    d = jd - 2451545.0

    # Sun coordinates
    g = _rad(357.529 + 0.98560028 * d)
    q = 280.459 + 0.98564736 * d
    L = _rad(q + 1.9151 * math.sin(g) + 0.020 * math.sin(2 * g))
    e = _rad(23.439 - 0.00000036 * d)
    RA = _deg(math.atan2(math.cos(e) * math.sin(L), math.cos(L))) / 15
    D = _deg(math.asin(math.sin(e) * math.sin(L)))
    EqT = q / 15 - RA

    Dh = 12 - EqT - (lon / 15) + tz

    def hour_angle(alt):
        num = -math.sin(_rad(alt)) - math.sin(_rad(lat)) * math.sin(_rad(D))
        den = math.cos(_rad(lat)) * math.cos(_rad(D))
        val = num / den
        if abs(val) > 1:
            return None
        return _deg(math.acos(val)) / 15

    def asr_angle():
        sf = 1  # Shafi/Maliki factor
        x = sf + math.tan(_rad(abs(lat - D)))
        num = -math.cos(math.atan(1 / x)) - math.sin(_rad(lat)) * math.sin(_rad(D))
        den = math.cos(_rad(lat)) * math.cos(_rad(D))
        val = num / den
        if abs(val) > 1:
            return None
        return _deg(math.acos(val)) / 15

    fajr_ha = hour_angle(-18)
    sunrise_ha = hour_angle(-0.833)
    asr_ha = asr_angle()
    maghrib_ha = hour_angle(-0.833)
    isha_ha = hour_angle(-17)

    def fmt(t):
        if t is None:
            return "--:--"
        h = int(t)
        m = int((t - h) * 60)
        ampm = "AM" if h < 12 else "PM"
        h12 = h % 12 or 12
        return f"{h12}:{m:02d} {ampm}"

    times = {
        "Fajr":    fmt(Dh - fajr_ha)    if fajr_ha else "--:--",
        "Sunrise": fmt(Dh - sunrise_ha) if sunrise_ha else "--:--",
        "Dhuhr":   fmt(Dh),
        "Asr":     fmt(Dh + asr_ha)     if asr_ha else "--:--",
        "Maghrib": fmt(Dh + maghrib_ha) if maghrib_ha else "--:--",
        "Isha":    fmt(Dh + isha_ha)    if isha_ha else "--:--",
    }
    return times


def _julian_day(y, m, d):
    if m <= 2:
        y -= 1
        m += 12
    A = int(y / 100)
    B = 2 - A + int(A / 4)
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5


class PrayerScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme
        today = date.today()
        times = calculate_prayer_times(LAT, LON, TIMEZONE, today.year, today.month, today.day)

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

        root.add_widget(Label(text="[b]Prayer Times[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        root.add_widget(Label(
            text=f"Krishnagiri, Tamil Nadu  •  {today.strftime('%d %B %Y')}",
            font_size="13sp", color=t.get("text_secondary"),
            size_hint_y=None, height=24,
        ))

        root.add_widget(Label(
            text="Calculated offline (Muslim World League method)",
            font_size="11sp", color=t.get("text_secondary"),
            size_hint_y=None, height=20,
        ))

        scroll = ScrollView()
        box = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None, padding=(0, 4))
        box.bind(minimum_height=box.setter("height"))

        now_str = datetime.now().strftime("%I:%M %p")
        for icon, name in zip(PRAYER_ICONS, PRAYER_NAMES):
            card = self._prayer_card(icon, name, times[name], t)
            box.add_widget(card)

        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _prayer_card(self, icon, name, time_str, t):
        card = BoxLayout(size_hint_y=None, height=60, padding=(16, 0), spacing=12)
        with card.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
        card.bind(pos=lambda w, *a: self._redraw(w, t), size=lambda w, *a: self._redraw(w, t))
        card.add_widget(Label(text=icon, font_size="22sp", size_hint_x=None, width=36))
        card.add_widget(Label(text=name, font_size="16sp", color=t.get("text_primary"),
                              halign="left", text_size=(None, None)))
        card.add_widget(Label(text=time_str, font_size="16sp", color=t.get("accent"),
                              halign="right", text_size=(None, None)))
        return card

    def _redraw(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[10])
