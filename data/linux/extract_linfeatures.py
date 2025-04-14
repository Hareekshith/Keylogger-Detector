import pandas as pd
import os

#A list which contains the directories where no files are run usually 
sus_path=["/tmp","/dev/shm","/var/tmp","/.cache","/.config"]

#function to use the sus_path and returns if it matches
def susp(path):
    return any(path.startswith(sp) for sp in sus_path)

#function which checks three conditions for detection of keylogger
def sus(r):
    s=0
    if 'p' in r and isinstance(r['p'],str):
        if susp(r['p']): #checks whether the path is suspicious
            s+=1
        if 'p' in r and '/.' in r['p']: #checks whether the path contains /. in path, usually no file should be running
            s+=1
        if 'ai' in r and r['ai'] == 1: # checks whether the input is accessed
            s+=1
    return 1 if s>=2 else 0

def main():
    f = pd.read_csv("samples/ldata41.csv", sep = "|", names=["pid","process","cpu","memory","p","pid"])
    f['label'] = f.apply(sus,axis=1)
    f.to_csv("csamples/flidata.csv", index=False)
    #prints the ones who's label is 1
    print(f[f["label"] == 1][["pid", "process"]])

if __name__=="__main__":
    main()
