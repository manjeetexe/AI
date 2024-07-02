import speech_recognition as sr
from AppKit import NSSpeechSynthesizer
import datetime
import subprocess
import cv2
import time
import ctypes
import os

# Global variable to store the last recognized text
last_text = ""

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.strip()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return None

def text_to_speech(text):
    synthesizer = NSSpeechSynthesizer.alloc().init()
    synthesizer.startSpeakingString_(text)
    while synthesizer.isSpeaking():  # Wait until the synthesizer finishes speaking
        time.sleep(0.1)

def wish():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        response = "Good morning. I am ACE. How can I assist you?"
    elif 12 <= hour < 18:
        response = "Good afternoon. I am ACE. How can I assist you?"
    else:
        response = "Good evening. I am ACE. How can I assist you?"

    print(response)
    text_to_speech(response)

def open_terminal():
    subprocess.call(["open", "-a", "Terminal"])

def close_terminal():
    subprocess.call(["osascript", "-e", 'tell application "Terminal" to quit'])

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    response = f"The time is {current_time}."
    print(response)
    text_to_speech(response)

def security_questions(recognizer, microphone):
    questions = [
        "What is your name?",
        "What is your lucky number?",
        "what is the password ?"
    ]

    responses = [
        "Manjeet",
        "thala",
        "9370 612327"
    ]

    # Informing about security questions
    text_to_speech("These are some questions for security purposes.")
    
    for i, question in enumerate(questions):
        print(f"\nListening for: {question}")
        text_to_speech(question)

        # Listen for answer
        while True:
            answer = recognize_speech_from_mic(recognizer, microphone)
            if answer:
                print(f"Recognized answer: {answer}")
                if answer.lower() == responses[i].lower():
                    print("Correct answer!")
                    break
                else:
                    print("Incorrect answer. Please try again.")
                    text_to_speech("Incorrect answer. Please try again.")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Secure unlock phrase
    unlock_phrase = "unlock yourself"

    # Listening for unlock phrase
    while True:
        with microphone as source:
            print("\nListening for unlock phrase...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            phrase = recognizer.recognize_google(audio)
            print(f"Recognized phrase: {phrase}")
            if unlock_phrase in phrase.lower():
                print("Unlock phrase recognized!")
                break

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    # Once unlocked, ask security questions
    security_questions(recognizer, microphone)

    # After successfully answering security questions, start assistant loop
    wish()

    while True:
        text = recognize_speech_from_mic(recognizer, microphone)
        if text:
            print(f"Recognized text: {text}")

            if "lock yourself" in text.lower():
                response = "Locking ACE. Goodbye!"
                print(f"Assistant will say: {response}")
                text_to_speech(response)
                break 

            if "how are you" in text.lower():
                response = "I'm fine, thank you."
            elif "what is your name" in text.lower():
                response = "My name is ACE."
            elif "who is your master" in text.lower():
                response = "My creator is Manjeet Sharma."
            elif "tell me something about you" in text.lower():
                response = "I am an artificial intelligence assistant created by Manjeet. I was built on June 29, 2024."
            elif "open terminal" in text.lower():
                response = "Opening terminal."
                open_terminal()
            elif "close terminal" in text.lower():
                response = "Closing terminal."
                close_terminal()
            elif any(keyword in text.lower() for keyword in ["what time is it", "tell me the time", "what is the time"]):
                get_time()
                continue
            elif "open spotify" in text.lower():
                response = "opening spotify"
                os.system(f"open /Applications/Spotify.app")
            elif "repeat what you say" in text.lower() or "say that again" in text.lower() or "repeat" in text.lower():
                response = last_text
            else:
                response = "I'm sorry,please say it again."

            print(f"Assistant: {response}")
            text_to_speech(response)

if __name__ == "__main__":
    main()

