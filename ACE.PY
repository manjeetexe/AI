import datetime
import speech_recognition as sr
from AppKit import NSSpeechSynthesizer
import subprocess
import cv2
from Foundation import NSObject, NSApplication
import AppKit

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        pass
    
    def applicationSupportsSecureRestorableState_(self, app):
        return True

last_text = ""  # Variable to store the last recognized text

def recognize_speech_from_mic():
    global last_text
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("\n")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...") 
        audio = recognizer.listen(source)

    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        last_text = text.strip()  # Store the last recognized text (stripped of leading/trailing whitespace)
        return last_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return None

def text_to_speech(text):
    synthesizer = NSSpeechSynthesizer.alloc().init()
    synthesizer.startSpeakingString_(text)

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        response = "Good morning. I am ACE sir. Please tell me how can I help you."
    elif hour >= 12 and hour < 18:
        response = "Good afternoon. I am ACE sir. Please tell me how can I help you."
    else:
        response = "Good evening. I am ACE sir. Please tell me how can I help you."

    print(response)
    text_to_speech(response)

def open_terminal():
    subprocess.call(["open", "-a", "Terminal"])

def close_terminal():
    subprocess.call(["osascript", "-e", 'tell application "Terminal" to quit'])

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")   
            break

        cv2.imshow('camera', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def close_camera():
    global cap
    if cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed")

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    response = f"The time is {current_time}."
    print(response)
    text_to_speech(response)

def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    
    wish()
    
    global last_text  # Use the global variable for last recognized text
    
    while True:
        text = recognize_speech_from_mic()
        if text:
            print(f"Recognized text: {text}")  # Debugging statement
            response = "Say that again please"  # Default response

            if "how are you" in text.lower():
                response = "I am fine, what about you sir?"
            elif "what is your name" in text.lower():
                response = "My name is ACE"
            elif "who is your master" in text.lower():
                response = "My master name is Manjeet Sharma, I am his A.I assistant ACE"
            elif "tell me something about you" in text.lower():
                response = "I'm an A.I language model created by Manjeet.i am built on 29 june 2024"
            elif "open terminal" in text.lower():
                response = "Opening terminal"
                open_terminal()
            elif "close terminal" in text.lower():
                response = "Closing terminal"   
                close_terminal()
            elif "open camera" in text.lower():
                response = "Opening camera"
                open_camera()
            elif "close camera" in text.lower():
                response = "Closing camera"   
                close_camera()
            elif any(keyword in text.lower() for keyword in ["what time is it", "tell me the time", "what is the time"]):
                get_time()
                continue
            elif "repeat what you say" in text.lower() or "say that again" in text.lower() or "repeat" in text.lower():
                response = last_text  # Repeat the last recognized text
            elif "stop" in text.lower():
                response = "Thank you sir, Goodbye!"
                print(f"Assistant: {response}")
                text_to_speech(response)
                break

            print(f"Assistant: {response}")
            text_to_speech(response)

if __name__ == "__main__":
    main()


