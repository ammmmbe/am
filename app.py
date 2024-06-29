from flask import Flask, send_from_directory, redirect
import os
import random

app = Flask(__name__)

# Directory path to list files from
# Adjust this path according to your Render.com environment or configure it dynamically
FILES_PATH = '/path/to/your/files'  # Replace with your actual path

# List to keep track of downloaded files
downloaded_files = []

@app.route('/')
def index():
    return redirect('/download')

@app.route('/download')
def download():
    try:
        # Get list of .cfg files in the specified directory
        files = os.listdir(FILES_PATH)
        cfg_files = [f for f in files if os.path.isfile(os.path.join(FILES_PATH, f)) and f.endswith('.cfg')]

        # Shuffle the list of files
        random.shuffle(cfg_files)

        # Find the next file that hasn't been downloaded yet
        file_to_download = next((f for f in cfg_files if f not in downloaded_files), None)

        if file_to_download:
            # Add the downloaded file to the list
            downloaded_files.append(file_to_download)

            # Provide the file as a downloadable link
            return send_from_directory(FILES_PATH, file_to_download, as_attachment=True)
        else:
            return "All files have been downloaded."

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    # Run the application with debug mode enabled for development
    app.run(host='0.0.0.0', port=5000)
