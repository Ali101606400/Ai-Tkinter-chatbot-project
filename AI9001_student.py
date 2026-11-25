import os
import random
import shutil
import subprocess
import threading
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from urllib.parse import quote

import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr

r = sr.Recognizer()

dataframe = {
    "hello": ["hello", "hey", "welcome to app"],
    "hey": ["hello", "hey", "welcome to app"],
    "hi": ["hello", "hey", "welcome to app"],
    "pc": ["hello", "hey", "welcome to app"],
    "bye": ["bye", "have a nice day", "goodbye"],
    "goodbye": ["bye", "have a nice day", "goodbye"],
}


def SpeakText(command):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(command)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Speech error: {e}")


def listen_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        text = r.recognize_google(audio)
        return text.lower()


def play_video(song):
    try:
        pywhatkit.playonyt(song)
    except Exception as e:
        print(f"Could not start video: {e}")


def open_chrome():
    chrome_path = shutil.which("chrome.exe") or shutil.which("chrome")
    if not chrome_path:
        install_directories = [
            os.environ.get("PROGRAMFILES"),
            os.environ.get("PROGRAMFILES(X86)"),
            os.environ.get("LOCALAPPDATA"),
        ]
        for directory in install_directories:
            if directory:
                possible_path = os.path.join(
                    directory, "Google", "Chrome", "Application", "chrome.exe"
                )
                if os.path.isfile(possible_path):
                    chrome_path = possible_path
                    break

    if not chrome_path:
        return "Google Chrome could not be found. Check that it is installed."

    try:
        subprocess.Popen([chrome_path, "https://www.google.com"])
        return "Opening Google Chrome"
    except OSError as error:
        return f"Could not open Google Chrome: {error}"


def textprocess(inp):
    if "time" in inp:
        t = time.localtime()
        return f"{t.tm_hour} hour and {t.tm_min} minute and {t.tm_sec} second"

    if "joke" in inp or "funny" in inp:
        try:
            return pyjokes.get_joke()
        except Exception:
            jokes_fallback = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why do Java developers wear glasses? Because they don't C sharp!",
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
            ]
            return random.choice(jokes_fallback)
    if "search" in inp or "google" in inp:
        query = inp.replace("search", "").replace("google", "").strip()
        if not query:
            question = "What would you like me to search for?"
            print("Bot:", question)
            SpeakText(question)

            try:
                print("Listening for search query...")
                query = listen_command()
                print("You said:", query)
            except Exception:
                return "I couldn't hear the search query."
        webbrowser.open(f"https://www.google.com/search?q={quote(query)}")
        return f"Searching Google for {query}"
    
    if "google" in inp or "chrome" in inp:
        return open_chrome()

    if "youtube" in inp:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube for you!"

    if "gmail" in inp:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail for you!"
    if "github" in inp:
        webbrowser.open("https://github.com")
        return "Opening GitHub for you!"
    if "wikipedia" in inp:
        topic = inp.replace("wikipedia", "").strip()
        topic = " ".join(
            word for word in topic.split()
            if word not in {"open", "search", "for", "about"}
        )
        if topic:
            webbrowser.open(f'https://en.wikipedia.org/wiki/{quote(topic.replace(" ", "_"))}')
            return f"Opening Wikipedia for {topic}"
        webbrowser.open("https://en.wikipedia.org")
        return "Opening Wikipedia"

    if "play" in inp:
        song = inp.replace("play", "").strip()
        if not song:
            question = "What would you like me to play?"
            print("Bot:", question)
            SpeakText(question)

            try:
                print("Listening for song/video name...")
                song = listen_command()
                print("You said:", song)
            except Exception:
                return "I couldn't hear the song name."

        song_to_play = song
        playback_thread = threading.Thread(
            target=play_video,
            args=(song_to_play,),
        )
        playback_thread.start()
        return f"Starting {song_to_play}"

    if "calculator" in inp:
        os.system("calc")
        return "Opening Calculator"

    words = inp.split()
    for word in words:
        if word in dataframe:
            return random.choice(dataframe[word])

    return "I did not understand that."


exit_words = ["bye", "goodbye", "exit", "quit", 'stop', 'turn off', 'end', 'close', 'power off', 'shutdown', 'off']


