import speech_recognition as sr
import webbrowser
import pyttsx3

# Initialize text-to-speech engine once
engine = pyttsx3.init()

def speak(text):
    """Speak the provided text."""
    print(f"Speaking: {text}")  # Debugging log to see what's being spoken
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for a voice command and return the recognized text."""
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            listener.energy_threshold = 300  # Predefined noise level threshold
            listener.dynamic_energy_threshold = False  # Avoid recalculating noise levels
            print("Listening...")
            speak("How can I help you?")
            voice = listener.listen(source, timeout=3, phrase_time_limit=5)
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
    speak("Hello, I'm ready for your command.")
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
