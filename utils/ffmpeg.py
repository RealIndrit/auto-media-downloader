from pathlib import Path
import requests
import os
import zipfile
from utils import settings
from pydub import AudioSegment
import subprocess

FFMPEG_BINARIES = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_FOLDER_DEFAULT = "./ffmpeg/"


def ffmpeg_bridge(*args):
    cmd = [settings.config["global"]["ffmpeg"]["ffmpeg"]] + list(args)
    subprocess.run(cmd)


def __download_ffmpeg(url: str, output: str):
    print("Downloading ffmpeg")
    response = requests.get(url)
    with open("temp.zip", "wb") as f:
        f.write(response.content)
    print("Downloaded ffmpeg")

    print("Extracting ffmpeg")
    with zipfile.ZipFile("temp.zip", 'r') as zip_ref:
        zip_ref.extractall(output)
    print("Extracted ffmpeg")
    Path("temp.zip").unlink()

    return Path(
        os.path.join(FFMPEG_FOLDER_DEFAULT,
                     os.listdir(output)[0], "bin"))


def resolve_ffmpeg():
    if (not settings.config["global"]["ffmpeg"]["ffmpeg"]
            or not settings.config["global"]["ffmpeg"]["ffprobe"]
            or not settings.config["global"]["ffmpeg"]["ffplay"]
        ) and not settings.config["global"]["ffmpeg"]["custom"]:
        ffmpeg_path = __download_ffmpeg(FFMPEG_BINARIES, FFMPEG_FOLDER_DEFAULT)
        print(ffmpeg_path)
        settings.config["global"]["ffmpeg"]["ffmpeg"] = os.path.join(
            ffmpeg_path, "ffmpeg.exe")
        settings.config["global"]["ffmpeg"]["ffprobe"] = os.path.join(
            ffmpeg_path, "ffprobe.exe")
        settings.config["global"]["ffmpeg"]["ffplay"] = os.path.join(
            ffmpeg_path, "ffplay.exe")

        AudioSegment.converter = settings.config["global"]["ffmpeg"]["ffmpeg"]
        AudioSegment.ffprobe = settings.config["global"]["ffmpeg"]["ffprobe"]
        AudioSegment.ffplay = settings.config["global"]["ffmpeg"]["ffplay"]
