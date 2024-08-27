import imaplib
import email
from email.header import decode_header
import pyttsx3
import os
import webbrowser

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def save_attachment(part, download_folder="attachments"):
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)
    filename = part.get_filename()
    filepath = os.path.join(download_folder, filename)
    with open(filepath, "wb") as f:
        f.write(part.get_payload(decode=True))
    return filepath

def read_emails():
    username = "adeoyed7@gmail.com"
    password = "oolg wyzx xqbv rhnk"
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login(username, password)
    server.select("inbox")

    status, messages = server.search(None, "ALL")
    email_ids = messages[0].split()

    speak("Welcome, your account is logged in. I will read the first 5 recent emails you received.")
    
    for i in range(5):
        email_id = email_ids[-(i + 1)]
        status, msg_data = server.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
            
                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding if encoding else "utf-8")

                subject, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                speak(f"Email {i + 1}. From: {sender}. Subject: {subject}.")
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            speak(part.get_payload(decode=True).decode())
                        elif part.get_content_maintype() == "audio":
                            filepath = save_attachment(part)
                            speak(f"Audio attachment {part.get_filename()} has been saved.")
                            engine.stop()
                            webbrowser.open(filepath)
                            server.logout()
                            return
                else:
                    speak(msg.get_payload(decode=True).decode())

    speak("You have reached the end of the recent emails.")
    server.logout()
