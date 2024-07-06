import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from gtts import gTTS
import os
import pyttsx3
import pygame
from PIL import Image, ImageTk
import tempfile
import uuid

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-To-Speech Application")
        self.root.geometry("700x700")

        # Set background color
        self.root.configure(bg="#E6E6FA")

        # Define styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Times New Roman", 14))
        self.style.configure("Play.TButton")
        self.style.map("Play.TButton")
        self.style.configure("Pause.TButton")
        self.style.map("Pause.TButton")
        self.style.configure("Resume.TButton")
        self.style.map("Resume.TButton")
        self.style.configure("Stop.TButton")
        self.style.map("Stop.TButton")
        self.style.configure("Replay.TButton")
        self.style.map("Replay.TButton")
        self.style.configure("Save.TButton")
        self.style.map("Save.TButton")

        # Load and display the logo at the top
        self.logo_image = Image.open("D:\intern\logo1.png")  # Replace with your logo path
        self.logo_image = self.logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(root, image=self.logo_photo, bg="#E6E6FA")
        self.logo_label.pack(pady=10)

        # Create a heading
        self.heading = tk.Label(root, text="Text-To-Speech Converter", font=("Times New Roman", 19), bg="#E6E6FA")
        self.heading.pack()

        # Create GUI components
        self.text_input_frame = ttk.Frame(root)
        self.text_input_frame.pack(pady=10, padx=10)
        self.text_input_field = tk.Text(self.text_input_frame, height=20, width=90)
        self.text_input_field.pack()

        self.language_frame = ttk.Frame(root)
        self.language_frame.pack()
        self.language_label = ttk.Label(self.language_frame, text="Language:", font=("Times New Roman", 13))
        self.language_label.pack(side=tk.LEFT)

        # Language dictionary for display names and corresponding language codes
        self.languages = {
            "English": "en",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Dutch": "nl",
            "Russian": "ru",
            "Japanese": "ja",
            "Chinese (Simplified)": "zh-CN",
            "Chinese (Traditional)": "zh-TW",
            "Korean": "ko",
            "Arabic": "ar",
            "Turkish": "tr",
            "Swedish": "sv",
            "Norwegian": "no",
            "Danish": "da",
            "Finnish": "fi"
        }

        self.language_var = tk.StringVar()
        self.language_var.set("English")  # default language

        # Create the OptionMenu with display names
        self.language_menu = ttk.OptionMenu(self.language_frame, self.language_var, "English", *self.languages.keys())
        self.language_menu.pack(side=tk.LEFT, padx=5)

        self.voice_frame = ttk.Frame(root)
        self.voice_frame.pack(pady=5, padx=10)
        self.voice_label = ttk.Label(self.voice_frame, text="Voice:", font=("Times New Roman", 13))
        self.voice_label.pack(side=tk.LEFT, padx=5)
        self.voice_var = tk.StringVar()
        self.voice_var.set("default")  # default voice
        self.voice_menu = ttk.OptionMenu(self.voice_frame, self.voice_var, "Default", "Default", "Male", "Female")
        self.voice_menu.pack(side=tk.LEFT, padx=5)

        self.slider_frame = ttk.Frame(root)
        self.slider_frame.pack(pady=10, padx=10)

        # Define custom styles for sliders
        self.style.configure("TScale", background="#E6E6FA")

        # Rate Slider
        self.rate_label = ttk.Label(self.slider_frame, text="Rate:", font=("Times New Roman", 13), foreground="black")
        self.rate_label.pack(side=tk.LEFT, padx=5)
        self.rate_slider = tk.Scale(self.slider_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, bg="white", fg="black", highlightbackground="#E6E6FA", troughcolor="white")
        self.rate_slider.pack(side=tk.LEFT, padx=5)
        self.rate_slider.set(1.0)

        # Pitch Slider
        self.pitch_label = ttk.Label(self.slider_frame, text="Pitch:", font=("Times New Roman", 13), foreground="black")
        self.pitch_label.pack(side=tk.LEFT, padx=5)
        self.pitch_slider = tk.Scale(self.slider_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, bg="white", fg="black", highlightbackground="#E6E6FA", troughcolor="white")
        self.pitch_slider.pack(side=tk.LEFT, padx=5)
        self.pitch_slider.set(1.0)

        # Volume Slider
        self.volume_label = ttk.Label(self.slider_frame, text="Volume:", font=("Times New Roman", 13),foreground="black")
        self.volume_label.pack(side=tk.LEFT, padx=5)
        self.volume_slider = tk.Scale(self.slider_frame, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, bg="white", fg="black", highlightbackground="#E6E6FA", troughcolor="white")
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        self.volume_slider.set(100)

        self.playback_controls_frame = ttk.Frame(root)
        self.playback_controls_frame.pack(pady=10)