class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice & Text Assistant")
        self.root.geometry("920x760")
        self.root.minsize(780, 620)
        self.root.configure(bg="#14002b")

        style = ttk.Style(root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("Title.TLabel", background="#14002b", foreground="#fff200")
        style.configure("Subtitle.TLabel", background="#14002b", foreground="#58f7ff")
        style.configure("Status.TLabel", background="#14002b", foreground="#ffffff")
        style.configure(
            "TEntry",
            fieldbackground="#ffffff",
            foreground="#28104e",
            padding=8,
        )
        style.configure(
            "TLabelframe",
            background="#2a0752",
            foreground="#ffffff",
            borderwidth=2,
            relief="raised",
        )
        style.configure(
            "TLabelframe.Label",
            background="#2a0752",
            foreground="#ff70d2",
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "Pink.TButton",
            background="#ff2da6",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
        )
        style.map("Pink.TButton", background=[("active", "#ff74c7"), ("pressed", "#b90072")])
        style.configure(
            "Blue.TButton",
            background="#00b8ff",
            foreground="#13003d",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
        )
        style.map("Blue.TButton", background=[("active", "#58f7ff"), ("pressed", "#007aaa")])
        style.configure(
            "Green.TButton",
            background="#43e97b",
            foreground="#082818",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
        )
        style.map("Green.TButton", background=[("active", "#98ffbd"), ("pressed", "#1ba85d")])
        style.configure(
            "Yellow.TButton",
            background="#fff200",
            foreground="#321500",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
        )
        style.map("Yellow.TButton", background=[("active", "#fff68a"), ("pressed", "#c7aa00")])

        self.create_distracting_background()

        ttk.Label(
            root,
            text="AI Assistant",
            style="Title.TLabel",
            font=("Segoe UI", 28, "bold"),
        ).pack(pady=(14, 2))
        ttk.Label(
            root,
            text="TYPE IT  |  CLICK IT  |  SAY IT",
            style="Subtitle.TLabel",
            font=("Segoe UI", 10),
        ).pack(pady=(0, 10))

        input_frame = tk.Frame(root, bg="#14002b")
        input_frame.pack(fill="x", padx=28)

        self.command_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.command_entry.bind("<Return>", lambda event: self.send_text())

        ttk.Button(input_frame, text="SEND!", style="Pink.TButton", command=self.send_text, width=10).pack(
            side="left"
        )

        quick_frame = ttk.LabelFrame(root, text="Quick buttons")
        quick_frame.pack(fill="x", padx=28, pady=10)

        quick_commands = [
            ("TIME", "what is the time", "Blue"),
            ("JOKE", "tell me a joke", "Yellow"),
            ("CHROME", "open chrome", "Pink"),
            ("GOOGLE", "google artificial intelligence", "Blue"),
            ("YOUTUBE", "open youtube", "Pink"),
            ("GMAIL", "open gmail", "Green"),
            ("GITHUB", "open github", "Blue"),
            ("WIKI", "open wikipedia", "Yellow"),
            ("CALCULATOR", "open calculator", "Green"),
            ("SEARCH", "search computer science", "Pink"),
            ("PLAY MUSIC", "play happy music", "Yellow"),
            ("HELLO", "hello", "Green"),
            ("BYE", "goodbye", "Pink"),
        ]

        for index, (label, command, color) in enumerate(quick_commands):
            row, column = divmod(index, 5)
            button = ttk.Button(
                quick_frame,
                text=label,
                style=f"{color}.TButton",
                command=lambda value=command: self.process_command(value),
                width=16,
            )
            button.grid(row=row, column=column, padx=7, pady=7)

        for column in range(5):
            quick_frame.columnconfigure(column, weight=1)

        voice_frame = tk.Frame(root, bg="#14002b")
        voice_frame.pack(fill="x", padx=28)

        self.microphone_button = ttk.Button(
            voice_frame,
            text="MICROPHONE",
            style="Pink.TButton",
            command=self.listen_with_microphone,
        )
        self.microphone_button.pack(side="left")

        ttk.Button(
            voice_frame,
            text="SPEAK",
            style="Yellow.TButton",
            command=self.speak_last_response,
        ).pack(side="left", padx=8)

        ttk.Button(
            voice_frame,
            text="CLEAR",
            style="Blue.TButton",
            command=self.clear_chat,
        ).pack(side="left")

        output_frame = ttk.LabelFrame(root, text="Conversation")
        output_frame.pack(fill="both", expand=True, padx=28, pady=(10, 12))

        self.output = scrolledtext.ScrolledText(
            output_frame,
            height=12,
            font=("Segoe UI", 11),
            wrap="word",
            state="disabled",
            background="#fffaf0",
            foreground="#24104f",
            insertbackground="#24104f",
        )
        self.output.pack(fill="both", expand=True, padx=8, pady=8)

        self.status = ttk.Label(root, text="READY!", style="Status.TLabel", anchor="w")
        self.status.pack(fill="x", padx=28, pady=(0, 10))

        self.last_response = ""
        self.add_message("Assistant", "Hello! What would you like me to do?")

    def create_distracting_background(self):
        self.background = tk.Canvas(
            self.root,
            width=920,
            height=760,
            highlightthickness=0,
            bg="#14002b",
        )
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)

        gradient_colors = ["#14002b", "#24005a", "#400084", "#67008c"]
        for index, color in enumerate(gradient_colors):
            self.background.create_rectangle(
                0,
                index * 190,
                920,
                (index + 1) * 190,
                fill=color,
                outline=color,
            )

        for offset in range(-600, 1000, 70):
            self.background.create_polygon(
                offset,
                0,
                offset + 28,
                0,
                offset + 220,
                760,
                offset + 192,
                760,
                fill="#ff2da6",
                outline="",
                stipple="gray25",
            )

        self.moving_shapes = []
        shape_colors = ["#fff200", "#00eaff", "#ff54ba", "#43e97b", "#ffffff"]
        for index in range(38):
            x = random.randint(10, 910)
            y = random.randint(10, 750)
            size = random.randint(5, 18)
            if index % 4 == 0:
                shape = self.background.create_rectangle(
                    x,
                    y,
                    x + size,
                    y + size,
                    fill=random.choice(shape_colors),
                    outline="",
                )
            elif index % 4 == 1:
                shape = self.background.create_oval(
                    x,
                    y,
                    x + size,
                    y + size,
                    fill=random.choice(shape_colors),
                    outline="",
                )
            else:
                shape = self.background.create_text(
                    x,
                    y,
                    text=random.choice(["*", "+", "?", "!", "AI"]),
                    fill=random.choice(shape_colors),
                    font=("Segoe UI", random.randint(10, 18), "bold"),
                )
            self.moving_shapes.append(
                [
                    shape,
                    random.choice([-3, -2, -1, 1, 2, 3]),
                    random.choice([-3, -2, -1, 1, 2, 3]),
                ]
            )

        self.animate_background()

    def animate_background(self):
        canvas_width = self.background.winfo_width()
        canvas_height = self.background.winfo_height()
        if canvas_width < 2:
            canvas_width = 920
        if canvas_height < 2:
            canvas_height = 760

        for shape, dx, dy in self.moving_shapes:
            self.background.move(shape, dx, dy)
            x1, y1, x2, y2 = self.background.bbox(shape)
            if x2 >= canvas_width or x1 <= 0:
                dx = -dx
                shape_info = next(info for info in self.moving_shapes if info[0] == shape)
                shape_info[1] = dx
            if y2 >= canvas_height or y1 <= 0:
                dy = -dy
                shape_info = next(info for info in self.moving_shapes if info[0] == shape)
                shape_info[2] = dy

        self.root.after(55, self.animate_background)

    def add_message(self, speaker, message):
        self.output.configure(state="normal")
        self.output.insert("end", f"{speaker}: {message}\n\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def set_status(self, message):
        self.status.configure(text=message)

    def send_text(self):
        command = self.command_entry.get().strip()
        if not command:
            messagebox.showinfo("Empty command", "Please type a request first.")
            return
        self.command_entry.delete(0, "end")
        self.process_command(command)

    def process_command(self, command):
        command = command.lower().strip()
        self.add_message("You", command)
        self.set_status("Working...")

        worker = threading.Thread(
            target=self.run_command_worker,
            args=(command,),
            daemon=True,
        )
        worker.start()

    def run_command_worker(self, command):
        response = textprocess(command)
        self.root.after(0, self.show_response, command, response)

    def show_response(self, command, response):
        self.last_response = response
        self.add_message("Assistant", response)
        self.set_status("Ready")

        if any(word in command for word in exit_words):
            self.set_status("Assistant closed")

    def listen_with_microphone(self):
        self.microphone_button.configure(state="disabled")
        self.set_status("Listening...")
        worker = threading.Thread(target=self.listen_worker, daemon=True)
        worker.start()

    def listen_worker(self):
        try:
            text = listen_command()
            self.root.after(0, self.process_voice_command, text)
        except sr.WaitTimeoutError:
            self.root.after(0, self.voice_error, "Listening timed out.")
        except sr.UnknownValueError:
            self.root.after(0, self.voice_error, "I could not understand the audio.")
        except sr.RequestError as error:
            self.root.after(0, self.voice_error, f"Speech service error: {error}")
        except Exception as error:
            self.root.after(0, self.voice_error, f"Microphone error: {error}")

    def process_voice_command(self, text):
        self.microphone_button.configure(state="normal")
        self.add_message("You (voice)", text)
        self.process_command(text)

    def voice_error(self, message):
        self.microphone_button.configure(state="normal")
        self.add_message("Assistant", message)
        self.set_status("Ready")

    def speak_last_response(self):
        if not self.last_response:
            messagebox.showinfo("No response", "Send or say a command first.")
            return
        threading.Thread(
            target=SpeakText,
            args=(self.last_response,),
            daemon=True,
        ).start()
        self.set_status("Speaking...")

    def clear_chat(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self.last_response = ""
        self.set_status("Ready")


def main():
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
