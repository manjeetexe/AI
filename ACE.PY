#modules
import os
import datetime
import speech_recognition as sr
from AppKit import NSSpeechSynthesizer
import subprocess

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("\n")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening.....") 
        audio = recognizer.listen(source)

    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return None
#text to speech
def text_to_speech(text):
    synthesizer = NSSpeechSynthesizer.alloc().init()
    synthesizer.startSpeakingString_(text)

# to wish 
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

#terminal
def open_terminal():
    subprocess.call(["open", "-a", "Terminal"])

#main function
def main():
    wish()
    while True:
        text = recognize_speech_from_mic()
        if text:
            response = "say that again please"  # Default response

            if "how are you" in text.lower():
                response = "I am fine, what about you sir?"
            elif "what is your name" in text.lower():
                response = "My name is ACE"
            elif "what time is it" in text.lower():
                response = "I don't have a clock, but you can check your device."
            elif "open terminal" in text.lower():
                response = "Opening terminal"
                open_terminal()
            elif "stop" in text.lower():
                response = "thankyou sir Goodbye!"
                print(f"Assistant will say: {response}")
                text_to_speech(response)
                break

            print(f"Assistant will say: {response}")
            text_to_speech(response)

if __name__ == "__main__":
    main()

