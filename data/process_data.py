import pandas as pd
import os

def load_linux_data(fp):
    if not os.path.exists(fp):
        raise FileNotFoundError(f"{fp} not found!")
    f = pd.read_csv("lpdata.csv")
    print("Linux Data loaded")
    print(f"{dfile.head()}")
    return f

def clean_linux_data(f):
    f.dropna(inplace=True)
    f["cpu"] = f.to_numeric(f["cpu"],errors="coerce")
    f["mem"] = f.to_numeric(f["mem"],errors="coerce")
    f["label"] = f["label"].astype(int)
    f.dropna(inplace=True)
    return f

def put_data(f,op):
    f.to_csv(op,index=False)
    print("Cleaned data saved in path")

def main():
    df = load_linux_data("linux/lpdata.csv")
    df = clean_linux_data(df)
    put_data(df,"flidata.csv")

if __name__=="__main__":
    main()
