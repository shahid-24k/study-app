# Building StudyApp APK on Windows
### For Android 5.0+ (Old phones supported)

---

## What you need
- Windows 10 version 2004+ or Windows 11
- At least 10GB free disk space
- Internet connection (only during build, not for the app itself)

---

## Step 1 — Enable WSL2 on Windows

Open **PowerShell as Administrator** (right-click Start → Windows PowerShell (Admin)) and run:

```powershell
wsl --install
```

This installs WSL2 with Ubuntu automatically. **Restart your PC** when asked.

After restart, Ubuntu will open and ask you to create a username and password. Set these — you'll need them.

> If you already have WSL but it's WSL1, upgrade it:
> ```powershell
> wsl --set-default-version 2
> ```

---

## Step 2 — Open Ubuntu terminal

Search "Ubuntu" in the Start menu and open it. You now have a Linux terminal running inside Windows.

---

## Step 3 — Copy StudyApp into Ubuntu

In the Ubuntu terminal, run:

```bash
cd ~
mkdir StudyApp
```

Now open **File Explorer** in Windows. In the address bar, type:
```
\\wsl$\Ubuntu\home\YOUR_USERNAME\
```
(Replace YOUR_USERNAME with the username you set in Step 1)

Extract your `StudyApp.zip` here into the `StudyApp` folder.

Alternatively, from Ubuntu terminal if the ZIP is on your Desktop:
```bash
cp /mnt/c/Users/YOUR_WINDOWS_USERNAME/Desktop/StudyApp.zip ~/
cd ~
unzip StudyApp.zip
```

---

## Step 4 — Run the build script

In the Ubuntu terminal:

```bash
cd ~/StudyApp
chmod +x build_windows.sh
./build_windows.sh
```

This will:
1. Install all required tools
2. Download Android SDK and NDK automatically (one-time, ~2GB)
3. Compile the APK

**First build takes 20–40 minutes.** Subsequent builds are much faster (2–5 min).

---

## Step 5 — Get your APK

After the build finishes, the APK will be automatically copied to your **Windows Desktop**.

Or find it manually at:
```
\\wsl$\Ubuntu\home\YOUR_USERNAME\StudyApp\bin\studyapp-1.0-debug.apk
```

---

## Step 6 — Install on your phone

1. Transfer the APK to your phone (USB cable or share via WhatsApp/Telegram to yourself)
2. On your phone: **Settings → Security → Unknown sources → Enable**
   - On Android 8+: Settings → Apps → Special access → Install unknown apps
3. Open the APK file and tap Install

---

## Old phone compatibility

The `buildozer.spec` is already configured for:

| Setting | Value | Meaning |
|---|---|---|
| `android.minapi` | 21 | Android 5.0 Lollipop and above |
| `android.archs` | arm64-v8a, armeabi-v7a | Both 64-bit and 32-bit old CPUs |
| `android.ndk_api` | 21 | Native code compiled for API 21+ |

This means the app runs on phones from **2014 onwards** (Android 5.0+).

---

## Common errors and fixes

| Error | Fix |
|---|---|
| `JAVA_HOME not set` | Run: `export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64` |
| `SDK licence not accepted` | Run: `yes \| sdkmanager --licenses` |
| `No module named 'Cython'` | Run: `pip3 install cython` |
| `Build failed: NDK not found` | Delete `~/.buildozer` and rebuild |
| `wsl: command not found` | Update Windows, then retry Step 1 |

---

## Rebuilding after code changes

Every time you edit Python files in the StudyApp folder, just run:
```bash
cd ~/StudyApp
buildozer android debug
```

The APK in `bin/` will be updated.
