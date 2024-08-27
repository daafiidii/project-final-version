import tkinter as tk
import pyttsx3
import pyaudio
from vosk import Model, KaldiRecognizer
import os
import json
import threading
from email_module.send_email import send_email
from email_module.read_emails import read_emails
import time


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech_vosk():
    model_path = "vosk-model-small-en-us-0.15" 

    if not os.path.exists(model_path):
        print("Please download the Vosk model and place it in the specified path.")
        return

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            recognized_text = result_json.get("text", "")
            if recognized_text:
                print(f"Recognized text: {recognized_text}")
                return recognized_text.lower()

def gather_email_details():
  
    speak("Please provide the recipient's email username. Say each letter clearly without spaces.")
    username = recognize_speech_vosk().replace(" ", "")  
   
    speak("Choose the domain for the email address.")
    speak("Say number 1 for @gmail.com.")
    speak("Say number 2 for @yahoo.com.")
    speak("Say number 3 for @outlook.com.")
    speak("Say number 4 for @icloud.com.")
    
    domain_choice = recognize_speech_vosk()
    
    domains = {
        "one": "gmail.com",
        "two": "yahoo.com",
        "three": "outlook.com",
        "four": "icloud.com"
    }
    
    domain = domains.get(domain_choice, "gmail.com")  
    
    recipient_email = f"{username}@{domain}"
  
    speak(f"The email address is {recipient_email}. Is this correct?")
    confirmation = recognize_speech_vosk()
    
    if "yes" not in confirmation:
        speak("Let's try again.")
        return gather_email_details()  


    speak("What is the subject of your email?")
    subject = recognize_speech_vosk()
    

    speak("Do you want to send a text message or an audio message?")
    speak("Say number one for text or number two for audio.")
    message_type_choice = recognize_speech_vosk()
    
    if "one" in message_type_choice:
        message_type = "text"
    elif "two" in message_type_choice:
        message_type = "audio"
    else:
        speak("Sorry, I didn't understand that. Sending email as audio by default.")
        message_type = "Audio"
    
    return recipient_email, subject, message_type

def show_success_popup():
    popup = tk.Toplevel(root)
    popup.title("Success")
    popup.geometry("300x100")
    label = tk.Label(popup, text="Email sent successfully!", font=("Inter", 14))
    label.pack(expand=True)
    
    # Close the popup automatically after 10 seconds
    popup.after(10000, popup.destroy)

def start_conversation():
    speak("Welcome to the Auditory-Based Email System!")
    speak("What would you like to do today?")
    speak("You can say send email, read emails, listen to audio, or exit.")

    while True:
        choice = recognize_speech_vosk()
        if choice is None:
            continue  
        elif "send" in choice:
            recipient_email, subject, message_type = gather_email_details()
            if message_type == "text":
                speak("What is the message?")
                message_content = recognize_speech_vosk()
            else:
                message_content = None 

            try:
                send_email(recipient_email, subject, message_type, message_content)
                show_success_popup()
            except Exception as e:
                speak("Sorry, the message couldn't be sent as a result of wrong information.")
            break
        elif "read" in choice:
            read_emails()  
            break
        elif "listen" in choice:
            speak("Listening to audio feature is under development.")
            break
        elif "exit" in choice:
            speak("Exiting the program. Goodbye!")
            root.quit()
            return
        else:
            speak("Sorry, I didn't understand that. Please say send email, read emails, listen to audio, or exit.")
            continue

def start_gui():
    global root
    root = tk.Tk()
    root.title("Auditory-Based Email System")
    root.geometry("900x650")
    root.configure(bg="#ffffff") 

    font_heading = ("Inter", 20, "bold")
    font_regular = ("Inter", 14)

    welcome_label = tk.Label(root, text="Welcome to\nAuditory Based\nEmail System", font=font_heading, fg="#000000", bg="#ffffff")
    welcome_label.pack(pady=20)

    def create_gradient_button(text):
        button = tk.Button(
            root, text=text, font=font_regular, fg="#ffffff", width=20, height=2,
            relief="flat", bg="#6471E3", activebackground="#394297", bd=0
        )
        return button

    send_email_button = create_gradient_button("Send Email")
    send_email_button.pack(pady=10)

    read_email_button = create_gradient_button("Read Emails")
    read_email_button.pack(pady=10)

    exit_button = create_gradient_button("Exit")
    exit_button.pack(pady=10)

    root.after(1000, lambda: threading.Thread(target=start_conversation).start())  

    root.mainloop()

if __name__ == "__main__":
    start_gui()
