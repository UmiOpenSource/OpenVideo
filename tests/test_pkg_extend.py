import os
import sys
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from openvideo.pkg_extend import youtube_dl_install_helper


def test_youtube_dl():
    youtube_dl_install_helper()
    

if __name__ == "__main__":
    test_youtube_dl()