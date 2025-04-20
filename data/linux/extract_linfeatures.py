import csv

#parses yes as 1 and no as 0
def pb(p):
    return 1 if p=="yes" else 0

# List of processes to ignore, like well-known browsers
IGNORE_PROCESSES = ['firefox', 'chrome', 'brave', 'gnome-shell']

def is_keylogger(process):
    startup = int(pb(process['startup']))
    network = int(pb(process['NetworkAccess']))
    file_write = int(pb(process['FileWrite']))
    script = int(pb(process['ScriptBased']))
    input_tap = int(pb(process['InputTap']))
    process_name = process['process'].lower()
    # Exclude well-known processes like browsers
    if any(ignore in process_name for ignore in IGNORE_PROCESSES):
        return 0

    # Refined tiered logic for keylogger detection
    if (
        (network and script) or 
        (file_write and script) or
        (startup and input_tap) 
    ):
        return 1
    return 0

def extract_features(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['label']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row['label'] = is_keylogger(row)
            writer.writerow(row)

if __name__ == '__main__':
    extract_features('samples/ldata56.csv', 'linux_features1.csv')
