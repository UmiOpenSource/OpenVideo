import os
import time
import shutil
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from openvideo.video.base.data import VideoData
from openvideo.video.base.dataset import VideoDataset
from openvideo.utils.file_utils import download, get_md5
from openvideo.video.fetch.utils import create_chrome_driver
from .uid import generate_pixabay_video_uid


class PixabayVideoFetch(VideoDataset):
    def __init__(self, root_dir: str):
        super().__init__(
            website="pixabay", 
            root_dir=root_dir,
        )
        
    def download(
        self, 
        chrome_exe_path: str,
        username: str,
        password: str,
        headless: bool=True,
        disable_gpu: bool=True,
        platform: str="windows",
    ):
        self.driver = create_chrome_driver(
            chrome_exe_path=chrome_exe_path,
            save_dir=self.tmp_dir,
            headless=headless,
            disable_gpu=disable_gpu,
        )
        self.login(username, password)
        for page_idx in range(524):
            print(f"download the page_{page_idx}")
            self.download_with_page_idx(
                page_idx=page_idx+1,
                platform=platform
            )

    def download_with_page_idx(
        self,
        page_idx: int,
        platform: str
    ):
        # read from the view source (.html)
        view_source_download_path = os.path.join(self.cache_dir, f"pixabay_page{page_idx}.html")
        with open(view_source_download_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        # resolution
        html_resolutions = soup.find_all(class_="videoDef--zlvbV")
        resolutions = [video.find('strong').text for video in html_resolutions]
        # unprocess download url
        html_unprocess_download_urls = soup.find_all(class_="link--WHWzm")
        orgin_urls = ["https://pixabay.com/zh" + video['href'] for video in html_unprocess_download_urls]
        
        for idx, origin_url in tqdm(enumerate(orgin_urls)):
            # download the origin page's view source
            origin_url: str
            self.driver.get(origin_url)
            time.sleep(0.1)
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            owner = soup.find(class_='usernameFollowersContainer--0odKZ').find('a').text
            name = origin_url.split('/')[-2]
            text = name
            resolution = resolutions[idx]
            
            # get the download url
            download_url_number = origin_url.split("/")[-2].split("-")[-1]
            download_url = origin_url.replace("/videos/", "/videos/download/")
            download_url = download_url.replace(
                download_url.split("/")[-2], 
                "video-" + download_url_number + "_source.mp4"
            )[0:-1]
            
            # check if is downloaded sucessfully 
            if download_url in self.monitor.downloaded_url_list:
                continue
            
            # download
            self.driver.get(download_url)
            html_page_source = self.driver.page_source
            soup_page_source = BeautifulSoup(html_page_source, 'html.parser')
            download_link = soup_page_source.find('video').find('source')['src']
            download_success = True
            tmp_filename =  f"{download_url_number}_tmp.mp4"
            tmp_download_path = os.path.join(self.tmp_dir, tmp_filename)
            try:
                download(tmp_download_path, download_link)
            except:
                download_success = False
                cur_time = str(datetime.now())
                error_message = f"{cur_time}: error occurred when the download url is {download_url}"
                with open(self.log_path, "a") as log_file:
                    log_file.write(error_message)
            if not download_success:
                continue
            
            # if download sucessfully, record the info of video
            md5 = get_md5(tmp_download_path)
            uid = generate_pixabay_video_uid(
                page_idx=page_idx,
                inner_idx=idx,
                origin_idx=download_url_number,
                md5=md5
            )
            save_path = os.path.join(self.download_dir, f"{uid}.mp4")
            shutil.move(tmp_download_path, save_path)

            video_info_dict = {
                "uid": uid,
                "name": name,
                "text": text,
                "free": True,
                "owner": owner,
                "save_path": save_path,
                "website": self.website,
                "origin_url": origin_url,
                "download_url": download_url,
                "resolution": resolution,
            }

            video_data = VideoData(
                video_info_dict=video_info_dict,
                basic_info_include=False
            )
            new_video_info_dict = video_data.get_video_info_dict()
            self.monitor.add_item(new_video_info_dict)
            self.monitor.update_state()
            self.monitor.save_state_dict()
            
    def login(
        self, 
        username: str, 
        password: str
    ):
        self.driver.get('https://pixabay.com/videos/search/?order=ec')

        try:
            accept_cookies_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_cookies_button.click()
        except TimeoutException:
            print("No cookie acceptance button found or not clickable.")
            
        # login button
        login_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "loginButton--uIEF2")))
        login_button.click()

        # input username and password
        username_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "login_user")))
        username_input.send_keys(username)

        password_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "login_pass")))
        password_input.send_keys(password)

        # click submit button
        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "loginButton--cVPDu")))
            self.driver.execute_script("arguments[0].click();", submit_button)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error clicking the submit button: {e}")
        time.sleep(1)