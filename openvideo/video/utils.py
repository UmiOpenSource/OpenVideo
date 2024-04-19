import subprocess
from typing import Tuple
from moviepy.editor import VideoFileClip


def cal_video_duration(video_path: str) -> Tuple[float, bool]:
    try:
        # Attempt to load the video file
        with VideoFileClip(video_path) as video:
            # If the file is loaded successfully, check 
            # the duration to ensure it's a valid video
            if video.duration > 0:
                return video.duration
            else:
                return -1
    except Exception:
        # If an exception occurs, it's likely the file 
        # can't be properly loaded or is not a valid video file
        return -1
    

def check_video_integrity(video_path: str):
    command = [
        'ffmpeg', '-v', 'error', '-i',
        f'{video_path}', '-f', 'null', '-'
    ]
    result = subprocess.run(command, capture_output=True)
    if result.returncode == 0:
        return True
    else:
        return False