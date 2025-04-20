# keylogger-detection
A project to detect keyloggers in the system either in signature or a program! For windows and Linux

## Linux
* Navigate to /data/Linux/
* Execute the file collect_data (run `./collect_data.sh`)
* Then execute `python3 extract_linfeatures.py` for a cleaned csv without NaN values

## Windows (Coming Soon!!)
The project is halted for now(for windows!). It will resume after 3 months of time. Till then stay tuned!

### Checks
- [x] Collects Linux system data
- [x] Processes and labels/flags keyloggers of Linux processes
- [x] Collects Windows system data (partial)
- [x] Checks for Windows programs which have persistence
- [ ] Processes and labels/flags keyloggers of Windows processes
- [ ] Enough data collected for model training
- [ ] Model
- [ ] Detects processes easily with the model
