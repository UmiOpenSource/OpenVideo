import os
import shutil
from openvideo.utils.file_utils import download, extract_archive

URL = "https://huggingface.co/heatingma/OpenVideo/resolve/main/youtube-dl-2024.04.08.tar.gz"


def youtube_dl_install_helper():
    # download
    download(
        filename="youtube-dl-2024.04.08.tar.gz",
        url="https://huggingface.co/heatingma/OpenVideo/resolve/main/youtube-dl-2024.04.08.tar.gz",
        md5="13a329f344de20e3c752542dd01b3726"
    )
    
    # extract_archive the youtube-dl-2024.04.08.tar.gz
    extract_archive(
        archive_path="youtube-dl-2024.04.08.tar.gz",
        extract_path="youtube-dl-2024.04.08"
    )
    
    # build dist package
    ori_dir = os.getcwd()
    os.chdir("youtube-dl-2024.04.08/youtube-dl")
    os.system("python setup.py sdist")
    os.chdir(ori_dir)
    
    # pip install youtube_dl-2024.4.8.tar.gz
    ori_dir = os.getcwd()
    os.chdir("youtube-dl-2024.04.08/youtube-dl/dist")
    os.system("pip install youtube_dl-2024.4.8.tar.gz")
    os.chdir(ori_dir)
    
    # remove the package
    os.remove("youtube-dl-2024.04.08.tar.gz")
    shutil.rmtree("youtube-dl-2024.04.08")