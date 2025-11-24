# Turbo Controller

A Windows application that sends rapid virtual key presses whenever you hold a chosen trigger key. Designed for simple turbo/tap firing without sacrificing responsiveness.

## Features
- **Global hotkey**: toggle turbo anywhere with **Ctrl+Alt+T**
- **Trigger vs. virtual buttons**: 13 trigger options and 12 virtual buttons
- **Turbo speed control**: 10–200 ms between press/release
- **System tray**: minimize to tray with quick balloon reminder
- **Responsive UI**: async loop so the form stays responsive
- **Win32 accuracy**: uses `SendInput`, `GetAsyncKeyState`, and `RegisterHotKey`

## Usage
1. Choose a **Trigger button** (what you hold).
2. Choose a **Virtual button** (what the app will press).
3. Set **Turbo speed (ms)** via slider or numeric input.
4. Click **Start** or press **Ctrl+Alt+T** to enable.
5. Hold your trigger key to send repeated presses of the virtual key.
6. Click **Stop** or use **Ctrl+Alt+T** again to pause.

## Tray controls
- **Minimize to tray** keeps turbo running in the background.
- Tray menu offers **Toggle Turbo** and **Exit** shortcuts.

## Safety note
Be mindful of game/service terms of use when automating input.
