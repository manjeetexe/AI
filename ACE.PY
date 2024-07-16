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
        response = "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        response = "Could not request results from Google Speech Recognition service; {e}"
    return None

def text_to_speech(text):
    synthesizer = NSSpeechSynthesizer.alloc().init()
    synthesizer.startSpeakingString_(text)
    while synthesizer.isSpeaking():  # Wait until the synthesizer finishes speaking
        time.sleep(0.1)

def wish():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        response = "Good morning. I am ZENOX. How can I assist you?"
    elif 12 <= hour < 18:
        response = "Good afternoon. I am ZENOX. How can I assist you?"
    else:
        response = "Good evening. I am ZENOX. How can I assist you?"

    print(response)
    text_to_speech(response)

def open_terminal():
    subprocess.call(["open", "-a", "Terminal"])

daily_routine = {
    "morning": "7:00 AM - Wake up and exercise.\n9:00 AM - Have breakfast.\n10:00 AM - Start studying.",
    "afternoon": "12:00 PM - Lunch break.\n3:00 PM - repeate studing part.\n5:00 PM - practice coding.",
    "evening": "6:00 PM - Dinner.\n7:00 PM - repeate the coding part.\n11:00 PM - break time and can have fun.\n1:00 AM - sleeping time"
                }


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

def security_questions(recognizer, microphone):
    questions = [
        "What is your name?",
        "What is your lucky number?",
        "what is the password ?"
    ]

    responses = [
        "My name is Manjeet",
        "7",
        "My password is 9370 612327"
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
                response = "Locking ZENOX."
                print(f"Assistant will say: {response}")
                text_to_speech(response)
                break 

            if any(keyword in text.lower() for keyword in ["how are you", "how r u", "how are u","how r you"]):
                response = "I'm fine, what about you sir"
            elif any(keyword in text.lower() for keyword in ["i am also fine", "i am fine to", "i am good"]):
                response = "that's great, how can i assist you today?"
            elif any(keyword in text.lower() for keyword in ["little bit sad", "not good ", "i am not well","felling lonely"]): 
                response = "I am always here for you sir,tell me if i can help you"   
            elif "NO it's not an big thing" in text.lower():
                response = "Ok sir, so how can i assist you today sir" 
            elif "what is your name" in text.lower():
                response = "My name is ZENOX,how can i assist you sir."
            elif "who is your creator" in text.lower():
                response = "My creator is Manjeet Sharma."   
            elif "tell me something about you" in text.lower():
                response = "I am an artificial intelligence assistant name ZENOX,I built on june 29 2024,I designed to help and assist my master."
            elif any(keyword in text.lower() for keyword in ["what is my mother's name", "what is name of my mother", "mother name","mother's name"]):
                response = "your's mother name is Neetu Sharma"
            elif "open terminal" in text.lower():
                response = "Opening terminal."
                open_terminal()
            elif "close terminal" in text.lower():
                response = "Closing terminal."
                close_terminal()
            elif "today's routine" in text.lower() or "what is my today routine" in text.lower():
                # Determine the part of the day
                hour = datetime.datetime.now().hour
                if 5 <= hour < 12:
                    part_of_day = "morning"
                elif 12 <= hour < 17:
                    part_of_day = "afternoon"
                else:
                    part_of_day = "evening"

                response = f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}. Here's your {part_of_day} routine:\n{daily_routine.get(part_of_day, 'No specific routine planned.')}"
            elif "open camera" in text.lower():
                response = "Opening camera."
                open_camera()
            elif "close camera" in text.lower():
                response = "Closing camera."
                close_camera()
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

