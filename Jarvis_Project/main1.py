import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Your NewsAPI key
newsapi = "a37f8d0cfc154e27aad6ba198bb1465d"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process user commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I could not find the song {song}.")

    elif "news" in c.lower():
        # Make a request to the NewsAPI
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        
        # Print the entire response for debugging
        print(r.json())
        
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Print remaining API requests for debugging
            print(f"Remaining API requests: {r.headers.get('X-RateLimit-Remaining', 'N/A')}")

            # Get the articles list
            articles = data.get('articles', [])
            if articles:
                speak(f"Here are the latest news headlines:")
                for i, article in enumerate(articles[:5], 1):  # Read only top 5 articles
                    headline = article['title']
                    speak(f"Headline {i}: {headline}")
            else:
                speak("Sorry, no news articles were found.")
                print(f"Response did not contain any articles: {data}")
        else:
            speak(f"Failed to retrieve news. Error code: {r.status_code}")
    else:
        pass        

if __name__ == "__main__":
    speak("Jarvis is ready to assist you.")

    while True:
        try:
            print("Recognizing...")
            
            # Listen for activation word
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            word = recognizer.recognize_google(audio).lower()

            # If the activation word is "jarvis", continue to listen for command
            if word == "jarvis":
                speak("YES")
                with sr.Microphone() as source:
                    print("Jarvis active. Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        # Handle cases where speech was not recognized
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        
        # Handle API request errors
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        
        # Catch any other exceptions
        except Exception as e:
            print(f"Error: {e}")
