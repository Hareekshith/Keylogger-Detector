import pandas as pd
import os

#function to create a file object and return it for the upcoming functions
def load_linux_data(fp):
    if not os.path.exists(fp):
        raise FileNotFoundError(f"{fp} not found!")
    f = pd.read_csv("linux/lpdata.csv")
    print("Linux Data loaded")
    print(f"{f.head()}")
    return f

#function to delete the rows with NaN and convert cpu,mem and label to readable format!
def clean_linux_data(f):
    f.dropna(inplace=True)
    f["cpu"] = pd.to_numeric(f["cpu"],errors="coerce")
    f["mem"] = pd.to_numeric(f["mem"],errors="coerce")
    f["label"] = f["label"].astype(int)
    f.dropna(inplace=True)
    return f

#function to insert the data to the finalised clean flidata.csv
def put_data(f,op):
    f.to_csv(op,index=False)
    print("Cleaned data saved in path")

#function which calls all the other functions while initialising the paths
def main():
    df = load_linux_data("linux/lpdata.csv")
    df = clean_linux_data(df)
    put_data(df,"flidata.csv")

if __name__=="__main__":
    main()
