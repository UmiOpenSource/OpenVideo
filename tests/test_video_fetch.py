import os
import sys
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from openvideo.video.fetch import MixkitVideoFetch


def test_mixkit():
    mixkit_fetch = MixkitVideoFetch(root_dir="tests/test_mixkit")
    mixkit_fetch.download_with_category_page_idx(
        category="sky",
        page_idx=1,
        start_idx=22,
        platform="linux"
    )
    
    
if __name__ == "__main__":
    test_mixkit()
