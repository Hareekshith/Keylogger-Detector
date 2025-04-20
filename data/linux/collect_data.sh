#!/bin/bash

mkdir -p samples

# List of known safe processes to skip
IGNORE_PROCESSES=("firefox" "chrome" "gnome-shell" "xorg" "gdm" "brave")

# Function to check if a process should be ignored
is_ignored_process() {
    local pname="$1"
    for ignore in "${IGNORE_PROCESSES[@]}"; do
        if [[ "$pname" == "$ignore" ]]; then
            return 0
        fi
    done
    return 1
}

# Collect data into multiple files for variety
for i in $(seq 51 60); do
    output_file="samples/ldata$i.csv"
    echo "PID,PPID,process,Executable,Commandline,startup,NetworkAccess,FileWrite,ScriptBased,InputTap" > "$output_file"

    for pid in $(ls /proc | grep -E '^[0-9]+$'); do
        # Extract process details
        exe_path=$(readlink -f /proc/$pid/exe 2>/dev/null)
        cmdline=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)
        ppid=$(awk '/^PPid:/ {print $2}' /proc/$pid/status 2>/dev/null)
        process_name=$(ps -p $pid -o comm= 2>/dev/null)

        # Skip invalid or ignored processes
        if [[ -z "$exe_path" || -z "$cmdline" ]]; then
            continue
        fi
        is_ignored_process "$process_name" && continue

        # Heuristic 1: Startup location check
        startup="no"
        for path in "/etc/init.d/" "/etc/rc*.d/" "$HOME/.config/autostart/" "$HOME/.bashrc" "$HOME/.profile" "/etc/systemd/system/" "/lib/systemd/system/"; do
            grep -q "$exe_path" "$path" 2>/dev/null && startup="yes" && break
        done

        # Heuristic 2: Script-based process (esp. keylogger scripts)
        script="no"
        if [[ "$cmdline" =~ (python|perl|ruby|bash|sh|node) && "$cmdline" =~ keylogger ]]; then
            script="yes"
        fi

        # Heuristic 3: File writing in suspicious locations
        file_write="no"
        open_files=$(ls -l /proc/$pid/fd 2>/dev/null | grep -E '.*\.(txt|log|dat)$|/tmp/|/var/tmp/')
        if [[ -n "$open_files" ]]; then
            suspicious_file_write=$(echo "$open_files" | grep -E '/tmp/|/var/tmp/|/home/')
            [[ -n "$suspicious_file_write" ]] && file_write="yes"
        fi

        # Heuristic 4: Input tapping (reads from /dev/input/)
        input_tap="no"
        maps=$(cat /proc/$pid/maps 2>/dev/null | grep "/dev/input/")
        [[ -n "$maps" ]] && input_tap="yes"

        # Heuristic 5: Network access (checks for sockets)
        network_access="no"
        net_files=$(ls /proc/$pid/fd 2>/dev/null | xargs -I{} readlink /proc/$pid/fd/{} 2>/dev/null | grep -E 'socket:')
        [[ -n "$net_files" ]] && network_access="yes"

        # Write results to CSV
        echo "$pid,$ppid,$process_name,\"$exe_path\",\"$cmdline\",$startup,$network_access,$file_write,$script,$input_tap" >> "$output_file"
    done
done

echo "✅ Data collection complete. Check the 'samples/' folder."
