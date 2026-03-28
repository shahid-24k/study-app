"""
HadithScreen — Hadith of the day from local curated collection.
No network calls. All data embedded locally for security.
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from datetime import datetime
import random


HADITHS = [
    {
        "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ",
        "transliteration": "Innamal a'maalu binniyyaat",
        "english": "Actions are judged by intentions.",
        "source": "Bukhari & Muslim",
    },
    {
        "arabic": "الطُّهُورُ شَطْرُ الإِيمَانِ",
        "transliteration": "At-tuhuru shatlul imaan",
        "english": "Cleanliness is half of faith.",
        "source": "Muslim",
    },
    {
        "arabic": "لَا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ",
        "transliteration": "Laa yu'minu ahadukum hatta yuhibba li-akhihi ma yuhibbu linafsihi",
        "english": "None of you truly believes until he loves for his brother what he loves for himself.",
        "source": "Bukhari & Muslim",
    },
    {
        "arabic": "الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ",
        "transliteration": "Al-muslimu man salimal muslimuna min lisaanihi wa yadihi",
        "english": "A Muslim is one from whose tongue and hands other Muslims are safe.",
        "source": "Bukhari",
    },
    {
        "arabic": "خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ",
        "transliteration": "Khairukum man ta'allamal Qur'aana wa 'allamah",
        "english": "The best of you are those who learn the Quran and teach it.",
        "source": "Bukhari",
    },
    {
        "arabic": "اتَّقِ اللَّهَ حَيْثُمَا كُنْتَ",
        "transliteration": "Ittaqillaha haythumaa kunta",
        "english": "Fear Allah wherever you are.",
        "source": "Tirmidhi",
    },
    {
        "arabic": "إِنَّ اللَّهَ رَفِيقٌ يُحِبُّ الرِّفْقَ",
        "transliteration": "Innallaha rafeequn yuhibbur-rifq",
        "english": "Verily, Allah is gentle and loves gentleness.",
        "source": "Bukhari & Muslim",
    },
    {
        "arabic": "مَنْ صَمَتَ نَجَا",
        "transliteration": "Man samata naja",
        "english": "Whoever remains silent is saved.",
        "source": "Tirmidhi",
    },
    {
        "arabic": "الْيَدُ الْعُلْيَا خَيْرٌ مِنَ الْيَدِ السُّفْلَى",
        "transliteration": "Al-yadul 'ulya khayrun minal-yadis-suflaa",
        "english": "The upper hand (the one that gives) is better than the lower hand (the one that takes).",
        "source": "Bukhari & Muslim",
    },
    {
        "arabic": "طَلَبُ الْعِلْمِ فَرِيضَةٌ عَلَى كُلِّ مُسْلِمٍ",
        "transliteration": "Talabul 'ilmi fareedatun 'ala kulli muslim",
        "english": "Seeking knowledge is an obligation upon every Muslim.",
        "source": "Ibn Majah",
    },
    {
        "arabic": "أَحَبُّ الْأَعْمَالِ إِلَى اللَّهِ أَدْوَمُهَا وَإِنْ قَلَّ",
        "transliteration": "Ahabbu al-a'maali ilallahi adwamuha wa in qall",
        "english": "The most beloved deeds to Allah are the most consistent ones, even if small.",
        "source": "Bukhari & Muslim",
    },
    {
        "arabic": "كُلُّ مَعْرُوفٍ صَدَقَةٌ",
        "transliteration": "Kullu ma'roofin sadaqah",
        "english": "Every act of goodness is charity.",
        "source": "Bukhari",
    },
    {
        "arabic": "إِذَا مَاتَ الإِنْسَانُ انْقَطَعَ عَنْهُ عَمَلُهُ إِلاَّ مِنْ ثَلاَثَةٍ",
        "transliteration": "Idha matal insaanu inqata'a 'anhu 'amaluhu illa min thalatha",
        "english": "When a person dies, all their deeds end except three: ongoing charity, beneficial knowledge, or a righteous child who prays for them.",
        "source": "Muslim",
    },
    {
        "arabic": "رِضَا اللَّهِ فِي رِضَا الْوَالِدَيْنِ",
        "transliteration": "Ridallahi fi ridat-walidayn",
        "english": "The pleasure of Allah lies in the pleasure of parents.",
        "source": "Tirmidhi",
    },
    {
        "arabic": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ",
        "transliteration": "Man kaana yu'minu billahi wal-yawmil-aakhiri falyaqul khayran aw liyasmut",
        "english": "Whoever believes in Allah and the Last Day should speak good or remain silent.",
        "source": "Bukhari & Muslim",
    },
]


class HadithScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self._build()

    def _build(self):
        app = App.get_running_app()
        t = app.theme

        # Pick hadith based on day of year for consistency
        day_idx = datetime.now().timetuple().tm_yday % len(HADITHS)
        self._current_idx = day_idx
        self._shown = HADITHS[day_idx]

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

        root.add_widget(Label(text="[b]Hadith of the Day[/b]", markup=True,
                              font_size="22sp", color=t.get("text_primary"),
                              size_hint_y=None, height=40))

        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", spacing=14, size_hint_y=None, padding=(0, 4))
        content.bind(minimum_height=content.setter("height"))

        self._card_box = content
        self._render_hadith(content, self._shown, t)

        next_btn = Button(text="Another Hadith ↻", background_normal="",
                          background_color=t.get("card"), color=t.get("accent"),
                          font_size="14sp", size_hint_y=None, height=48)
        next_btn.bind(on_press=lambda b: self._next_hadith())
        content.add_widget(next_btn)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def _render_hadith(self, parent, hadith, t):
        # Arabic
        arabic_card = BoxLayout(orientation="vertical", size_hint_y=None, height=90, padding=16)
        with arabic_card.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=arabic_card.pos, size=arabic_card.size, radius=[12])
        arabic_card.bind(pos=lambda w, *a: self._redraw(w, t), size=lambda w, *a: self._redraw(w, t))
        arabic_card.add_widget(Label(
            text=hadith["arabic"],
            font_size="20sp",
            color=t.get("accent"),
            halign="center",
            text_size=(None, None),
        ))
        parent.add_widget(arabic_card)

        # Transliteration
        parent.add_widget(Label(
            text=f"[i]{hadith['transliteration']}[/i]",
            markup=True,
            font_size="13sp",
            color=t.get("text_secondary"),
            halign="center",
            text_size=(None, None),
            size_hint_y=None,
            height=36,
        ))

        # English
        eng_card = BoxLayout(orientation="vertical", size_hint_y=None, height=100, padding=16)
        with eng_card.canvas.before:
            Color(*t.get("card"))
            RoundedRectangle(pos=eng_card.pos, size=eng_card.size, radius=[12])
        eng_card.bind(pos=lambda w, *a: self._redraw_card(w, t), size=lambda w, *a: self._redraw_card(w, t))
        eng_card.add_widget(Label(
            text=f'"{hadith["english"]}"',
            font_size="15sp",
            color=t.get("text_primary"),
            halign="center",
            text_size=(None, None),
        ))
        parent.add_widget(eng_card)

        # Source
        parent.add_widget(Label(
            text=f"— {hadith['source']}",
            font_size="12sp",
            color=t.get("text_secondary"),
            halign="right",
            text_size=(None, None),
            size_hint_y=None,
            height=28,
        ))

    def _redraw(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("surface"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[12])

    def _redraw_card(self, w, t):
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*t.get("card"))
            RoundedRectangle(pos=w.pos, size=w.size, radius=[12])

    def _next_hadith(self):
        self._current_idx = (self._current_idx + 1) % len(HADITHS)
        self._shown = HADITHS[self._current_idx]
        self.on_enter()
