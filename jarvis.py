import speech_recognition as sr
import webbrowser
import datetime
import asyncio
import edge_tts
import pygame
import os
import tempfile
import threading
import requests
import ollama
import subprocess
import json
from openai import OpenAI

# ================= OPENROUTER ================= #

client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key="YOUR_API_KEY"

)

# ================= AUDIO ================= #

pygame.mixer.init()

stop_speaking = False

# ================= MEMORY ================= #

def load_memory():

    try:

        with open("memory.json", "r") as file:

            return json.load(file)

    except:

        return {}

def save_memory(memory):

    with open("memory.json", "w") as file:

        json.dump(memory, file)

memory = load_memory()

# ================= CHAT HISTORY ================= #

chat_history = []

# ================= INTERNET ================= #

def internet_available():

    try:

        requests.get("https://www.google.com", timeout=3)

        return True

    except:

        return False

# ================= SPEAK ================= #

async def speak_async(text):

    global stop_speaking

    stop_speaking = False

    communicate = edge_tts.Communicate(

        text=text,

        voice="en-US-GuyNeural",

        rate="+20%"

    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:

        temp_filename = tmp_file.name

    await communicate.save(temp_filename)

    pygame.mixer.music.load(temp_filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        if stop_speaking:

            pygame.mixer.music.stop()

            break

        await asyncio.sleep(0.03)

    pygame.mixer.music.unload()

    os.remove(temp_filename)

def speak(text):

    print("\nJarvis:", text)

    asyncio.run(speak_async(text))

# ================= TAKE COMMAND ================= #

def take_command():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.3)

        recognizer.pause_threshold = 0.8

        recognizer.non_speaking_duration = 0.5

        audio = recognizer.listen(source)

    try:

        print("Recognizing...")

        command = recognizer.recognize_google(audio)

        print("You:", command)

        return command.lower()

    except:

        return ""

# ================= ONLINE AI ================= #

def ask_online_ai(question):

    global chat_history

    chat_history.append({

        "role": "user",

        "content": question

    })

    completion = client.chat.completions.create(

        model="openai/gpt-3.5-turbo",

        messages=[

            {

                "role": "system",

                "content": (
                    """
                 You are Jarvis, a smart futuristic AI assistant.

                 Give detailed, intelligent and clean answers.

                 Explain properly in points when user asks.

                 Be conversational and natural.
                  """

                    
                )

            }

        ] + chat_history,

        max_tokens=500,

    )

    answer = completion.choices[0].message.content

    chat_history.append({

        "role": "assistant",

        "content": answer

    })

    if len(chat_history) > 10:

        chat_history = chat_history[-10:]

    return answer

# ================= OFFLINE AI ================= #

def ask_offline_ai(question):

    global chat_history

    chat_history.append({

        "role": "user",

        "content": question

    })

    response = ollama.chat(

        model='tinyllama',

        messages=[

            {

                'role': 'system',

                'content': (
                    'You are Jarvis, an offline AI assistant. '
                    'Reply shortly and clearly.'
                )

            }

        ] + chat_history,

        options={

            'num_predict': 40,

            'temperature': 0.7

        }

    )

    answer = response['message']['content']

    chat_history.append({

        "role": "assistant",

        "content": answer

    })

    if len(chat_history) > 10:

        chat_history = chat_history[-10:]

    return answer

# ================= MAIN AI ================= #

def ask_ai(question):

    # OPEN YOUTUBE
    if "open youtube" in question:

        webbrowser.open("https://youtube.com")

        return "Opening YouTube Sir."

    # OPEN GOOGLE
    elif "open google" in question:

        webbrowser.open("https://google.com")

        return "Opening Google Sir."

    # OPEN CHATGPT
    elif "open chat gpt" in question:

        webbrowser.open("https://chatgpt.com")

        return "Opening ChatGPT Sir."

    # OPEN CHROME
    elif "open chrome" in question:

        os.startfile(
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )

        return "Opening Chrome Sir."

    # OPEN NOTEPAD
    elif "open notepad" in question:

        subprocess.Popen("notepad.exe")

        return "Opening Notepad Sir."

    # OPEN CALCULATOR
    elif "open calculator" in question:

        subprocess.Popen("calc.exe")

        return "Opening Calculator Sir."

    # OPEN VS CODE
    elif "open vscode" in question or "open vs code" in question:

        os.startfile(
            "C:\\Users\\suraj\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        )

        return "Opening Visual Studio Code Sir."

    # TIME
    elif "time" in question:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"The time is {current_time}"

    # SAVE NAME
    elif "my name is" in question:

        name = question.replace("my name is", "").strip()

        memory["name"] = name

        save_memory(memory)

        return f"I will remember your name {name}"

    # RECALL NAME
    elif "what is my name" in question:

        if "name" in memory:

            return f"Your name is {memory['name']}"

        else:

            return "I do not know your name yet"

    # ONLINE MODE
    if internet_available():

        print("\n[Using OpenRouter AI]")

        try:

            return ask_online_ai(question)

        except:

            print("\n[OpenRouter Failed -> Offline AI]")

            return ask_offline_ai(question)

    # OFFLINE MODE
    else:

        print("\n[Using Offline AI]")

        return ask_offline_ai(question)

# ================= STOP LISTENER ================= #

def stop_listener():

    global stop_speaking

    recognizer = sr.Recognizer()

    while True:

        with sr.Microphone() as source:

            audio = recognizer.listen(source, phrase_time_limit=2)

        try:

            command = recognizer.recognize_google(audio).lower()

            if "stop" in command:

                stop_speaking = True

                pygame.mixer.music.stop()

                print("\nSpeech Stopped")

        except:
            pass

threading.Thread(target=stop_listener, daemon=True).start()

# ================= MAIN ================= #

if __name__ == "__main__":

    speak("Hello Sir. I am Jarvis. How can I help you?")

    while True:

        command = take_command()

        if command == "":
            continue

        if "exit" in command:

            speak("Goodbye Sir")

            break

        answer = ask_ai(command)

        print("\nAI:", answer)

        speak(answer)