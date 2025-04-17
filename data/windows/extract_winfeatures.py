import pandas as pd
import os

def load_data(path):
    print(f"[1] Loading data from {path}...")
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None
    df = pd.read_csv(path)
    print(f"📊 Columns found: {list(df.columns)}")
    return df

def clean_data(df):
    print("[2] Cleaning data...")

    df = df.dropna()

    # Adjust column names if necessary
    if 'cpu' in df.columns:
        df['cpu'] = df['cpu'].astype(float)
    if 'mem' in df.columns:
        df['mem'] = df['mem'].astype(float)

    df = df.drop_duplicates()

    return df

def label_data(df):
    print("[3] Labeling data...")

    def detect_keylogger(row):
        score = 0
        if 'keyboard' in str(row.get('CommandLine', '')).lower():
            score += 1
        if str(row.get('ScriptBased', '')).lower() == 'yes':
            score += 1
        if str(row.get('InputTap', '')).lower() == 'yes':
            score += 1
        if str(row.get('FileWrite', '')).lower() == 'yes':
            score += 1
        if str(row.get('NetworkAccess', '')).lower() == 'yes':
            score += 1
        return 1 if score >= 3 else 0  # 1 = keylogger, 0 = benign

    df['label'] = df.apply(detect_keylogger, axis=1)
    return df

def save_data(df, output_path):
    print(f"[4] Saving labeled data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("[✅] Processing complete.")

def main():
    input_path = "data/windows/samples/processes.csv"
    output_path = "data/windows/samples/processed_data.csv"

    df = load_data(input_path)
    if df is not None:
        df = clean_data(df)
        df = label_data(df)
        save_data(df, output_path)

if __name__ == "__main__":
    main()
