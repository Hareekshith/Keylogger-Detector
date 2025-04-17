
echo "PID,PPID,process,Executable,Commandline,Startup,NetworkAccess,FileWrite,ScriptBased,InputTap" > samples/processes.csv

# Define some keywords to ignore (non-keylogger processes)
IGNORE_PROCESSES=("firefox" "chrome" "gnome-shell" "xorg" "gdm")
for i in $(seq 11 20); do
for pid in $(ls /proc | grep -E '^[0-9]+$'); do
    exe_path=$(readlink -f /proc/$pid/exe 2>/dev/null)
    cmdline=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)
    ppid=$(awk '/^PPid:/ {print $2}' /proc/$pid/status 2>/dev/null)
    
    # Get the process name using ps command
    process_name=$(ps -p $pid -o comm= 2>/dev/null)

    # Skip empty exe or command line or ignored processes
    [[ -z "$exe_path" || -z "$cmdline" || " ${IGNORE_PROCESSES[@]} " =~ " $process_name " ]] && continue

    # Heuristic 1: Is the binary in a suspicious directory?
    suspicious_dir="no"
    if [[ "$exe_path" == *"/tmp/"* || "$exe_path" == *"/home/"* || "$exe_path" == *"/.cache/"* || "$exe_path" == *"/var/tmp/"* ]]; then
        suspicious_dir="yes"
    fi

    # Heuristic 2: Is it a script? Refined to include keylogger detection
    script="no"
    # If the cmdline contains a Python keylogger script (keylogger1.py, for example), it's flagged as a script
    if [[ "$cmdline" =~ (python|perl|ruby|bash|sh|node) && "$cmdline" =~ "keylogger" ]]; then
        script="yes"
    fi

    # Heuristic 3: File write detection - only flag writes to suspicious files (e.g., keyloggers usually write to logs)
    file_write="no"
    open_files=$(ls -l /proc/$pid/fd 2>/dev/null | grep -E '.*\.(txt|log|dat)$|/tmp/|/var/tmp/')
    if [[ -n "$open_files" ]]; then
        # Ensure file write happens in suspicious directories (like /tmp)
        suspicious_file_write=$(echo "$open_files" | grep -E '/tmp/|/var/tmp/|/home/')
        if [[ -n "$suspicious_file_write" ]]; then
            file_write="yes"
        fi
    fi

    # Heuristic 4: Input tap detection (/dev/input/* access)
    input_tap="no"
    maps=$(cat /proc/$pid/maps 2>/dev/null | grep "/dev/input/")
    if [[ -n "$maps" ]]; then
        input_tap="yes"
    fi

    # Heuristic 5: Network access (only flag sockets)
    network_access="no"
    net_files=$(ls /proc/$pid/fd 2>/dev/null | xargs -I{} readlink /proc/$pid/fd/{} 2>/dev/null | grep -E 'socket:')
    if [[ -n "$net_files" ]]; then
        network_access="yes"
    fi

    # Heuristic 6: Startup presence - look for executable in startup locations
    startup="no"
    for path in "/etc/init.d/" "/etc/rc*.d/" "$HOME/.config/autostart/" "$HOME/.bashrc" "$HOME/.profile" "/etc/systemd/system/" "/lib/systemd/system/"; do
        grep -q "$exe_path" "$path" 2>/dev/null && startup="yes"
    done

    # Write the results into the CSV file
    echo "$pid,$ppid,$process_name,\"$exe_path\",\"$cmdline\",$startup,$network_access,$file_write,$script,$input_tap" >> samples/ldata$i.csv
done
done
