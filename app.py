import customtkinter as ctk
import threading
import jarvis

from jarvis import take_command, ask_ai, speak

# ================= APP ================= #

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.state("zoomed")

app.title("JARVIS AI")

# ================= COLORS ================= #

BG = "#050816"
SIDEBAR = "#081120"
CARD = "#0b1324"
CYAN = "#00e5ff"

app.configure(fg_color=BG)

# ================= SIDEBAR ================= #

sidebar = ctk.CTkFrame(

    app,

    width=300,

    fg_color=SIDEBAR,

    corner_radius=0

)

sidebar.pack(side="left", fill="y")

# ================= SHIELD ================= #

shield_frame = ctk.CTkFrame(

    sidebar,

    width=240,

    height=240,

    fg_color="transparent"

)

shield_frame.pack(pady=(20,10))

shield = ctk.CTkLabel(

    shield_frame,

    text="⬢",

    font=("Arial", 150),

    text_color=CYAN

)

shield.place(relx=0.5, rely=0.5, anchor="center")

shield_core = ctk.CTkLabel(

    shield_frame,

    text="◉",

    font=("Arial", 85),

    text_color="white"

)

shield_core.place(relx=0.5, rely=0.5, anchor="center")

# ================= ANIMATION ================= #

glow = 0

def animate_core():

    global glow

    glow += 1

    colors = [

        "#00e5ff",

        "#00ffff",

        "#66ffff",

        "#00ccff"

    ]

    shield_core.configure(

        text_color=colors[glow % len(colors)]

    )

    app.after(500, animate_core)

animate_core()

# ================= LOGO ================= #

logo = ctk.CTkLabel(

    sidebar,

    text="JARVIS",

    font=("Arial", 42, "bold"),

    text_color=CYAN

)

logo.pack(pady=(0,25))

# ================= MENU ================= #

menu_items = [

    "💬 New Chat",

    "🤖 AI Assistant",

    "📁 Files",

    "🖥 System",

    "⚙ Settings"

]

for item in menu_items:

    btn = ctk.CTkButton(

        sidebar,

        text=item,

        width=240,

        height=55,

        corner_radius=18,

        fg_color="#0d1b2a",

        hover_color="#123456",

        font=("Arial", 17)

    )

    btn.pack(pady=8)

# ================= USER ================= #

user_label = ctk.CTkLabel(

    sidebar,

    text="👤 User\n🟢 Online",

    font=("Arial", 16),

    justify="left",

    text_color="white"

)

user_label.pack(side="bottom", pady=25)

# ================= MAIN FRAME ================= #

main_frame = ctk.CTkFrame(

    app,

    fg_color=BG

)

main_frame.pack(

    side="right",

    fill="both",

    expand=True

)

# ================= HEADER ================= #

title = ctk.CTkLabel(

    main_frame,

    text="JARVIS AI",

    font=("Arial", 48, "bold"),

    text_color="white"

)

title.pack(pady=(20,0))

subtitle = ctk.CTkLabel(

    main_frame,

    text="Your Intelligent Assistant",

    font=("Arial", 20),

    text_color="#8a8a8a"

)

subtitle.pack(pady=(0,10))

# ================= CHAT CONTAINER ================= #

chat_container = ctk.CTkFrame(

    main_frame,

    fg_color="transparent"

)

chat_container.pack(

    fill="both",

    expand=True,

    padx=20,

    pady=10

)

# ================= CHAT FRAME ================= #

chat_frame = ctk.CTkScrollableFrame(

    chat_container,

    fg_color=CARD,

    corner_radius=25

)

chat_frame.pack(

    fill="both",

    expand=True

)

# ================= STATUS ================= #

status = ctk.CTkLabel(

    main_frame,

    text="● ONLINE",

    font=("Arial", 18, "bold"),

    text_color="#00ff88"

)

status.pack(pady=5)

# ================= ADD MESSAGE ================= #

def add_message(sender, message, is_user=False):

    bubble_color = "#00e5ff" if is_user else "#111827"

    text_color = "black" if is_user else "white"

    anchor = "e" if is_user else "w"

    bubble = ctk.CTkLabel(

        chat_frame,

        text=f"{sender}\n\n{message}",

        fg_color=bubble_color,

        text_color=text_color,

        corner_radius=20,

        justify="left",

        wraplength=650,

        font=("Arial", 18),

        padx=20,

        pady=15

    )

    bubble.pack(

        anchor=anchor,

        pady=10,

        padx=15

    )

# ================= DEFAULT MESSAGE ================= #

add_message(

    "🤖 JARVIS",

    "Hello Sir 👋\nI am Jarvis. How can I help you today?"

)

# ================= PROCESS ================= #

def process_text(user_text, is_voice=False):

    jarvis.voice_mode = is_voice

    # USER MESSAGE
    add_message(

        "👤 YOU",

        user_text,

        True

    )

    status.configure(text="🧠 Thinking...")

    # AI RESPONSE
    answer = ask_ai(user_text)

    add_message(

        "🤖 JARVIS",

        answer

    )

    # VOICE
    if is_voice:

        speak(answer)

    status.configure(text="● ONLINE")

# ================= SEND ================= #

def send_message():

    text = entry.get()

    if text.strip() != "":

        entry.delete(0, "end")

        threading.Thread(

            target=process_text,

            args=(text, False)

        ).start()

# ================= VOICE ================= #

def mic_click():

    status.configure(text="🎤 Listening...")

    def assistant_loop():

        while True:

            wake = take_command()

            if wake == "":
                continue

            if "jarvis" in wake:

                speak("How can I assist you Sir?")

                while True:

                    command = take_command()

                    if command == "":
                        continue

                    if "exit" in command:

                        speak("Stopping assistant")

                        return

                    process_text(command, True)

    threading.Thread(

        target=assistant_loop,

        daemon=True

    ).start()

# ================= INPUT FRAME ================= #

bottom_frame = ctk.CTkFrame(

    main_frame,

    fg_color="transparent"

)

bottom_frame.pack(

    side="bottom",

    fill="x",

    padx=20,

    pady=15

)

# ================= MIC BUTTON ================= #

mic_button = ctk.CTkButton(

    bottom_frame,

    text="🎤",

    width=70,

    height=70,

    corner_radius=35,

    fg_color=CYAN,

    hover_color="#00b8d4",

    text_color="black",

    font=("Arial", 26),

    command=mic_click

)

mic_button.grid(row=0, column=0, padx=10)

# ================= ENTRY ================= #

entry = ctk.CTkEntry(

    bottom_frame,

    width=900,

    height=70,

    corner_radius=22,

    fg_color="#0f172a",

    border_color="#16324f",

    text_color="white",

    font=("Arial", 18),

    placeholder_text="Type your message..."

)

entry.grid(row=0, column=1, padx=10)

# ================= SEND BUTTON ================= #

send_button = ctk.CTkButton(

    bottom_frame,

    text="➤",

    width=70,

    height=70,

    corner_radius=35,

    fg_color=CYAN,

    hover_color="#00b8d4",

    text_color="black",

    font=("Arial", 26),

    command=send_message

)

send_button.grid(row=0, column=2, padx=10)

# ================= ENTER SEND ================= #

entry.bind(

    "<Return>",

    lambda event: send_message()

)

# ================= RUN ================= #

app.mainloop()