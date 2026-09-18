# Rendszergazdai jogosultság ellenőrzése / kérése
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "=== Discord Bot Manager - Python & CustomTkinter Telepito ===" -ForegroundColor Cyan

# 1. Python ellenőrzése
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonInstalled) {
    Write-Host "[+] Python nem található. Telepítés indítása..." -ForegroundColor Yellow
    $url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
    $output = "$env:TEMP\python_installer.exe"

    Write-Host "[+] Python telepítő letöltése..." -ForegroundColor Gray
    Invoke-WebRequest -Uri $url -OutFile $output

    Write-Host "[+] Python telepítése (ez eltarthat egy kis ideig)..." -ForegroundColor Gray
    Start-Process -FilePath $output -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
    Remove-Item $output

    # Environment PATH frissítése a jelenlegi munkamenetben
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host "[OK] Python sikeresen telepítve!" -ForegroundColor Green
} else {
    Write-Host "[OK] Python már telepítve van." -ForegroundColor Green
}

# 2. Pip és modulok telepítése
Write-Host "[+] Modulok telepítése (customtkinter, pillow, stb.)..." -ForegroundColor Yellow

python -m pip install --upgrade pip --quiet
python -m pip install customtkinter psutil Pillow matplotlib pystray pypresence --quiet

Write-Host "`n[SUCCESS] Minden függőség és a Python sikeresen telepítve lett!" -ForegroundColor Green
Write-Host "Most már elindíthatod az installer.pyw fájlt." -ForegroundColor Cyan
Read-Host -Prompt "Nyomj Enter-t a bezáráshoz"