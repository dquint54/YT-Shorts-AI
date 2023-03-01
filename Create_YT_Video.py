import csv
import json
import os
import random

import gtts
import requests
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from mutagen.mp3 import MP3
from tqdm import tqdm
from twisted.python.util import println

from Variables import pexels_api_key, query, orientation, save_dir, file_path, music_dir,video_dir


def download_video(url: str, filename: str) -> str:
    """Gets Video_Url from get_video_url and include a progress bar"""
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    return filename


def get_video_url(api_key: str, query: str, orientation: str) -> str:
    """Scrapes a random video URL from Pexels.com for a given query and orientation"""
    headers = {'Authorization': api_key}
    params = {'query': query, 'orientation': orientation}
    response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed to scrape videos. Status code: {response.status_code}")
        return None

    data = json.loads(response.text)
    video_count = len(data['videos'])
    if video_count == 0:
        print(f"No videos found for query '{query}' and orientation '{orientation}'")
        return None
    random_video_index = random.randint(0, video_count - 1)
    video_url = data['videos'][random_video_index]['video_files'][0]['link']

    return video_url


def scrape_and_download_video(api_key: str, query: str, orientation: str, save_dir: str):
    """Scrapes a video from Pexels.com and downloads it to a given directory"""
    video_url = get_video_url(api_key, query, orientation)
    if video_url is None:
        return
    filename = os.path.join(save_dir, f"{query}_{random.randint(1, 100000)}.mp4")
    data = download_video(video_url, filename)
    print(f"Downloaded {filename} successfully")
    return data

def getFactFromFile(file_path):
    """Extracts the next line of text from a CSV file and returns it"""

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip the first line (header)
        next(reader)
        # Get the next line (first row)
        row = next(reader)
        # Return the first cell in the row
        println(" ")
        print(row)
        fact_FF = row[0]
        return fact_FF

def removeFactFromFile(file_path):
    """Removes the first line from a CSV file"""

    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])


def get_random_song(music_dir):

    # Get the full path to the directory
    songs_dir = os.path.join(os.getcwd(), music_dir)

    # Get a list of all files in the directory
    song_files = os.listdir(songs_dir)

    # Select a random song file from the list
    random_song = random.choice(song_files)

    # Return the full path to the selected song file
    println("")
    print("Song Selected: " + random_song)

    song = os.path.join(songs_dir, random_song)
    return song

def get_random_video(video_dir):

    # Get the full path to the directory
    video_dir = os.path.join(os.getcwd(), music_dir)

    # Get a list of all files in the directory
    video_files = os.listdir(video_dir)

    # Select a random song file from the list
    random_video = random.choice(video_files)

    # Return the full path to the selected song file
    println("")
    print("video Selected: " + random_video)

    video = os.path.join(video_dir, random_video)
    return video



def combine_video_fact_song(fact_FF: str, song: str, video: str,):
    # Get random video from Pexels
    video_file = scrape_and_download_video(pexels_api_key, query, orientation, save_dir)
    if not video_file:
        print("Failed to download video")
        return
    quoteArray = []
    quoteArray.append(quoteText)

    quoteArray.append(quoteText)

    # Get random fact from CSV file
    fact = getFactFromFile(file_path)
    removeFactFromFile(file_path)

    # Get random song from music directory
    song = get_random_song(music_dir)

    # Create a video clip from the downloaded video
    video_clip = get_random_video(video_dir)

    for idx, sentence in enumerate(quoteArray):
        # create the audio
        save_as = f"tempFiles/temp_audio_{str(idx)}.mp3"
        tts = gtts.gTTS(sentence, lang='en', tld='ca')
        # save audio
        tts.save(save_as)
        audio = MP3(save_as)
        time = audio.info.length
        totalTTSTime += time
        print(f"Mp3 {str(idx)} has audio length: {time} ")

    # Add fact as text overlay
    text_clip = TextClip(
            txt=sentence,
            fontsize=70,
            size=(800, 0),
            font="Roboto-Regular",
            color="white",
            method="caption",
            ).set_position('center')

    video_with_text = CompositeVideoClip([video_clip, txt_clip])

    # Add song as audio
    audio_clip = AudioFileClip(song)
    final_clip = video_with_text.set_audio(audio_clip)

    # Save the final video
    final_clip.write_videofile("final_video.mp4", fps=30)


def main():

    scrape_and_download_video(pexels_api_key, query, orientation, save_dir)
    getFactFromFile(file_path)
    removeFactFromFile(file_path)
    get_random_song(music_dir)
    get_random_song(video_dir)
    combine_video_fact_song(pexels_api_key, query, orientation, save_dir, file_path, music_dir)



if __name__ == '__main__':

        main()