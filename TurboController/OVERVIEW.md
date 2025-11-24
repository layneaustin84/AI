# Overview

Turbo Controller is a lightweight WinForms utility for Windows that repeatedly sends a chosen virtual key while you hold a trigger key. It uses native Win32 APIs to keep latency low and registers a global hotkey so you can toggle turbo from any window.

- **UI stack:** .NET 6.0, WinForms
- **Entry point:** `Program.cs`
- **Main logic:** `MainForm.cs` (UI, hotkey registration, turbo loop, Win32 interop)
- **Build script:** `build.bat` (Release publish to `published/`)
