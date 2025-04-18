# Windows Persistence Detection Script for Keylogger Indicators
# Author: sakthi
# Purpose: Detect potential keylogger persistence via registry, startup folders, scheduled tasks

# Create output directory
$outputDir = "$PSScriptRoot\PersistenceScan_Results"
if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Check Registry Run Keys - Current User
try {
    Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" |
    Out-File -FilePath "$outputDir\reg_run_user.txt"
} catch {
    "Could not read HKCU Run registry keys." | Out-File -Append "$outputDir\errors.txt"
}

# Check Registry Run Keys - Local Machine
try {
    Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" |
    Out-File -FilePath "$outputDir\reg_run_machine.txt"
} catch {
    "Could not read HKLM Run registry keys." | Out-File -Append "$outputDir\errors.txt"
}

# Check Startup Folder
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
try {
    Get-ChildItem -Path $startupPath -Force |
    Out-File -FilePath "$outputDir\startup_files.txt"
} catch {
    "Could not access Startup folder." | Out-File -Append "$outputDir\errors.txt"
}

# Check Scheduled Tasks with potential suspicious names
try {
    Get-ScheduledTask |
    Where-Object { $_.TaskName -match "keylog" -or $_.TaskPath -match "keylog" } |
    Out-File -FilePath "$outputDir\scheduled_tasks.txt"
} catch {
    "Could not query Scheduled Tasks." | Out-File -Append "$outputDir\errors.txt"
}

# Basic Flagging Logic
$hasPersistence = 0

if ((Get-Content "$outputDir\reg_run_user.txt").Length -gt 0 -or
    (Get-Content "$outputDir\reg_run_machine.txt").Length -gt 0 -or
    (Get-Content "$outputDir\startup_files.txt").Length -gt 0 -or
    (Get-Content "$outputDir\scheduled_tasks.txt").Length -gt 0) {

    $hasPersistence = 1
}

@"
has_persistence,$hasPersistence
"@ | Out-File -FilePath "$outputDir\persistence_flag.csv" -Encoding ascii

Write-Output "Persistence scan complete. Results saved to $outputDir"
