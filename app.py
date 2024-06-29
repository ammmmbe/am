from flask import Flask, send_from_directory, redirect
import os
import random

app = Flask(__name__)

# Directory path to list files from - use environment variable for flexibility
FILES_PATH = os.getenv('FILES_PATH', '/default/files/path')

# List to keep track of downloaded files - could use a database in production
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
    # Use Gunicorn as the WSGI server, bind to 0.0.0.0 for external access
    # Run with 4 worker processes (adjust as needed based on your application's needs)
    app.run(host='0.0.0.0', port=5000)
