#!/usr/bin/env python3
"""
setup.py - Installation script for Manim Math Visualization Generator

This script installs all required dependencies for:
1. The Manim library and its prerequisites
2. The UI application dependencies
3. FFmpeg for video processing

Run this script with: python setup.py
"""

import os
import sys
import platform
import subprocess
import shutil
import time

def print_header(message):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f" {message} ".center(80, "="))
    print("="*80)

def print_step(message):
    """Print a step message"""
    print(f"\n>> {message}")

def run_command(command, description=None, exit_on_error=True):
    """Run a shell command and handle errors"""
    if description:
        print(f"{description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✓ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr.strip()}")
        if exit_on_error:
            print("Setup failed. Please check the error message above.")
            sys.exit(1)
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python version")
    
    version = sys.version_info
    min_version = (3, 7)
    
    if version < min_version:
        print(f"Error: Python {min_version[0]}.{min_version[1]} or higher is required.")
        print(f"Current version: Python {version.major}.{version.minor}")
        sys.exit(1)
    
    print(f"✓ Using Python {version.major}.{version.minor}.{version.micro}")

def setup_system_dependencies():
    """Install system dependencies based on platform"""
    print_header("INSTALLING SYSTEM DEPENDENCIES")
    system = platform.system().lower()
    
    # Install FFmpeg
    print_step("Installing FFmpeg")
    if system == "windows":
        if shutil.which("choco"):
            run_command("choco install ffmpeg -y", "Installing FFmpeg using Chocolatey")
        else:
            print("Please install FFmpeg manually from: https://ffmpeg.org/download.html")
            print("After installation, make sure FFmpeg is added to your PATH.")
            input("Press Enter to continue after installing FFmpeg...")
    
    elif system == "darwin":  # macOS
        if shutil.which("brew"):
            run_command("brew install ffmpeg", "Installing FFmpeg using Homebrew")
        else:
            print("Installing Homebrew (required for FFmpeg)...")
            run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            run_command("brew install ffmpeg", "Installing FFmpeg using Homebrew")
    
    elif system == "linux":
        # Try different package managers
        if shutil.which("apt"):
            run_command("sudo apt update && sudo apt install -y ffmpeg", "Installing FFmpeg using apt")
        elif shutil.which("yum"):
            run_command("sudo yum install -y ffmpeg", "Installing FFmpeg using yum")
        elif shutil.which("dnf"):
            run_command("sudo dnf install -y ffmpeg", "Installing FFmpeg using dnf")
        else:
            print("Please install FFmpeg manually using your distribution's package manager.")
            input("Press Enter to continue after installing FFmpeg...")
    
    # Install Cairo (required for Manim)
    print_step("Installing Cairo (required for Manim)")
    if system == "windows":
        print("Cairo will be installed via pip later in the process")
    elif system == "darwin":
        if shutil.which("brew"):
            run_command("brew install cairo pango", "Installing Cairo using Homebrew")
    elif system == "linux":
        if shutil.which("apt"):
            run_command("sudo apt update && sudo apt install -y libcairo2-dev pkg-config python3-dev", 
                       "Installing Cairo using apt")
        elif shutil.which("yum"):
            run_command("sudo yum install -y cairo-devel pkg-config python3-devel", 
                       "Installing Cairo using yum")
        elif shutil.which("dnf"):
            run_command("sudo dnf install -y cairo-devel pkg-config python3-devel", 
                       "Installing Cairo using dnf")
        else:
            print("Please install Cairo manually using your distribution's package manager.")
            input("Press Enter to continue after installing Cairo...")
    
    # Verify FFmpeg installation
    if shutil.which("ffmpeg"):
        print("✓ FFmpeg is installed and available in PATH")
    else:
        print("⚠️ FFmpeg was not found. Some features may not work correctly.")

def create_virtual_environment():
    """Create a virtual environment for the application"""
    print_header("SETTING UP PYTHON ENVIRONMENT")
    print_step("Creating virtual environment")
    
    # Install virtualenv if needed
    if not shutil.which("pip"):
        print("pip is not installed. Please install pip first.")
        sys.exit(1)
    
    run_command("pip install --upgrade pip", "Upgrading pip")
    run_command("pip install virtualenv", "Installing virtualenv")
    
    # Create virtual environment
    venv_path = os.path.join(os.getcwd(), "venv")
    
    if os.path.exists(venv_path):
        print("Virtual environment already exists at:", venv_path)
    else:
        run_command(f"virtualenv {venv_path}", "Creating virtual environment")
    
    # Determine activate script path
    if platform.system().lower() == "windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
    
    print(f"✓ Virtual environment created at: {venv_path}")
    return activate_script

def install_python_dependencies(activate_script):
    """Install all required Python dependencies"""
    print_header("INSTALLING PYTHON PACKAGES")
    
    # Write requirements to a file
    requirements = """
# UI Dependencies
Pillow>=9.0.0
google-generativeai>=0.3.0

# Manim Dependencies
manim>=0.17.3
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
pycairo>=1.21.0
pygments>=2.10.0
networkx>=2.6.3
sympy>=1.9
colour>=0.1.5
isosurfaces>=0.1.0
svgelements>=1.9.0
mapbox-earcut>=0.12.10
moderngl>=5.6.4
moderngl-window>=2.4.1
watchdog>=2.1.6
IPython>=8.0.0
webcolors>=1.12
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements.strip())
    
    # Install the dependencies within the virtual environment
    print_step("Installing Python packages (this may take a while)")
    if platform.system().lower() == "windows":
        command = f"{activate_script} && pip install -r requirements.txt"
    else:
        command = f"source {activate_script} && pip install -r requirements.txt"
    
    run_command(command, "Installing required Python packages")
    print("✓ All Python dependencies installed successfully")

def create_startup_script(activate_script):
    """Create startup scripts for the application"""
    print_header("CREATING STARTUP SCRIPTS")
    
    if platform.system().lower() == "windows":
        # Create batch file for Windows
        with open("run_app.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"call {activate_script}\n")
            f.write(f"python manim_ui.py\n")
        
        print("✓ Created run_app.bat")
    else:
        # Create shell script for Unix-like systems
        with open("run_app.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"source {activate_script}\n")
            f.write("python manim_ui.py\n")
        
        # Make it executable
        os.chmod("run_app.sh", 0o755)
        print("✓ Created run_app.sh")

def create_api_directory():
    """Create directory for API key storage"""
    print_step("Creating API key directory")
    os.makedirs("api", exist_ok=True)
    print("✓ Created 'api' directory for API key storage")

def print_completion_message():
    """Print completion message with instructions"""
    print_header("SETUP COMPLETE")
    print("""
✅ All dependencies for the Manim Math Visualization Generator have been installed.

To run the application:
  - On Windows: Double-click run_app.bat
  - On macOS/Linux: Run ./run_app.sh in terminal

On first run, you'll be prompted to enter your Google Gemini API key.
If you don't have one, you can get it from: https://aistudio.google.com/

Enjoy creating math visualizations!
""")

def main():
    print_header("MANIM MATH VISUALIZATION GENERATOR SETUP")
    
    check_python_version()
    setup_system_dependencies()
    activate_script = create_virtual_environment()
    install_python_dependencies(activate_script)
    create_api_directory()
    create_startup_script(activate_script)
    print_completion_message()

if __name__ == "__main__":
    main()