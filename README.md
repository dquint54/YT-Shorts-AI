
# YouTube Video Uploader
This script automates the process of uploading videos to YouTube. It logs in to a YouTube account, uploads videos, and assigns titles and descriptions to them.

## Features
- Logs in to a YouTube account
- Uploads videos with generated titles and descriptions
- Moves uploaded videos to a specified directory
- Uses a random sleep timer to mimic human behavior

## Prerequisites
 Before using this script, you need to install the following Python packages:
- selenium
- webdriver-manager
- openai

You can install them using pip:  

pip install selenium webdriver-manager openai

## Configuration

The configuration for this script is stored in the config.json file. You need to set the following:

- username: Your YouTube account's email address
- password: Your YouTube account's password
- video_dir: The directory containing the videos you want to upload
- used_videos_dir: The directory where you want to move the uploaded videos
- api_key: Your OpenAI API key for generating descriptions


## Usage
1. Configure the config.json file with your account credentials, directories, and API key.
2. Make sure the required Python packages are installed.
3. Run the script by executing:

python3 youtube_video_uploader.py

The script will log in to your YouTube account, upload the specified number of videos, and assign generated titles and descriptions to them. The uploaded videos will then be moved to the used_videos_dir. The script logs its progress in the upload_log.log file.

Note: This script is for educational purposes only. Make sure to follow YouTube's terms of service when using any automation tools.
