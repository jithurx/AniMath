import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
import google.generativeai as genai
import subprocess
import os
import threading
import time
from PIL import Image, ImageTk
import glob
import json

class ApiKeyDialog(simpledialog.Dialog):
    """Dialog for entering the Google Gemini API key"""
    
    def __init__(self, parent, title, initial_value=""):
        self.initial_value = initial_value
        super().__init__(parent, title)
    
    def body(self, master):
        ttk.Label(master, text="Enter your Google Gemini API Key:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.api_key_entry = ttk.Entry(master, width=50, show="*")
        self.api_key_entry.grid(row=1, column=0, pady=(0, 10))
        self.api_key_entry.insert(0, self.initial_value)
        
        self.show_key_var = tk.BooleanVar(value=False)
        self.show_key_check = ttk.Checkbutton(
            master, 
            text="Show API Key", 
            variable=self.show_key_var,
            command=self.toggle_show_key
        )
        self.show_key_check.grid(row=2, column=0, sticky="w")
        
        instructions = (
            "You need a Google Gemini API key to use this application.\n"
            "If you don't have one, you can get it from the Google AI Studio."
        )
        instruction_label = ttk.Label(master, text=instructions, wraplength=300)
        instruction_label.grid(row=3, column=0, pady=10)
        
        return self.api_key_entry  # Initial focus
    
    def toggle_show_key(self):
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
    
    def apply(self):
        self.result = self.api_key_entry.get()


class ManimUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manim Math Visualization Generator")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f0f0")
        
        self.status = "Ready"
        self.current_step = 0
        self.total_steps = 4
        self.api_key = None
        
        # Load or request API key before setting up UI
        self.load_or_request_api_key()
        
        self.setup_ui()
        
    def load_or_request_api_key(self):
        """Load API key from file or request from user if not found"""
        # Create directory if it doesn't exist
        os.makedirs("api", exist_ok=True)
        
        # Check if key file exists
        if os.path.exists("api/key.txt"):
            try:
                with open("api/key.txt", "r") as f:
                    self.api_key = f.read().strip()
                    if self.api_key:
                        genai.configure(api_key=self.api_key)
                        return
            except Exception as e:
                print(f"Error reading API key: {str(e)}")
        
        # If we got here, we need to request a key
        self.request_api_key()
    
    def request_api_key(self):
        """Show dialog to request API key from user"""
        # Get current key for display (if any)
        current_key = self.api_key if self.api_key else ""
        
        # Show dialog
        dialog = ApiKeyDialog(self.root, "API Key Required", current_key)
        new_key = dialog.result
        
        if new_key:
            # Save the key
            with open("api/key.txt", "w") as f:
                f.write(new_key)
            
            self.api_key = new_key
            genai.configure(api_key=self.api_key)
        else:
            # If no key provided, exit application
            if not self.api_key:  # Only exit if no previous key
                messagebox.showerror("API Key Required", "An API key is required to use this application.")
                self.root.destroy()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title bar with settings button
        title_bar = ttk.Frame(main_frame)
        title_bar.pack(fill=tk.X)
        
        # Title
        title_label = ttk.Label(
            title_bar, 
            text="Manim Math Visualization Generator", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Settings button
        settings_button = ttk.Button(
            title_bar,
            text="⚙️ Settings",
            command=self.show_settings
        )
        settings_button.pack(side=tk.RIGHT, pady=10)
        
        # Prompt input section
        prompt_frame = ttk.LabelFrame(main_frame, text="Enter Your Math Concept", padding="10")
        prompt_frame.pack(fill=tk.X, pady=10)
        
        self.prompt_input = scrolledtext.ScrolledText(
            prompt_frame, 
            height=5, 
            width=80, 
            font=("Arial", 11),
            wrap=tk.WORD
        )
        self.prompt_input.pack(fill=tk.X, pady=5)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Status indicator
        status_frame = ttk.Frame(controls_frame)
        status_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        
        self.status_indicator = ttk.Label(
            status_frame, 
            text="Ready", 
            background="#4CAF50", 
            foreground="white",
            padding="5 2",
            relief="flat",
            anchor="center",
            width=15
        )
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        self.generate_button = ttk.Button(
            controls_frame, 
            text="Generate Visualization", 
            command=self.start_generation_process
        )
        self.generate_button.pack(side=tk.RIGHT, padx=10)
        
        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress = ttk.Progressbar(
            progress_frame, 
            orient=tk.HORIZONTAL, 
            length=100, 
            mode='determinate'
        )
        self.progress.pack(fill=tk.X)
        
        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Generated Manim Code", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.code_output = scrolledtext.ScrolledText(
            output_frame, 
            height=10, 
            width=80, 
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.code_output.pack(fill=tk.BOTH, expand=True)
        
        # Video display frame
        self.video_frame = ttk.LabelFrame(main_frame, text="Generated Visualization", padding="10")
        self.video_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = ttk.Label(main_frame, text="Powered by Manim and Google Gemini", font=("Arial", 8))
        footer.pack(pady=5)
    
    def show_settings(self):
        """Show settings dialog with API key management option"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        settings_frame = ttk.Frame(settings_window, padding="20")
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # API Key section
        api_key_frame = ttk.LabelFrame(settings_frame, text="API Key Management", padding="10")
        api_key_frame.pack(fill=tk.X, pady=10)
        
        # Show masked API key
        masked_key = "•" * 25 + self.api_key[-5:] if self.api_key and len(self.api_key) > 5 else "Not set"
        ttk.Label(api_key_frame, text="Current API Key:").pack(anchor="w")
        ttk.Label(api_key_frame, text=masked_key).pack(anchor="w", pady=(0, 10))
        
        # Button to change API key
        change_key_btn = ttk.Button(
            api_key_frame,
            text="Change API Key",
            command=lambda: self.change_api_key(settings_window)
        )
        change_key_btn.pack(pady=5)
    
    def change_api_key(self, parent_window=None):
        """Show dialog to change API key"""
        dialog = ApiKeyDialog(parent_window or self.root, "Change API Key", self.api_key or "")
        new_key = dialog.result
        
        if new_key:
            # Save the key
            with open("api/key.txt", "w") as f:
                f.write(new_key)
            
            self.api_key = new_key
            genai.configure(api_key=self.api_key)
            
            if parent_window:
                parent_window.destroy()
            
            messagebox.showinfo("Success", "API key updated successfully!")
    
    def update_status(self, status, progress=None):
        self.status = status
        
        status_colors = {
            "Ready": "#4CAF50",  # Green
            "Processing": "#2196F3",  # Blue
            "Complete": "#4CAF50",  # Green
            "Error": "#F44336",  # Red
        }
        
        color = status_colors.get(status.split()[0], "#2196F3")
        
        self.status_indicator.config(text=status, background=color)
        self.progress_label.config(text=status)
        
        if progress is not None:
            self.progress["value"] = progress
            
        self.root.update_idletasks()
    
    def start_generation_process(self):
        # Check if API key is available
        if not self.api_key:
            self.request_api_key()
            if not self.api_key:  # User canceled
                return
        
        # Disable button during processing
        self.generate_button.config(state="disabled")
        self.progress["value"] = 0
        
        # Clear previous outputs
        self.code_output.delete(1.0, tk.END)
        self.video_label.config(image="")
        
        # Get user input
        user_input = self.prompt_input.get(1.0, tk.END).strip()
        
        if not user_input:
            self.update_status("Error: No input provided", 0)
            self.generate_button.config(state="normal")
            return
        
        # Start generation in a separate thread
        threading.Thread(target=self.generate_visualization, args=(user_input,), daemon=True).start()
    
    def generate_visualization(self, user_input):
        try:
            # Step 1: Refine prompt
            self.update_status("Processing: Refining prompt", 25)
            refined_prompt = self.refine_prompt(user_input)
            
            if not refined_prompt:
                self.update_status("Error: Failed to refine prompt", 0)
                self.generate_button.config(state="normal")
                return
            
            # Step 2: Generate Manim code
            self.update_status("Processing: Generating Manim code", 50)
            manim_code = self.generate_manim_code(refined_prompt)
            
            if not manim_code:
                self.update_status("Error: Failed to generate code", 0)
                self.generate_button.config(state="normal")
                return
            
            # Clean and display code
            clean_code = self.clean_text(manim_code)
            self.code_output.insert(tk.END, clean_code)
            
            # Step 3: Save script
            self.update_status("Processing: Saving Manim script", 75)
            self.save_manim_script(clean_code)
            
            # Step 4: Run Manim script
            self.update_status("Processing: Rendering visualization", 90)
            success = self.run_manim_script()
            
            if success:
                self.update_status("Complete: Visualization generated", 100)
                self.display_video()
            else:
                self.update_status("Error: Failed to render visualization", 0)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", 0)
        
        # Re-enable button
        self.root.after(0, lambda: self.generate_button.config(state="normal"))
    
    def refine_prompt(self, user_input):
        """Send user input to Gemini Flash to create a better prompt for Manim code generation."""
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = (
            "You are an AI that helps generate precise prompts for AI code generation. "
            "Given a user's math concept description, refine it into a well-structured prompt "
            "that asks for a Manim script to visualize the concept. "
            "Do NOT generate code, only output the improved prompt."
        )

        response = model.generate_content(f"{system_prompt}\nUser Input: {user_input}")

        if response and hasattr(response, 'text'):
            return response.text.strip()
        else:
            return None

    def generate_manim_code(self, refined_prompt):
        """Send the refined prompt to Gemini Flash to generate only Manim code."""
        model = genai.GenerativeModel("gemini-1.5-flash")

        final_prompt = (
            f"{refined_prompt}\n\n"
            "Output only the Python Manim script. Do not add explanations or extra text. "
            "The script should define a Manim class called 'AutoScene'. "
            "Ensure that text elements are well-aligned and old text disappears before new text appears. "
            "Ensure proper alignment, remove previous text before adding new text, and include smooth transitions."
            "Take note of frame space and don't overflow out of frame. "
            "Try to utilize all the frame area without overlapping. "
        )

        response = model.generate_content(final_prompt)

        if response and hasattr(response, 'text'):
            return response.text.strip()
        else:
            return None

    def clean_text(self, text: str) -> str:
        prefix = "```python"
        suffix = "```"
        
        if text.startswith(prefix):
            text = text[len(prefix):]
        if text.endswith(suffix):
            text = text[:-len(suffix)]
        
        return text.strip()

    def save_manim_script(self, code, filename="generated_manim.py"):
        """Save the AI-generated Manim script to a file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(code)

    def run_manim_script(self, filename="generated_manim.py", scene_name="AutoScene"):
        """Run the Manim script and render a video."""
        try:
            command = f"manim -pql {filename} {scene_name}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def display_video(self):
        """Display the generated video in the UI."""
        try:
            # Find the most recent mp4 file in the media/videos directory
            media_dir = "./media/videos/generated_manim/480p15/"
            video_files = glob.glob(f"{media_dir}*.mp4")
            
            if not video_files:
                self.update_status("Error: No video file found", 0)
                return
                
            # Sort files by creation time (newest first)
            latest_video = max(video_files, key=os.path.getctime)
            
            # Extract a thumbnail from the video using ffmpeg
            thumbnail_path = "temp_thumbnail.png"
            subprocess.run(
                f"ffmpeg -i \"{latest_video}\" -ss 00:00:01 -vframes 1 \"{thumbnail_path}\" -y",
                shell=True,
                capture_output=True
            )
            
            # Load the thumbnail and display it
            if os.path.exists(thumbnail_path):
                img = Image.open(thumbnail_path)
                # Resize to fit the frame
                width, height = 640, 360
                img = img.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.video_label.config(image=photo)
                self.video_label.image = photo  # Keep a reference to prevent garbage collection
                
                # Add a play button overlay
                play_button = ttk.Button(
                    self.video_frame, 
                    text="Play Video", 
                    command=lambda: self.play_video(latest_video)
                )
                play_button.place(relx=0.5, rely=0.5, anchor="center")
                
                # Clean up
                os.remove(thumbnail_path)
            else:
                self.update_status("Error: Could not generate thumbnail", 0)
        except Exception as e:
            self.update_status(f"Error displaying video: {str(e)}", 0)
    
    def play_video(self, video_path):
        """Play the video in the default media player."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(video_path)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', video_path])
        except Exception as e:
            self.update_status(f"Error playing video: {str(e)}", 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ManimUI(root)
    root.mainloop()