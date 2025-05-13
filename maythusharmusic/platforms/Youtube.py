import asyncio
import os
import re
import json
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from maythusharmusic.utils.database import is_on_off
from maythusharmusic.utils.formatters import time_to_seconds

API_KEY = "1EdAhtfqtegJL0A6I6RjCaxv"

import os
import glob
import random
import logging


import requests
import os
import time
def extract_video_id(link: str) -> str:
    """
    Extracts the video ID from a variety of YouTube links.
    Supports full, shortened, and playlist URLs.
    """
    # Regular expression to match different YouTube link formats
    patterns = [
        r'youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=)([0-9A-Za-z_-]{11})',  # youtube.com/watch?v= or youtube.com/embed/
        r'youtu\.be\/([0-9A-Za-z_-]{11})',  # youtu.be/short link
        r'youtube\.com\/(?:playlist\?list=[^&]+&v=|v\/)([0-9A-Za-z_-]{11})',  # youtube.com/playlist?list= and youtube.com/v/
        r'youtube\.com\/(?:.*\?v=|.*\/)([0-9A-Za-z_-]{11})'  # youtube.com/watch?v= with additional query parameters
    ]

    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube link provided.")
def api_dl(video_id: str) -> str:
    api_url = f"http://159.89.175.53:8080/download/song/{video_id}?key={API_KEY}"
    file_path = os.path.join("downloads", f"{video_id}.mp3")

    # Check if file already exists
    if os.path.exists(file_path):
        print(f"{file_path} already exists. Skipping download.")
        return file_path

    # Download the file
    response = requests.get(api_url, stream=True)

    if response.status_code == 200:
        os.makedirs("downloads", exist_ok=True)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {file_path}")
        return file_path
    else:
        print(f"Failed to download {video_id}. Status: {response.status_code}")
        return None





def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Choosen File : {cookie_txt_file}\n')
    return f"""cookies/{str(cookie_txt_file).split("/")[-1]}"""



async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_txt_file(),
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

    def parse_size(formats):
        total_size = 0
        for format in formats:
            if 'filesize' in format:
                total_size += format['filesize']
        return total_size

    info = await get_format_info(link)
    if info is None:
        return None
    
    formats = info.get('formats', [])
    if not formats:
        print("No formats found.")
        return None
    
    total_size = parse_size(formats)
    return total_size

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        return downloaded_file, direct
