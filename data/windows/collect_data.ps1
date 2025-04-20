# collect_data.ps1
# Detect suspicious process behaviors using heuristics (Persistence, Network, FileWrite, Script)

$csvPath = "samples\processes.csv"
$output = @()
$output += "PID,PPID,Executable,Commandline,Persistence,NetworkAccess,FileWrite,ScriptBased"

# Get all processes excluding the current script
$processes = Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $PID }

# Get network connections once to avoid repeated calls
$netConnections = Get-NetTCPConnection -ErrorAction SilentlyContinue

# Get Startup folder items once
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$startupFiles = Get-ChildItem -Path $startupPath -Force -ErrorAction SilentlyContinue

# Get scheduled tasks once
$scheduledTasks = Get-ScheduledTask -ErrorAction SilentlyContinue

# Get registry startup values once
$regUser = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
$regMachine = Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue

foreach ($proc in $processes) {
    $procId = $proc.ProcessId
    $ppid = $proc.ParentProcessId
    $exe = $proc.ExecutablePath
    $cmdline = $proc.CommandLine

    if (-not $cmdline) { continue }

    # Truncate long command lines for better readability
    $shortCmd = if ($cmdline.Length -gt 100) { $cmdline.Substring(0, 100) + "..." } else { $cmdline }

    # Heuristic 1: Persistence
    $persistence = 0
    foreach ($val in $regUser.PSObject.Properties) {
        if ($cmdline -like "*$($val.Value)*") { $persistence = 1; break }
    }
    foreach ($val in $regMachine.PSObject.Properties) {
        if ($cmdline -like "*$($val.Value)*") { $persistence = 1; break }
    }
    foreach ($file in $startupFiles) {
        if ($cmdline -like "*$($file.Name)*") { $persistence = 1; break }
    }
    foreach ($task in $scheduledTasks) {
        if ($task.Actions.Execute -and $cmdline -like "*$($task.Actions.Execute)*") { $persistence = 1; break }
    }

    # Heuristic 2: Network Access
    $networkAccess = ($netConnections | Where-Object { $_.OwningProcess -eq $procId }).Count -gt 0

    # Heuristic 3: File Write (uses SysInternals Handle tool if available)
    $fileWrite = 0
    try {
        $handleList = (Handle.exe -p $procId | Select-String -Pattern "\.txt|\.log|\.dat" | Out-String)
        if ($handleList) { $fileWrite = 1 }
    } catch { }

    # Heuristic 4: Script-based execution
    $scriptBased = 0
    if ($cmdline -match "python|powershell|perl|ruby|vbs|bat") { $scriptBased = 1 }

    $line = "$procId,$ppid,""$exe"",""$shortCmd"",$persistence,$networkAccess,$fileWrite,$scriptBased"
    $output += $line
}

# Output to CSV
$output | Set-Content -Path $csvPath -Encoding UTF8
Write-Output "Saved to $csvPath"
