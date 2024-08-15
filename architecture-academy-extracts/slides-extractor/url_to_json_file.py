import re
import os

def extract_presentation_id(url):
    """Extract the presentation ID from a Google Slides URL."""
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    else:
        return None

def main():
    # Ask the user for the Google Slides URL
    url = input("Enter the Google Slides URL: ")

    # Extract the presentation ID
    presentation_id = extract_presentation_id(url)
    if presentation_id:
        print(f"Presentation ID: {presentation_id}")
    else:
        print("Invalid URL. Please try again.")
        return

    # Ask for the file name to save the JSON data
    file_name = input("Enter the file name to save the JSON (without extension): ")
    file_path = os.path.join('..', 'json', f"{file_name}.json")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create an empty JSON file
    with open(file_path, 'w') as json_file:
        json_file.write("{}")  # Write an empty JSON object as a placeholder

    print(f"Empty JSON file created at {file_path}")
    print(f"Presentation ID: {presentation_id}")

if __name__ == "__main__":
    main()