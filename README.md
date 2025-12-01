# AI

This repository contains two tracks:

- **TurboController**: A Windows example built with .NET 6.0 and WinForms, located in `TurboController/`.
- **OpenAI workspace**: A lightweight Python setup for experimenting with the OpenAI API from this repo root.

## OpenAI workspace setup

1. Create a `.env` file in the repository root and add your API key:
   ```bash
   echo "OPENAI_API_KEY=sk-..." > .env
   ```
2. Ensure secrets stay untracked by Git (already handled in `.gitignore`).
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows: venv\\Scripts\\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Verify connectivity with the included test script:
   ```bash
   python main.py
   ```

The test script loads `OPENAI_API_KEY` from `.env`, initializes the OpenAI client, and makes a sample chat completion request so you can confirm your credentials are working.

## TurboController build

To build the TurboController WinForms app on a Windows host with .NET 6 installed:
```bash
dotnet restore TurboController/TurboController.csproj
dotnet build TurboController/TurboController.csproj --configuration Release
```
