import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("\n")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening.....")
        audio = recognizer.listen(source)

    print("Recognizing.....")
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return None

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    play(audio)
    os.remove("output.mp3")

    



if __name__ == "__main__":
    text = recognize_speech_from_mic()
    if text:
        response = "I didn't understand that."  # Default response

        if "how are you" in text.lower():
            response = "I am fine, what about you sir?"
        elif "what is your name" in text.lower():
            response = "My name is A.C.E"
        elif "what time is it" in text.lower():
            response = "I don't have a clock, but you can check your device."
        elif "tell me a joke" in text.lower():
            response = "Why don't scientists trust atoms? Because they make up everything!"

        text_to_speech(response)
