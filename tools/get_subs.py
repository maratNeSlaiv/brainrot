import subprocess

def generate_subtitles(input_file, output_dir, model="large", task="translate"):
    """
    Generate subtitles using auto_subtitle.

    Parameters:
    - input_file (str): Path to the input video file.
    - output_dir (str): Directory where output files will be saved.
    - model (str): The model to use for subtitle generation (default is "large").
    - task (str): Task to perform, e.g., "translate" (default is "translate").

    Returns:
    - str: Output from the command execution.
    """
    command = [
        "auto_subtitle",
        input_file,
        "-o", output_dir,
        "--model", model,
        "--task", task
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Subtitles generated successfully.")
    else:
        print("Error generating subtitles:", result.stderr)
    
    return result.stdout

if __name__ == '__main__':
    # Example usage:
    output = generate_subtitles(
        "/Users/maratorozaliev/Desktop/ishowspeed-almost-dies-doing-the-vacuum-challenge-1080-publer.io.mp4",
        "subtitled/"
    )
    print(output)
