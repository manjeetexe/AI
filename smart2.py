import os
import boto3
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("\n")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
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

def text_to_speech(text, voice_id='Matthew', region_name='us-east-1'):
    polly_client = boto3.Session(
        aws_access_key_id='manjeet.exe',
        aws_secret_access_key='manjeet.exe',
        region_name=region_name
    ).client('polly')

    response = polly_client.synthesize_speech(VoiceId=voice_id,
                                              OutputFormat='mp3', 
                                              Text=text)
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

    audio = AudioSegment.from_mp3('output.mp3')
    play(audio)
    os.remove('output.mp3')

if __name__ == "__main__":
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
            elif "tell me a joke" in text.lower():
                response = "Why don't scientists trust atoms? Because they make up everything!"
            elif "stop" in text.lower():
                response = "Goodbye!"
                print(f"Assistant will say: {response}")
                text_to_speech(response)
                break

            print(f"Assistant will say: {response}")
            text_to_speech(response)
