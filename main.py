import google.generativeai as genai
import subprocess

# Replace with your Google Gemini API key
GEMINI_API_KEY = "API_KEY"

genai.configure(api_key=GEMINI_API_KEY)

def refine_prompt(user_input):
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
        print("Error: Failed to refine prompt.")
        return None

def generate_manim_code(refined_prompt):
    """Send the refined prompt to Gemini Flash to generate only Manim code."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    final_prompt = (
        f"{refined_prompt}\n\n"
        "Output only the Python Manim script. Do not add explanations or extra text. "
        "Based on the "
        "The script should define a Manim class called 'AutoScene'. "
        "Ensure that text elements are well-aligned and old text disappears before new text appears. "
        "Ensure proper alignment, remove previous text before adding new text, and include smooth transitions. "
        "Take note of frame space and don't overflow out of frame. "
        "Try to utilize all the frame area without overlapping."
    )

    response = model.generate_content(final_prompt)

    if response and hasattr(response, 'text'):
        return response.text.strip()
    else:
        print("Error: Failed to generate Manim code.")
        return None

def clean_text(text: str) -> str:
    prefix = "```python"
    suffix = "```"
    
    if text.startswith(prefix):
        text = text[len(prefix):]
    if text.endswith(suffix):
        text = text[:-len(suffix)]
    
    return text.strip()

def save_manim_script(code, filename="generated_manim.py"):
    """Save the AI-generated Manim script to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(code)

def run_manim_script(filename="generated_manim.py", scene_name="AutoScene"):
    """Run the Manim script and render a video."""
    command = f"manim -pql {filename} {scene_name}"
    subprocess.run(command, shell=True)

def main():
    user_input = input("Enter a math concept to visualize with Manim: ")

    print("\nRefining prompt with Gemini Flash 2.0...")
    refined_prompt = refine_prompt(user_input)

    if refined_prompt:
        print("\nUsing refined prompt to generate Manim code...\n", refined_prompt)
        manim_code = generate_manim_code(refined_prompt)

        if manim_code:
            print("\nGenerated Manim Code:\n")
            clean_manim_code = clean_text(manim_code)
            print(clean_manim_code)  # Print the generated Manim script

            print("\nSaving Manim script...")
            
            save_manim_script(clean_manim_code)
            
            print("\nRunning Manim script...")
            run_manim_script()
        else:
            print("Failed to generate Manim code.")
    else:
        print("Failed to refine prompt.")

if __name__ == "__main__":
    main()
