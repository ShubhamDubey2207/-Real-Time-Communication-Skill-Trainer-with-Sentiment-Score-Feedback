import speech_recognition as sr
from textblob import TextBlob
import threading
import time

transcript = ""
sentiment_score = None
feedback = ""
stop_listening = False

def analyze_sentiment(text):
    if not text.strip():
        return 0.0, "Neutral"
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return polarity, "Positive 😊"
    elif polarity < -0.1:
        return polarity, "Negative 😟"
    else:
        return polarity, "Neutral 😐"

def listen_loop():
    global transcript, sentiment_score, feedback, stop_listening
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Microphone calibrated for ambient noise. Start speaking...")

    while not stop_listening:
        try:
            with mic as source:
                print("\nListening...")
                audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            transcript = text
            sentiment_score, sentiment_label = analyze_sentiment(text)
            feedback = f"Sentiment: {sentiment_label} (score: {sentiment_score:.2f})"
        except sr.WaitTimeoutError:
            transcript = "[No speech detected]"
            feedback = ""
        except sr.UnknownValueError:
            transcript = "[Unrecognized speech]"
            feedback = ""
        except Exception as e:
            transcript = f"[Error: {str(e)}]"
            feedback = ""

        # Print live result
        print(f"Transcript: {transcript}")
        if feedback:
            print(f"{feedback}")
        time.sleep(0.5)

# Start the listening thread
thread = threading.Thread(target=listen_loop, daemon=True)
thread.start()

print("Press Ctrl + C to stop listening.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop_listening = True
    print("\nStopped listening.")
