import requests
from selenium import webdriver


###############################################
#                  View Source                #
###############################################

USERAGENT = {
    "windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

REFER = {
    "mixkit": "https://mixkit.co",
    "pixabay": "https://pixabay.com/videos/search/?order=ec"
}

def download_view_source(
    website: str,
    url: str,
    save_path: str,
    platform: str="windows"
):
    headers = {
        "User-Agent": USERAGENT[platform],
        "referer": REFER[website]
    }
    res = requests.get(url, headers=headers)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(res.text)


###############################################
#                    Driver                   #
###############################################

def create_chrome_driver(
    chrome_exe_path: str,
    save_dir: str,
    headless: bool=True,
    disable_gpu: bool=True,
    platform: str="windows"
):
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_exe_path
    if headless:
        options.add_argument('--headless')
        options.add_argument(f"user-agent={USERAGENT[platform]}")
    if disable_gpu:
        options.add_argument('--disable-gpu')
    if platform == "linux":
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--enable-logging')
        options.add_argument('--v=1')
    options.add_argument('window-size=1920x1080')
    prefs = {
        "download.default_directory": save_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    return driver