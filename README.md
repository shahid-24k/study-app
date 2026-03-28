# StudyApp — Personal Study Command Center
### Built for Shahid Khan | Secure | Fully Offline | Android APK

---

## Features
- 🔐 PIN Lock Screen (SHA-256 hashed, lockout after 5 wrong attempts)
- 🍅 Pomodoro Timer (25/5/15 min modes, session log)
- ✅ Task Manager (add, complete, delete tasks)
- 📚 Subject Progress Tracker (7 subjects, tap to update)
- 📖 Hadith of the Day (15 verified Hadiths, offline)
- 🕌 Prayer Times (offline calculation for Krishnagiri, TN)
- 📅 Exam Countdown (add exam dates, live countdown)
- ⚙️ Settings (dark/light mode, PIN change, data reset)
- 🔒 App auto-locks when minimized

## Security Features
- NO internet permission in APK (zero network attack surface)
- PIN stored as SHA-256 hash, never plain text
- All data stored locally in app's private directory
- Storage file obfuscated with XOR + Base64
- Atomic file writes (no corruption on crash)
- App re-locks on every resume from background
- 30-second lockout after 5 wrong PIN attempts
- `android.allow_backup = False` (prevents ADB data extraction)

---

## How to Build the APK

### Option A: Using Termux on Android (Recommended for you)

1. Install **Termux** from F-Droid (not Play Store)
2. Open Termux and run:

```bash
pkg update && pkg upgrade -y
pkg install python git wget -y
pip install buildozer cython
```

3. Copy the StudyApp folder to your phone (via USB or cloud)
4. Navigate to the folder:
```bash
cd /path/to/StudyApp
```

5. Initialize and build:
```bash
buildozer android debug
```

6. First build takes 30–60 minutes (downloads Android SDK/NDK).
   The APK will be in: `bin/studyapp-1.0-debug.apk`

7. Install it:
```bash
buildozer android deploy run
```

### Option B: Using Google Colab (Easiest — no device needed)

1. Go to https://colab.research.google.com
2. Create a new notebook
3. Run these cells:

```python
# Cell 1 — Install dependencies
!pip install buildozer cython virtualenv
!sudo apt-get install -y \
    python3-pip build-essential git \
    python3 python3-dev \
    libffi-dev libssl-dev \
    libltdl-dev zlib1g-dev \
    openjdk-17-jdk
```

```python
# Cell 2 — Upload your zip
from google.colab import files
files.upload()  # Upload StudyApp.zip
```

```python
# Cell 3 — Unzip and build
!unzip StudyApp.zip -d StudyApp
%cd StudyApp
!buildozer android debug
```

```python
# Cell 4 — Download APK
from google.colab import files
import glob
apk = glob.glob('bin/*.apk')[0]
files.download(apk)
```

### Option C: Using a Linux PC/Laptop

```bash
sudo apt install python3-pip build-essential git \
    python3-dev libffi-dev libssl-dev openjdk-17-jdk -y
pip3 install buildozer cython
cd StudyApp
buildozer android debug
```

---

## Installing the APK on Your Phone

1. Enable "Install from unknown sources" in Settings > Security
2. Transfer the APK to your phone
3. Tap to install

---

## Project Structure

```
StudyApp/
├── main.py                  # App entry point
├── buildozer.spec           # Android build config
├── screens/
│   ├── lock_screen.py       # PIN lock
│   ├── home_screen.py       # Dashboard
│   ├── pomodoro_screen.py   # Timer
│   ├── tasks_screen.py      # Task manager
│   ├── subjects_screen.py   # Subject progress
│   ├── hadith_screen.py     # Hadith of the day
│   ├── prayer_screen.py     # Prayer times
│   ├── exam_screen.py       # Exam countdown
│   └── settings_screen.py   # Settings
├── utils/
│   ├── storage.py           # Encrypted local storage
│   └── theme.py             # Dark/light theme manager
├── assets/                  # Icons (add icon.png here)
└── data/                    # Extra data files (optional)
```

---

## First Launch

1. App opens to the **PIN setup screen**
2. Enter any 4-digit PIN — this becomes your lock PIN
3. You're in! All data saves automatically.

## Changing PIN Later
Settings → Change PIN → Enter current PIN → Enter new PIN

## Prayer Times Note
Prayer times are calculated **offline** using astronomical formulas
for Krishnagiri, Tamil Nadu (12.5186°N, 78.2138°E, UTC+5:30).
Uses the Muslim World League calculation method.
