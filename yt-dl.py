import os
import sys
import subprocess
from pytube import YouTube

def get_yt_audio(link):
    """
    Downloads the audio stream of the given YouTube video link.
    :param link: URL of the YouTube video.
    :return: File path of the downloaded audio file.
    """
    print(f"Downloading audio from: {link}")
    yt = YouTube(link)
    audio_stream = yt.streams.get_audio_only()
    filename = "./yt-tmp.wav"

    # Check if a file with the same name exists and remove it
    if os.path.exists(filename):
        os.remove(filename)

    downloaded_file = audio_stream.download(filename=filename)
    print(f"Original Audio downloaded: {downloaded_file}")  # Moved this line up
    convert_to_16bit_wav(downloaded_file)
    return downloaded_file

def convert_to_16bit_wav(input_file):
    """
    Converts an audio file to 16-bit WAV format using FFmpeg. If the output file already exists, it is replaced.
    :param input_file: Path of the input audio file.
    """
    output_file = input_file.replace('.wav', '-16.wav')

    # Check if a file with the same name exists and remove it
    if os.path.exists(output_file):
        os.remove(output_file)

    command = [
        'ffmpeg', '-i', input_file, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', output_file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Converted to 16-bit WAV: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python yt_dl.py <YouTube_Link>")
        sys.exit(1)

    youtube_link = sys.argv[1]
    print(f"Received YouTube link: {youtube_link}")
    get_yt_audio(youtube_link)

if __name__ == "__main__":
    main()
