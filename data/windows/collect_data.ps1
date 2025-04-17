# Create the samples directory if it doesn't exist
if (!(Test-Path -Path "samples")) {
    New-Item -ItemType Directory -Path "samples" | Out-Null
}

# Prepare an array to collect data
$processData = @()

# Output CSV header
$header = "PID,PPID,Executable,CommandLine,Startup,NetworkAccess,FileWrite,ScriptBased,InputTap"
$header | Out-File -Encoding UTF8 -FilePath "samples\processes.csv"

# Get all processes
Get-Process | ForEach-Object {
    try {
        # Get Process Information
        $processId = $_.Id
        $ppid = (Get-WmiObject Win32_Process -Filter "ProcessId = '$processId'" | Select-Object -ExpandProperty ParentProcessId)
        $exe = $_.Path

        # Get CommandLine using WMI
        $cmd = (Get-WmiObject Win32_Process -Filter "ProcessId = '$processId'" | Select-Object -ExpandProperty CommandLine)

        # Fallback for null values
        if (-not $exe) { $exe = "N/A" }
        if (-not $cmd) { $cmd = "N/A" }

        # Heuristic 1: Suspicious directories (like temp or user profile)
        $suspicious = "no"
        if ($exe -match "Users\\.*\\AppData\\|Temp\\|Downloads") {
            $suspicious = "yes"
        }

        # Heuristic 2: Script-based (PowerShell, Python, etc.)
        $scriptBased = "no"
        if ($cmd -match "powershell|python|wscript|cscript|cmd|batch") {
            $scriptBased = "yes"
        }

        # Heuristic 3: File writing (recently accessed .txt/.log/.dat files)
        $fileWrite = "no"
        try {
            $processHandles = (.\handle64.exe -p $processId -nobanner 2>$null) -join "`n"
            
            # Check if the process is handling specific file types (e.g., .txt, .log, .dat)
            if ($processHandles -match "\.txt|\.log|\.dat") {
                $fileWrite = "yes"
            }
        } catch {
            $fileWrite = "no" # If handle64 is unavailable or fails
        }

        # Heuristic 4: Network access (check if it opened any connections)
        $netAccess = "no"
        try {
            $netstat = netstat -ano | Select-String ":.ESTABLISHED.$processId"
            if ($netstat) {
                $netAccess = "yes"
            }
        } catch {
            $netAccess = "no" # If netstat command fails or no network access found
        }

        # Heuristic 5: Startup presence (registry autorun or startup folder)
        $startup = "no"
        try {
            $paths = @(
                "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
                "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
            )
            foreach ($path in $paths) {
                $items = Get-ItemProperty -Path $path -ErrorAction SilentlyContinue
                foreach ($item in $items.PSObject.Properties) {
                    if ($item.Value -like "$exe") {
                        $startup = "yes"
                        break
                    }
                }
            }
        } catch {
            $startup = "no" # If registry query fails
        }

        # Heuristic 6: Input tapping (low-level hooks - limited in userland)
        $inputTap = "no"
        if ($cmd -match "SetWindowsHookEx|WH_KEYBOARD_LL|WH_JOURNALRECORD") {
            $inputTap = "yes"
        }

        # Create output object
        $processDataObject = [PSCustomObject]@{
            PID         = $processId
            PPID        = $ppid
            Executable  = $exe
            CommandLine = $cmd
            Startup     = $startup
            NetworkAccess = $netAccess
            FileWrite   = $fileWrite
            ScriptBased = $scriptBased
            InputTap    = $inputTap
        }

        # Append the process information to the CSV file
        $processDataObject | Export-Csv -Path "samples\processes.csv" -NoTypeInformation -Append

    } catch {
        continue
    }
}

Write-Host "Process data collection complete!"