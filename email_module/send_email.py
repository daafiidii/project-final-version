import pyttsx3
import smtplib
import speech_recognition as sr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sounddevice as sd
import soundfile as sf

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_audio(filename):
    speak("This recording will last 30 seconds. Please speak into the microphone. Recording starts now.")
    duration = 30  
    fs = 44100  
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  
    sf.write(filename, myrecording, fs)
    speak("Recording complete.")

def send_email(recipient_email, subject, message_type, message_content=None):
    sender_email = "adeoyed7@gmail.com"  
    password = "oolg wyzx xqbv rhnk"  

    if message_type == "text":  
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_content, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.close()
            speak("Email sent successfully.")
        except Exception as e:
            speak(f"Failed to send email. Error: {str(e)}")

    elif message_type == "audio": 
        filename = "audio_message.wav"
        record_audio(filename)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={filename}")
                msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.close()
            speak("Email with audio attachment sent successfully.")
        except Exception as e:
            speak(f"Failed to send email. Error: {str(e)}")

