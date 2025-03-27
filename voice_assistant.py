import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit
import os
import pyjokes
import psutil  # For battery info
import requests  # For weather
import pyautogui  # For screenshots
import smtplib  # For emails
import time

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speed of speech
engine.setProperty("volume", 1.0)  # Volume level

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("Request Error from Google API")
        return ""

# Get current time
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

# Get current date
def get_date():
    today = datetime.date.today()
    return today.strftime("%B %d, %Y")

# Open applications
def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "command prompt": "cmd.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    }
    if app_name in apps:
        os.system(f"start {apps[app_name]}")
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I can't find {app_name}.")

# Get battery percentage
def battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    return f"Battery is at {percent} percent."

# Get weather info (Replace 'YOUR_API_KEY' with your OpenWeatherMap API key)
def get_weather(city="New York"):
    API_KEY = "74b9510e9efbcfdbddfc6487fe544422"  # Replace with your OpenWeatherMap API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"


    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            description = response["weather"][0]["description"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]

            weather_info = (
                f"The temperature in {city} is {temp}°C with {description}. "
                f"Humidity is {humidity}% and wind speed is {wind_speed} m/s."
            )
            return weather_info
        else:
            return "Sorry, I couldn't get the weather details."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# Take a screenshot
def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot().save(filename)
    return f"Screenshot saved as {filename}."

# Send email (Basic setup)
def send_email(to, subject, message):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to, email_message)
        server.close()
        return "Email has been sent."
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# Shutdown or restart system
def system_control(command):
    if "shutdown" in command:
        os.system("shutdown /s /t 5")
        return "Shutting down the system in 5 seconds."
    elif "restart" in command:
        os.system("shutdown /r /t 5")
        return "Restarting the system in 5 seconds."
    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting system to sleep."

# Main function
def run_assistant():
    speak("Hello! How can I assist you today?")
    
    while True:
        query = listen()

        if "time" in query:
            speak(f"The time is {get_time()}.")

        elif "date" in query:
            speak(f"Today is {get_date()}.")

        elif "open" in query:
            app_name = query.replace("open ", "")
            open_app(app_name)

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "")
            speak("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia, {result}")

        elif "search" in query:
            search_query = query.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Searching {search_query} on Google.")

        elif "play" in query:
            song = query.replace("play", "").strip()
            pywhatkit.playonyt(song)
            speak(f"Playing {song} on YouTube.")

        elif "joke" in query:
            speak(pyjokes.get_joke())

        elif "battery" in query or "power status" in query:
            speak(battery_status())

        elif "weather" in query:
            speak("Which city do you want the weather for?")
            city = listen()
            if city:
                weather_report = get_weather(city)
                speak(weather_report)
            else:
                speak("I didn't get the city name. Please try again.")

        elif "screenshot" in query:
            speak("Taking a screenshot.")
            speak(take_screenshot())

        elif "email" in query:
            speak("Who should I send the email to?")
            recipient = listen()
            speak("What is the subject?")
            subject = listen()
            speak("What should I say?")
            body = listen()
            speak(send_email(recipient, subject, body))

        elif "shutdown" in query or "restart" in query or "sleep" in query:
            speak(system_control(query))
            break

        elif "exit" in query or "stop" in query:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("I didn't understand. Can you repeat that?")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
