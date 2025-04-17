import platform

if platform.system() == "Linux":
    print(True)
elif platform.system() == "Windows":
    print(False)
