from utils import get_youtube_video_id
from moviepy.editor import VideoFileClip
import yt_dlp as youtube_dl
import os
import datetime

def main():
    file_path = 'input/input.txt'
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            video_urls = [line.strip() for line in file.readlines()]
    else:
        print("No input file found. Please provide an input file with video URLs.")
        return

    timestamps = {}
    sum_durations = 0
    for url in video_urls:
        if url.startswith(("http://", "https://")):
            video_id = get_youtube_video_id(url)
            video_path_mp4 = f'temp/{video_id}.mp4'
            video_path_webm = f'temp/{video_id}.webm'
            if os.path.isfile(video_path_mp4):
                video_path = video_path_mp4
            elif os.path.isfile(video_path_webm):
                video_path = video_path_webm
            else:
                print(f"No local file found for the video URL: {url}. Please ensure the video has been downloaded by '__main__.py'.")
                continue
        else:
            video_path = os.path.join('input', url)
            if not os.path.isfile(video_path):
                print(f"No local file found for the video: {url}. Please ensure the video exists.")
                continue

        # Get video duration using moviepy
        clip = VideoFileClip(video_path)
        duration = clip.duration  # in seconds

        # Calculate the start and end time of each video
        start_time_hh_mm_ss = str(datetime.timedelta(seconds=sum_durations))
        end_time_hh_mm_ss = str(datetime.timedelta(seconds=(sum_durations + duration)))

        # Check if the video is from YouTube or from a local file and use corresponding name
        if url.startswith(("http://", "https://")):
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', None)
            timestamps[video_title] = [start_time_hh_mm_ss, end_time_hh_mm_ss]
        else:
            video_name = os.path.basename(video_path)
            timestamps[video_name] = [start_time_hh_mm_ss, end_time_hh_mm_ss]

        sum_durations += duration

    # Write the timestamps to a text file
    with open("output/timestamps.txt", "w") as file:
        for name, times in timestamps.items():
            file.write(f"{times[0]}-{times[1]} - {name}\n")
    
    print("Timestamps generated in output/timestamps.txt")

if __name__ == "__main__":
    main()
