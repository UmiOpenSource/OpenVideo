import os
import subprocess
from openvideo.utils.file_utils import get_md5


def extract_key_frames(
    video_path: str, 
    save_dir: str,
    filename: str = None
):
    if filename is None:
        filename = get_md5(video_path)
    save_path = os.path.join(save_dir, filename)
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', "select=eq(pict_type\,I)",
        '-vsync', 'vfr',
        f"{save_path}_%03d.jpg"
    ]
    
    try:
        subprocess.run(command, check=True)
        print("Key frames extraction completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting key frames: {e}")
