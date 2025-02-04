import os
import pyttsx3
import datetime
import speech_recognition as sr
import pywhatkit as kit
import wikipedia
import requests
import time
import pyautogui
from PIL import Image
import random
import speedtest

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"Jarvis: {text}")  # Debug output
    engine.say(text)
    engine.runAndWait()

# Greet the user
def greet_me():
    """Greets the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning Shashank! How may I help you?")
    elif 12 <= hour < 18:
        speak("Good Afternoon Shashank! How may I help you?")
    else:
        speak("Good Evening Shashank! How may I help you?")

# Listen to user's voice command
def listen():
    """Listens to the user's voice command and returns it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")  # Debug output
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech service.")
        except Exception as e:
            speak(f"An error occurred: {e}")
        return ""

# Search the web
def search_web(query):
    """Searches Google, YouTube, or Wikipedia based on the query."""
    if 'google' in query:
        kit.search(query.replace('google', ''))
    elif 'youtube' in query:
        kit.playonyt(query.replace('youtube', ''))
    elif 'wiki' in query:
        try:
            result = wikipedia.summary(query.replace('wiki', ''), sentences=2)
            speak(result)
        except wikipedia.DisambiguationError:
            speak("Your query is ambiguous. Please be more specific.")

# Get weather temperature
def get_temperature(city):
    """Fetches and announces the current temperature of a city."""
    api_key = "890e2a762782299e089c5402cd872238"  # Replace with your API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data['cod'] == 200:
            temperature = data['main']['temp']
            speak(f"The current temperature in {city} is {temperature} degrees Celsius.")
        else:
            speak("Sorry, I couldn't get the temperature information.")
    except requests.RequestException:
        speak("Network error. Please check your connection.")

# Get the current time
def get_time():
    """Announces the current time."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}.")

# Open apps by voice command
def open_app(app_name):
    """Opens specified applications or websites."""
    apps = {
        'chrome': ('start chrome', "Opening Google Chrome"),
        'notepad': ('start notepad', "Opening Notepad"),
        'microsoft word': ('start winword', "Opening Microsoft Word"),
        'microsoft excel': ('start excel', "Opening Microsoft Excel"),
        'microsoft powerpoint': ('start powerpnt', "Opening Microsoft PowerPoint"),
        'youtube': ('start https://youtube.com', "Opening YouTube"),
        'gmail': ('start https://mail.google.com', "Opening Gmail"),
        'whatsapp': ('start https://web.whatsapp.com', "Opening WhatsApp"),
        'spotify': ('start spotify', "Opening Spotify"),
        'facebook': ('start https://www.facebook.com', "Opening Facebook"),
        'twitter': ('start https://www.twitter.com', "Opening Twitter"),
        'instagram': ('start https://www.instagram.com', "Opening Instagram"),
        'zoom': ('start zoom', "Opening Zoom"),
        'calculator': ('start calc', "Opening Calculator")
    }

    for key, (command, response) in apps.items():
        if key in app_name:
            os.system(command)
            speak(response)
            return
    speak(f"Sorry, I cannot open {app_name}.")

# Set an alarm
def set_alarm(time_str):
    """Sets an alarm for the specified time."""
    speak(f"Alarm set for {time_str}.")
    while True:
        if datetime.datetime.now().strftime("%H:%M") == time_str:
            os.system("start alarm_sound.mp3")  # Replace with actual alarm sound
            speak("Time to wake up!")
            break
        time.sleep(30)

# Take a screenshot
def screenshot():
    """Takes and displays a screenshot."""
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    img = Image.open(screenshot_path)
    img.show()
    speak("Screenshot taken and opened.")

# Check internet speed
def check_internet_speed():
    """Checks and announces internet speed."""
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    speak(f"Download speed is {download_speed:.2f} Mbps and upload speed is {upload_speed:.2f} Mbps.")

# Focus mode (minimize all windows)
def focus_mode():
    """Activates focus mode by minimizing all windows."""
    pyautogui.hotkey('win', 'd')
    speak("Focus mode activated.")

# Perform calculations
def calculate(command):
    """Evaluates mathematical expressions from user commands."""
    try:
        expression = command.replace("calculate", "").strip()
        result = eval(expression)
        speak(f"The result is {result}.")
    except Exception as e:
        speak(f"Sorry, there was an error with the calculation: {e}")

# Password protection
def password_protection():
    """Restricts access with a password."""
    password = "Shashank"
    user_input = input("Enter password: ")
    if user_input != password:
        speak("Access denied.")
        exit()
    speak("Access granted.")

# Main function
def main():
    """Main logic for the voice assistant."""
    greet_me()
    while True:
        print("Debug: Waiting for a command.")  # Debug output
        command = listen()
        print(f"Debug: Command received: {command}")  # Debug output
        if not command:
            continue
        if 'jarvis close' in command:
            speak("Goodbye Shashank!")
            break
        elif 'who is anya' in command:
            speak("Anya is Shashank's sister and his classmate. Would you like to know more about her?")
        elif 'tell me more about anya' in command:
            speak("Anya is a college student studying at Chandigarh University and completing her BCA degree. She lives in Saharanpur, Uttar Pradesh.")
        elif 'who is my wife' in command:
            speak("Your wife is sitting next to you right now and her name is Devganga.")
        elif 'internet speed' in command:
            check_internet_speed()
        elif 'time' in command:
            get_time()
        elif 'search' in command:
            search_web(command)
        elif 'temperature' in command:
            city = command.replace("temperature in", "").strip()
            get_temperature(city)
        elif 'open' in command:
            open_app(command)
        elif 'alarm' in command:
            time_str = command.replace("set alarm for", "").strip()
            set_alarm(time_str)
        elif 'focus' in command:
            focus_mode()
        elif 'screenshot' in command:
            screenshot()
        elif 'calculate' in command:
            calculate(command)

if __name__ == "__main__":
    password_protection()
    main()
