import os
import subprocess
import sys
import csv

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    linux_dir = os.path.join(base_dir, "data", "linux")
    
    print("[*] Step 1: Running collect_data.sh to gather system metrics...")
    try:
        # Suppress stderr to hide "No such file or directory" errors for transient /proc/ files
        subprocess.run(["bash", "./collect_data.sh"], cwd=linux_dir, check=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"[-] Data collection failed: {e}")
        sys.exit(1)
        
    print("[*] Step 2: Extracting and cleaning features from collected samples...")
    # Make sure we use the virtualenv python if we created one, or sys.executable
    venv_python = os.path.join(linux_dir, "venv", "bin", "python3")
    python_cmd = venv_python if os.path.exists(venv_python) else sys.executable
    
    script_path = os.path.join(linux_dir, "extract_linfeatures.py")
    try:
        subprocess.run([python_cmd, script_path], cwd=linux_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Feature extraction failed: {e}")
        sys.exit(1)
        
    print("[+] Feature extraction complete.")
    
    # Analyze the results and display them
    results_file = os.path.join(linux_dir, "linux_features1.csv")
    keyloggers = set()
    
    if os.path.exists(results_file):
        with open(results_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('label') == '1':
                    process_name = row.get('process', 'Unknown')
                    keyloggers.add(process_name)
                    
        print("\n" + "="*50)
        print("          KEYLOGGER DETECTION RESULTS")
        print("="*50)
        
        if keyloggers:
            print("[!!!] WARNING: Potential keylogger signature(s) detected!")
            print("      Suspicious processes identified:")
            for kl in sorted(keyloggers):
                print(f"      - {kl}")
        else:
            print("[+] SUCCESS: No keylogger signatures detected on the system.")
            
        print("="*50 + "\n")
        print(f"Full dataset available at: {os.path.relpath(results_file, base_dir)}")
    else:
        print("[-] Error: Output file not found. Could not display results.")

if __name__ == "__main__":
    main()
