# Pomodoro Clock (Kivy / Android)

A Pomodoro timer built with Kivy, with the timer panel docked to the top-right
corner of the screen. Includes **Start**, **Pause**, **Stop**, and **+ / -**
buttons to adjust the session length in minutes (1-90, default 25).

## Run on desktop (for testing)

```bash
pip install kivy
python3 main.py
```

## Get the Android APK (no local Android SDK needed)

This repo includes a GitHub Actions workflow
(`.github/workflows/build-pomodoro-apk.yml`) that builds the APK for you:

1. Push changes under `pomodoro_kivy_app/` (or trigger the workflow manually
   from the **Actions** tab -> "Build Pomodoro Kivy APK" -> "Run workflow").
2. Wait for the job to finish (first run downloads the Android SDK/NDK, so it
   can take 15-30 minutes).
3. Download the `pomodoro-clock-apk` artifact from the completed run.
4. Transfer the `.apk` to your Poco X6 Pro (e.g. via USB, Google Drive, or a
   direct download link) and install it. You'll need to allow
   "install from unknown sources" for the app you use to open the file.

## Build locally instead (optional)

If you'd rather build on your own Linux machine/WSL:

```bash
pip install buildozer cython
cd pomodoro_kivy_app
buildozer -v android debug
```

The APK will be generated in `pomodoro_kivy_app/bin/`.
