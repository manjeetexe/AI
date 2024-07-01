import os
import datetime
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

#listining and recognizing
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("\n")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening.....") 
        audio = recognizer.listen(source)

    print("Recognizing,,...")
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
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    play(audio)
    os.remove("output.mp3")


# to wish 
def wish():
    Text = recognize_speech_from_mic()
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        response = "Good morning. I am ACE sir. Please tell me how can I help you."
    elif hour >= 12 and hour < 18:
        response = "Good afternoon. I am ACE sir. Please tell me how can I help you."
    else:
        response = "Good evening. I am ACE sir. Please tell me how can I help you."

    print(response)
    text_to_speech(response)

#main function
def main():
    wish()
    while True:
        text = recognize_speech_from_mic()
        if text:
            response = "I didn't understand that."  # Default response

            if "how are you" in text.lower():
                response = "I am fine, what about you sir?"
            elif "what is your name" in text.lower():
                response = "My name is AI assistant."
            elif "what time is it" in text.lower():
                response = "I don't have a clock, but you can check your device."
            elif "open terminal" in text.lower():
                response = "Why don't scientists trust atoms? Because they make up everything!"
            elif "stop" in text.lower():
                response = "Goodbye!"
                print(f"Assistant will say: {response}")
                text_to_speech(response)
                break

            print(f"Assistant will say: {response}")
            text_to_speech(response)

if __name__ == "__main__":
   main()
   