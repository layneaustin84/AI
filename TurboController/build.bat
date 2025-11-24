@echo off
setlocal

set DOTNET_CLI_TELEMETRY_OPTOUT=1

if not exist published mkdir published

dotnet restore
if %errorlevel% neq 0 goto :error

dotnet publish -c Release -r win-x64 --self-contained false -o published
if %errorlevel% neq 0 goto :error

echo.
echo Publish complete. Launch published\TurboController.exe
exit /b 0

:error
echo Build failed.
exit /b 1
