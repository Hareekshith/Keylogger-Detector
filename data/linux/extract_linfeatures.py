import pandas as pd

#creates a csv object to access its content
df = pd.read_csv("ldata.csv",sep="|",names=["pid","process_name","cpu","mem"])

#convert the values of cpu and memory to numerals
df["cpu"] = pd.to_numeric(df["cpu"],errors="coerce")
df["mem"] = pd.to_numeric(df["mem"],errors="coerce")

#keylogger identification list
sus = ["keylogger","klgr","hooker","logkey","logger"]

#keylogger indentification function
def is_sus(pn):
    if not isinstance(pn,str):
        return 0
    else:
        return any(k in pn.lower() for k in sus)

#label: detects whether it is a keylogger or not
df["label"] = df["process_name"].apply(lambda x: 1 if is_sus(x) else 0)

#Deletes the NaN rows, keeping the only required rows!
df.dropna(inplace=True)

#shifting the updated data with label
df.to_csv("lpdata.csv",index=False)

#prints the ones who's label is 1
print(df[df["label"] == 1][["pid", "process_name"]])
