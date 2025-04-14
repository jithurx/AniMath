# 🧮 Manim Math Visualization Generator

> Create beautiful animations of mathematical concepts with AI assistance!

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)

## 📚 Overview

The **Manim Math Visualization Generator** is a powerful tool that combines the visualization capabilities of [Manim](https://www.manim.community/) with the intelligence of Google's Gemini AI. This application allows you to transform plain text descriptions of mathematical concepts into stunning, animated visualizations with just a few clicks.

Perfect for:
- 👩‍🏫 Teachers explaining complex math concepts
- 👨‍🎓 Students creating visual study aids
- 💻 Content creators developing educational materials
- 🧪 Researchers visualizing mathematical models

## ✨ Features

- 🤖 AI-powered conversion of math descriptions to Manim code
- 📊 Beautiful animations with professional-quality rendering
- 🎯 User-friendly interface requiring no coding knowledge
- 🎬 Video export for use in presentations or educational content
- ⚙️ Seamless integration with Google Gemini's AI capabilities

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection (for API access)
- Google Gemini API key ([Get one here](https://aistudio.google.com/))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/manim-math-visualizer.git
   cd manim-math-visualizer
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   
   This will automatically:
   - Install Python dependencies (Manim, Pillow, Google Generative AI, etc.)
   - Set up FFmpeg for video processing
   - Install Cairo and other system dependencies
   - Create a virtual environment
   - Generate startup scripts

3. **Launch the application**
   - On Windows: Double-click `main.py`
   - On macOS/Linux: Run `./main.py` in terminal

4. **Enter your Google Gemini API key** when prompted on first run

## 🖥️ Using the Application

1. **Enter your mathematical concept** in the text field
   ```
   Examples:
   - Show the proof of the Pythagorean theorem geometrically
   - Visualize the convergence of a Taylor series for sin(x)
   - Demonstrate the concept of a derivative as a limit
   ```

2. **Click "Generate Visualization"**
   - The application will refine your prompt
   - Generate Manim code
   - Render the animation
   - Display the result in the application

3. **View and use the generated content**
   - Examine the generated Manim code
   - Play the video in your default media player
   - The video file is saved in the `media/videos/` directory

## 🔧 Advanced Configuration

### Changing Your API Key

1. Click the "⚙️ Settings" button in the top-right corner
2. Select "Change API Key" and enter your new key

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU       | Dual-core | Quad-core |
| RAM       | 4GB     | 8GB or more |
| Storage   | 1GB free | 5GB free |
| OS        | Windows 10, macOS 10.14, Ubuntu 18.04 | Latest version |

## 🚀 Future Enhancements

- [ ] Support for advanced Manim customization options
- [ ] Export to multiple video formats and resolutions
- [ ] Library of sample concepts and visualizations
- [ ] Collaborative sharing of generated animations
- [ ] Integration with learning management systems
- [ ] Direct upload to YouTube and other platforms

## 📝 Troubleshooting

### Common Issues

**Error: FFmpeg not found in PATH**
- Ensure FFmpeg is installed properly following the installation instructions
- Restart the application after installation

**API Key Issues**
- Verify your Google Gemini API key is valid
- Check your internet connection
- Ensure you have sufficient API quota remaining

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- [Manim Community](https://www.manim.community/) for the incredible animation engine
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI capabilities
- All open-source contributors who made this project possible