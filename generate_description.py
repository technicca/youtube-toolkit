import yt_dlp as youtube_dl
import os

def get_channel_name(video_url):
    with youtube_dl.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        channel_name = info_dict.get('uploader', None)
    return channel_name
    
def main():
    # Define the text to be added
    subscribe_text = "Subscribe to the channel"
    credit_text = "Credit to original artists:"

    # Open the timestamps file and read the timestamps
    with open("output/timestamps.txt", "r") as timestamps_file:
        timestamps = timestamps_file.readlines()

    # Open the description file and write the text and timestamps
    with open("output/description.txt", "w") as description_file:
        # Write the subscribe text
        description_file.write(subscribe_text + "\n\n")

        # Write the timestamps
        for timestamp in timestamps:
            description_file.write(timestamp)

        # Write the credit text
        description_file.write("\n" + credit_text + "\n")

        # Write the video URLs
        with open("input/input.txt", "r") as input_file:
            video_urls = [url.strip() for url in input_file.readlines()]
        for url in video_urls:
            if url.startswith(("http://", "https://")):
                channel_name = get_channel_name(url)
                description_file.write(f"{channel_name} - {url}\n")
            else:
                filename_without_extension = os.path.splitext(url)[0]
                description_file.write(filename_without_extension + "\n")

    print("Description generated")

if __name__ == "__main__":
    main()