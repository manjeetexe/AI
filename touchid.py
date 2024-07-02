import speech_recognition as sr
from AppKit import NSSpeechSynthesizer
import datetime
import cv2
import time
from Foundation import NSBundle
import objc
import ctypes

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

def authenticate_with_touchid():
    try:
        # Import necessary frameworks
        LocalAuthentication = NSBundle.bundleWithPath_('/System/Library/Frameworks/LocalAuthentication.framework')
        objc.loadBundle(LocalAuthentication, globals(), bundle_path='/System/Library/Frameworks/LocalAuthentication.framework')

        # Define types and functions from LocalAuthentication
        NSError_ptr = ctypes.POINTER(ctypes.c_void_p)
        context = objc.objc_getClass('LAContext').alloc().init()
        context.canEvaluatePolicy_error_(objc.LAPolicyDeviceOwnerAuthenticationWithBiometrics, None)
        
        # Perform biometric authentication
        if context.canEvaluatePolicy_error_(objc.LAPolicyDeviceOwnerAuthenticationWithBiometrics, None):
            auth_result, error = context.evaluatePolicy_localizedReason_reply_(
                objc.LAPolicyDeviceOwnerAuthenticationWithBiometrics,
                "Authenticate to unlock ACE assistant",
                None
            )
            if auth_result:
                return True
            else:
                print(f"Authentication failed: {error}")
                return False
        else:
            print("Biometric authentication not available.")
            return False

    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return False

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Perform Touch ID authentication
    if not authenticate_with_touchid():
        print("Touch ID authentication failed.")
        text_to_speech("Touch ID authentication failed. Access denied.")
        return

    # Once authenticated, start assistant loop
    wish()

    while True:
        text = recognize_speech_from_mic(recognizer, microphone)
        if text:
            print(f"Recognized text: {text}")

            if "lock ACE" in text.lower():
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
            elif "open camera" in text.lower():
                response = "Opening camera."
                open_camera()
            elif "close camera" in text.lower():
                response = "Closing camera."
                close_camera()
            elif any(keyword in text.lower() for keyword in ["what time is it", "tell me the time", "what is the time"]):
                get_time()
                continue
            elif "repeat what you say" in text.lower() or "say that again" in text.lower() or "repeat" in text.lower():
                response = last_text
            else:
                response = "I'm sorry, I don't understand that command."

            print(f"Assistant: {response}")
            text_to_speech(response)

if __name__ == "__main__":
    main()

