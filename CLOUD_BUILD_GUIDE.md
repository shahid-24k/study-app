# Build StudyApp APK Online — GitHub Actions (Free Cloud)

No PC needed. No WSL. No installs. GitHub builds your APK for free
on their cloud servers and you download it when it's done.

---

## What you need
- A GitHub account (free) → github.com
- Your StudyApp.zip file

---

## One-time setup (5 minutes)

### Step 1 — Create a new GitHub repo

1. Go to github.com → click the green "New" button
2. Name it: `StudyApp`
3. Set it to **Private** (so only you can see it)
4. Click **Create repository**

### Step 2 — Upload the project files

On the repo page, click **"uploading an existing file"** link.

Extract your `StudyApp.zip` and upload ALL the files/folders:
```
main.py
buildozer.spec
build_windows.sh
screens/  (whole folder)
utils/    (whole folder)
assets/   (whole folder)
.github/  (whole folder — IMPORTANT, this has the workflow!)
```

> Important: Make sure you upload the `.github/workflows/build_apk.yml` file.
> GitHub hides dot-folders — look for it in the extracted ZIP.

Click **Commit changes**.

---

## Every time you want to build

### Option A — Auto build on every push
The workflow runs automatically whenever you push/upload any file change.

### Option B — Manual trigger (recommended)

1. Go to your repo on GitHub
2. Click the **"Actions"** tab at the top
3. Click **"Build StudyApp APK"** in the left sidebar
4. Click the **"Run workflow"** button (top right)
5. Click the green **"Run workflow"** button in the popup

---

## Downloading your APK

1. Go to **Actions** tab
2. Click the latest workflow run (green checkmark = success)
3. Scroll down to **Artifacts** section
4. Click **"StudyApp-APK"** to download a ZIP
5. Extract the ZIP → you get `studyapp-1.0-debug.apk`
6. Transfer to your phone and install!

---

## Build times

| Situation | Time |
|---|---|
| First ever build (downloads SDK/NDK ~2GB) | 35–50 minutes |
| Repeat build (cache hit) | 8–15 minutes |

GitHub caches the Android SDK automatically so repeat builds are fast.

---

## Free tier limits

GitHub Actions gives you **2,000 free minutes per month** on private repos.
Each build uses ~15–40 minutes. That's 50–130 free builds per month — more than enough.

---

## If the build fails

1. Go to Actions → click the failed run (red X)
2. Click "Build APK with Buildozer" step to see the log
3. Download the "build-log" artifact for the full log
4. Common fixes:
   - If it says "requirements error" → check buildozer.spec requirements line
   - If it says "SDK license" → the workflow already handles this automatically
   - If it times out → re-run, the cache will make it faster next time

---

## Updating the app

1. Edit any `.py` file in your repo on GitHub (click the file → pencil icon)
2. Commit the change
3. Go to Actions → Run workflow → wait → download new APK

That's it! You never need to touch your phone's terminal or install anything.
