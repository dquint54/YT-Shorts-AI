import os
import json
import requests
import random
from tqdm import tqdm
import time
from datetime import datetime

from Variables import pexels_api_key, query, orientation, save_dir



def download_video(url: str, filename: str) -> None:
    """Donwloading Video using a progress bar."""
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
        print("Something wrong in Download Video")



def scrape_and_download_video(api_key: str, query: str, orientation: str, save_dir: str) -> str:
    """Scrapes a video from Pexels.com and downloads it to a given directory"""
    headers = {'Authorization': api_key}
    params = {'query': query, 'orientation': orientation}
    response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to scrape videos. Status code: {response.status_code}")
        return None
    data = json.loads(response.text)
    video_count = len(data['videos'])
    if video_count == 0:
        print(f"No videos found for query: {query}")
        return None
    next_video_index = random.randint(0, video_count - 1)
    video_url = data['videos'][next_video_index]['video_files'][0]['link']
    filename = os.path.join(save_dir, f"{query}_{next_video_index}.mp4")
    download_video(video_url, filename)
    print(f"Downloaded {filename} successfully")
    return filename


def main():
    filename = scrape_and_download_video(pexels_api_key, query, orientation, save_dir)
    if filename:
        print(f"Video saved as {filename}")


if __name__ == '__main__':
    main()