# Load images
        play_image = Image.open("D:\\intern\\play.png").resize((20, 20), Image.LANCZOS)
        pause_image = Image.open("D:\\intern\\pause.png").resize((20, 20), Image.LANCZOS)
        resume_image = Image.open("D:\\intern\\resume.png").resize((20, 20), Image.LANCZOS)
        stop_image = Image.open("D:\\intern\\stop.png").resize((20, 20), Image.LANCZOS)
        replay_image = Image.open("D:\\intern\\replay-png-1.png").resize((20, 20), Image.LANCZOS)

        # Convert images to PhotoImage objects
        play_photo = ImageTk.PhotoImage(play_image)
        pause_photo = ImageTk.PhotoImage(pause_image)
        resume_photo = ImageTk.PhotoImage(resume_image)
        stop_photo = ImageTk.PhotoImage(stop_image)
        replay_photo = ImageTk.PhotoImage(replay_image)

        # Create buttons with images
        self.play_button = ttk.Button(self.playback_controls_frame, text="Play", style="Play.TButton", command=self.play_speech, image=play_photo, compound=tk.LEFT)
        self.play_button.image = play_photo  # Keep a reference to avoid garbage collection
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = ttk.Button(self.playback_controls_frame, text="Pause", style="Pause.TButton", command=self.pause_speech, image=pause_photo, compound=tk.LEFT)
        self.pause_button.image = pause_photo  # Keep a reference to avoid garbage collection
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.resume_button = ttk.Button(self.playback_controls_frame, text="Resume", style="Resume.TButton", command=self.resume_speech, image=resume_photo, compound=tk.LEFT)
        self.resume_button.image = resume_photo  # Keep a reference to avoid garbage collection
        self.resume_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(self.playback_controls_frame, text="Stop", style="Stop.TButton", command=self.stop_speech, image=stop_photo, compound=tk.LEFT)
        self.stop_button.image = stop_photo  # Keep a reference to avoid garbage collection
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.replay_button = ttk.Button(self.playback_controls_frame, text="Replay", style="Replay.TButton", command=self.replay_speech, image=replay_photo, compound=tk.LEFT)
        self.replay_button.image = replay_photo  # Keep a reference to avoid garbage collection
        self.replay_button.pack(side=tk.LEFT, padx=10)


        # Save Button with a download icon
        self.save_frame = ttk.Frame(root)
        self.save_frame.pack(pady=10)
        self.download_image = Image.open("D:\intern\down (1).png")  # Replace with your download icon path
        self.download_image = self.download_image.resize((20, 20), Image.LANCZOS)
        self.download_photo = ImageTk.PhotoImage(self.download_image)
        self.save_button = ttk.Button(self.save_frame, text="Save as MP3", style="Save.TButton", command=self.save_speech, image=self.download_photo, compound=tk.LEFT)
        self.save_button.pack(pady=5)

        # Initialize playback state
        self.paused = False

    def get_language_code(self):
        return self.languages.get(self.language_var.get(), "en")

    def play_speech(self):
        try:
            text = self.text_input_field.get("1.0", "end-1c").strip()
            if not text:
                messagebox.showerror("Error", "Text field is empty. Please enter some text.")
                return

            language = self.get_language_code()
            print(f"Selected Language: {language}")
            voice = self.voice_var.get()
            rate = self.rate_slider.get()
            pitch = self.pitch_slider.get()
            volume = self.volume_slider.get()

            # Use a unique temporary file path for temp.mp3
            temp_file = os.path.join(tempfile.gettempdir(), f"temp_{uuid.uuid4()}.mp3")
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(temp_file)
            print(f"temp.mp3 saved successfully at {temp_file}")

            # Reinitialize pygame mixer to ensure it loads the new file
            pygame.mixer.quit()
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            print("temp.mp3 loaded successfully")
            pygame.mixer.music.play()
            print("Playing temp.mp3")
            
            # Reset pause state
            self.paused = False
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def pause_speech(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            print("Paused temp.mp3")

    def resume_speech(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            print("Resumed temp.mp3")

    def stop_speech(self):
        pygame.mixer.music.stop()
        self.paused = False
        print("Stopped temp.mp3")

    def replay_speech(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()
        self.paused = False
        print("Replayed temp.mp3")

    def save_speech(self):
        try:
            text = self.text_input_field.get("1.0", "end-1c").strip()
            if not text:
                messagebox.showerror("Error", "Text field is empty. Please enter some text.")
                return

            language = self.get_language_code()
            print(f"Selected Language: {language}")

            # Choose a file path for saving
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if file_path:
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(file_path)
                print(f"Text saved as MP3 at {file_path}")
                messagebox.showinfo("Saved", f"Text saved successfully as MP3 at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
