import os
import sys
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from openvideo.utils import download, get_md5
from openvideo.video.utils import check_video_integrity
from openvideo.video.clean import VideoCleaner


def test_video_clean():
    if not os.path.exists("tests/test_clean/"):
        os.makedirs("tests/test_clean/")
    
    # download the test video
    download(
        filename="tests/test_clean/panda_example.mp4",
        url="https://huggingface.co/heatingma/OpenVideo/resolve/main/panda_example.mp4"
    )
    download(
        filename="tests/test_clean/mixkit_example.mp4",
        url="https://huggingface.co/heatingma/OpenVideo/resolve/main/mixkit_example.mp4"
    )
    
    # create a cleaner
    cleaner = VideoCleaner(src_dir="tests/test_clean", out_dir="tests/test_clean_out")
    cleaner.clean()
        

if __name__ == "__main__":
    test_video_clean()
