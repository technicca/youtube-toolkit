import youtube_dl
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import yt_dlp as youtube_dl
import os
import re
import requests
from io import BytesIO
from PIL import Image
import mimetypes

def get_youtube_video_id(url):
    # Extract video id from URL
    pattern = r"(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def download_video(url: str, output_path: str = "."):
    ydl_opts = {'outtmpl': f'{output_path}/%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        return f"{output_path}/{info_dict['id']}.{info_dict['ext']}"

def download_file(url: str, output_path: str = "."):
    response = requests.get(url)
    file_name = url.split("/")[-1]
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

def merge_audios(video_paths: list[str]):
    audio_clips = [AudioSegment.from_file(path) for path in video_paths]
    combined = AudioSegment.empty()
    for audio in audio_clips:
        combined += audio
    combined.export("/merged_audio.mp3", format='mp3')
    return "/merged_audio.mp3"

def is_gif_or_video(file_url: str) -> bool:
    mimetype, _ = mimetypes.guess_type(file_url)
    if mimetype:
        return mimetype.startswith(('video', 'image/gif'))
    return False


def generate_video(audio_path: str, image_url: str, output_path: str, loop: bool = False):
    audio = AudioFileClip(audio_path)
    if loop and is_gif_or_video(image_url):
        # Download the GIF or video file
        file_path = download_file(image_url)
        img_clip = VideoFileClip(file_path)
        img_clip = img_clip.set_fps(24)
        loops_required = int(audio.duration / img_clip.duration) + 1
        img_clip = concatenate_videoclips([img_clip]*loops_required, method='compose')
    else:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.save("image.png")
        img_clip = ImageClip("image.png")

    img_clip.set_duration(audio.duration).set_audio(audio).write_videofile(output_path, codec='libx264', fps=24)

def main():
    # Default URLs
    default_video_urls = [
        "https://youtu.be/1O0yazhqaxs",
        "https://youtu.be/TK4N5W22Gts"
    ]

    # File path
    file_path = 'input/input.txt'

    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            video_urls = [os.path.join('input', line.strip()) for line in file.readlines()]
    else:
        # If file doesn't exist or is empty, use default URLs
        video_urls = default_video_urls

    image_url = "https://i.imgur.com/4EmycCc.jpeg"
    output_path = "test.mp4"

    video_paths = []
    for url in video_urls:
        if url.startswith(("http://", "https://")):
            video_id = get_youtube_video_id(url)
            video_path = f'{video_id}.mp4'
            if not os.path.isfile(video_path):
                video_path = download_video(url)
        else:
            video_path = url
        video_paths.append(video_path)

    audio_path = merge_audios(video_paths)
    generate_video(audio_path, image_url, output_path, loop=True)


if __name__ == "__main__":
    main()

