import speech_recognition as sr
import webbrowser
from google.cloud import texttospeech  # Import google-cloud-texttospeech
import time

# Initialize the Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

def speak(text):
    """Speak the provided text using google-cloud-texttospeech."""
    print(f"Speaking: {text}")  # Debugging log to see what's being spoken

    # Synthesize speech from the text
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Request speech synthesis
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save audio to a file and play it
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    # Optionally, play the audio on the system
    import os
    os.system("mpg321 output.mp3")
    time.sleep(1)  # Ensure a brief pause after speech for synchronization

def take_command():
    """Listen for a voice command and return the recognized text."""
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            listener.energy_threshold = 300  # Predefined noise level threshold
            listener.dynamic_energy_threshold = False  # Avoid recalculating noise levels
            print("Listening...")
            speak("How can I help you?")
            voice = listener.listen(source, timeout=5, phrase_time_limit=10)  # Increased timeout and phrase time limit
            command = listener.recognize_google(voice).lower()  # Convert to lowercase text
            print(f"You said: {command}")
            return command
    except (sr.WaitTimeoutError, sr.UnknownValueError) as e:
        print(f"Error: {e}")
        speak("I didn't hear anything or couldn't understand. Please try again.")
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred. Please try again.")
    return ""

def is_health_related(query):
    """Determine if the query is related to health symptoms."""
    health_keywords = ["symptom", "disease", "fever", "cough", "headache", "pain", "COVID-19",
                       "stomach", "flu", "cold", "infection", "rash", "injury", "health"]
    return any(keyword in query for keyword in health_keywords)

def search(query, site="google"):
    """Search using the specified website."""
    try:
        if site == "nhs":
            speak(f"Searching for information about {query} on the NHS website.")
            nhs_url = f"https://www.nhs.uk/search/results?q={query}"
            webbrowser.open(nhs_url)
            print(f"Opening NHS results: {nhs_url}")
        else:
            speak(f"Searching for {query} on Google.")
            google_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(google_url)
            print(f"Opening Google results: {google_url}")
    except Exception as e:
        print(f"Error during search: {e}")
        speak(f"An error occurred while trying to search on {site}. Please check your internet connection.")

def voice_google_search():
    """Main function to initiate the voice assistant."""
    speak("Hello!")
    command = take_command()

    if command:
        if is_health_related(command):
            search(command, site="nhs")  # Search on NHS if it's health-related
        else:
            search(command)  # Search on Google for general queries
        speak("Your search has been opened in the browser.")
    else:
        speak("I couldn't process your request. Please try again.")

if __name__ == "__main__":
    try:
        voice_google_search()
    except KeyboardInterrupt:
        print("Program terminated.")
        speak("Goodbye! Have a great day.")
