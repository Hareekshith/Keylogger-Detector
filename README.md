![screenshots](https://raw.githubusercontent.com/hareekshith/keylogger-detection/main/poster_final.webp)

# Keylogger-detector
A project to detect keyloggers in the system either in signature or a program! For Linux

## How to Detect
* Execute the `main.py` file by running the command `python3 main.py`.
* The final output will be displayed in the terminal. 
* The dataset will then be stored in `data/linux/linux_features1.csv`

## What Actually is Happening
Below is the detailed explanation on how each file performs their task. 
### `collect_data.sh`
* Collects metrics data for each PID which is active. 
* Runs 5 heuristics (Persistence, Script-Based, File-Writing, Input-Tapping and Network Access).
* Awards 1 if yes and 0 if no. 
* All these datas are collected and stored in a CSV, this process is repeated 10 times. 
### `extract_linfeatures.py`
* Uses Panda to classify each CSV values into the respective variables. 
* Uses a Tiered Heuristic logic to determine whether any of the particular file has a suspicious behavior. 
* This process is repeated for all the remaining collected sample data. 
### `safe.txt`
* The file contains all the whitelisted process names so, it does not return any false positives. 
### `stejkeu.py & keylogger_m2.py`
* These are the sample keylogger programs that were created to test the detector.

## Author
Hareekshith AS

## License
This project is licensed under the terms of the GPL-3.0 license.

## Want to collaborate? 
Feel free to open an issue or submit a pull request!