# Quickstart

1. Install the **.NET 6.0 SDK** (or newer) on Windows.
2. From a Developer Command Prompt, run:
   ```cmd
   dotnet restore
   dotnet publish -c Release -r win-x64 --self-contained false -o published
   ```
3. Launch `published/TurboController.exe`.
4. Choose your trigger/virtual buttons, set speed, and press **Ctrl+Alt+T** to toggle.

You can also double-click `build.bat`, which runs the publish command and drops the output into `published/`.
