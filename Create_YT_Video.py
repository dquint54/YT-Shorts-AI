import csv
import json
import os
import random
import urllib.request

import requests
from tqdm import tqdm

from Variables import pexels_api_key, query, orientation, save_dir, file_path, shazam_api_key, shazam_query, music_save_dir


def download_video(url: str, filename: str) -> None:
    """Downloads a video file from a given URL"""
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


def scrape_and_download_video(api_key: str, query: str, orientation: str, save_dir: str) -> None:
    """Scrapes a video from Pexels.com and downloads it to a given directory"""
    video_url = get_video_url(api_key, query, orientation)
    if video_url is None:
        return
    filename = os.path.join(save_dir, f"{query}_{random.randint(1, 100000)}.mp4")
    download_video(video_url, filename)
    print(f"Downloaded {filename} successfully")


def getFactFromFile():
    """Extracts the next line of text from a CSV file and returns it"""
    csv_file_path = 'CSV Files/cooking_facts.csv'
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip the first line (header)
        next(reader)
        # Get the next line (first row)
        row = next(reader)
        # Return the first cell in the row
        print(row)
        return row[0]

def removeFactFromFile(file_path):
    """Removes the first line from a CSV file"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])


def main():

    scrape_and_download_video(pexels_api_key, query, orientation, save_dir)
    fact = getFactFromFile()
    removeFactFromFile(file_path)



if __name__ == '__main__':

        main()