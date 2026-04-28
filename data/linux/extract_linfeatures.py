import pandas as pd
import os
import glob

IGNORE_PROCESSES = ['firefox', 'chrome', 'brave', 'gnome-shell']

def process_all_samples(samples_dir, output_file):
    all_files = glob.glob(os.path.join(samples_dir, "*.csv"))
    df_list = []
    
    for file in all_files:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            
    if not df_list:
        print("No sample files found.")
        return
        
    # Combine all sample data
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Drop NaN values to create a cleaned CSV
    combined_df.dropna(inplace=True)
    
    # Classify each CSV value (yes -> 1, no -> 0)
    cols_to_map = ['startup', 'NetworkAccess', 'FileWrite', 'ScriptBased', 'InputTap']
    for col in cols_to_map:
        if col in combined_df.columns:
            combined_df[col] = combined_df[col].map({'yes': 1, 'no': 0}).fillna(0).astype(int)
            
    # Tiered Heuristic logic
    def apply_heuristic(row):
        process_name = str(row['process']).lower()
        if any(ignore in process_name for ignore in IGNORE_PROCESSES):
            return 0
            
        startup = row['startup']
        network = row['NetworkAccess']
        file_write = row['FileWrite']
        script = row['ScriptBased']
        input_tap = row['InputTap']
        
        # Refined tiered logic for keylogger detection
        if (
            (network and script) or 
            (file_write and script) or
            (startup and input_tap) 
        ):
            return 1
        return 0

    combined_df['label'] = combined_df.apply(apply_heuristic, axis=1)
    
    # Save to the output CSV
    combined_df.to_csv(output_file, index=False)
    print(f"Cleaned features saved to {output_file}")

if __name__ == '__main__':
    process_all_samples('samples', 'linux_features1.csv')
