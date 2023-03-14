# YT-Shorts-AI
YouTube Auto Uploader
This script is used to automatically upload videos to YouTube using Selenium and Python. It logs in to a YouTube account, selects the option to upload a video, selects the video file, sets the title and description, selects the privacy settings, and then publishes the video.

How to Use
Install the required libraries:
Copy code
pip install selenium webdriver_manager
Add the video file you want to upload to the video_dir directory.
Update the Variables.py file with the correct test object locators for your YouTube account.
Run the script:
Copy code
python youtube_uploader.py
The script will prompt you to enter your YouTube login credentials.
Requirements
This script requires the following libraries to be installed:

Selenium
Webdriver_manager
shutil
Script Details
The login function in the script creates a Chrome web driver instance and initializes test objects for identifying web elements on the YouTube page. It takes two parameters, username and password, and returns a boolean value indicating if the login was successful or not.

The script then checks if the video_number.txt file exists, and if it does, reads the value of "i" from it. If the file does not exist, the value of "i" is set to 0. The script then navigates to YouTube and identifies test objects for the login page.

After successfully logging in, the script clicks on the create button and selects the upload video option. It then selects the video file, sets the title and description, selects the privacy settings, and publishes the video.

Once the video is uploaded successfully, it moves the uploaded video file to the used_videos_dir directory.

If an error occurs during the process, it prints a message indicating the error and returns False. Otherwise, it returns True.