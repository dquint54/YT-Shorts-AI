
# YuTube Video Uploader 

This is a Python script for uploading videos to YouTube using Selenium web driver.

## Getting Started

### Prerequisites
The script requires the following dependencies:

* Selenium: pip install selenium
* ChromeDriver: pip install webdriver_manager
## Usage
* Open the Variables.py file and update the video_dir and used_videos_dir variables with your local directories.
* Open the login.py file and update the username and password variables with your YouTube credentials.
* Run the script: python login.py
## How it Works
The script uses the Selenium web driver to automate the process of uploading videos to YouTube. It navigates to the YouTube website, logs in to your account, and uploads the video from the specified directory. The script also generates a title and description for the video and sets the privacy settings to "public".
  * NOTE CREDENTIALS NOT UPLOADED TO GITHUB FOR SECURITY PURPOSE

# License
This project is licensed under the MIT License - see the LICENSE file for details.
