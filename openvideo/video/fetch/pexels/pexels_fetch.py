import os
import time
import shutil
import numpy as np
from tqdm import tqdm
from openvideo.video.base.data import VideoData
from openvideo.video.base.dataset import VideoDataset
from openvideo.utils.file_utils import get_md5
from openvideo.video.fetch.utils import create_chrome_driver
from .uid import generate_pexels_video_uid


class PexelsVdieoFetch(VideoDataset):
    def __init__(self, root_dir: str):
        super().__init__(
            website="pexels", 
            root_dir=root_dir,
        )
        self.finish_api_id_list = self.monitor.videos_state_dict.get(
            'finish_api_id_list', list()
        )
        self.finish_api_id_list: list
        
    def download(
        self, 
        api_npy_save_path: str,
        chrome_exe_path: str,
        headless: bool=True,
        disable_gpu: bool=True,
        sleep_interval: int=1,
        timeout: int=30,
        platform: str="windows",
    ):
        self.driver = create_chrome_driver(
            chrome_exe_path=chrome_exe_path,
            save_dir=self.tmp_dir,
            headless=headless,
            disable_gpu=disable_gpu,
        )
        api_dict = np.load(api_npy_save_path, allow_pickle=True).item()
        api_video_dict = api_dict['videos']
        api_video_dict: dict
        for api_video_info in tqdm(api_video_dict.values()):
            if api_video_info['api_id'] in self.finish_api_id_list:
                continue
            self.download_with_api_video_info(
                api_video_info,
                sleep_interval=sleep_interval,
                timeout=timeout,
                platform=platform
            )

    def download_with_api_video_info(
        self,
        api_video_info: dict,
        sleep_interval: int,
        timeout: int,
        platform: str = "windows"
    ):
        api_id = api_video_info['api_id']
        origin_url = api_video_info['origin_url']
        download_url = api_video_info['download_url']
        resolution = api_video_info['resolution']
        page_idx = api_video_info['page']
        time.sleep(0.1)
        self.driver.get(download_url)
        download_success = self.wait_for_download(
            sleep_interval=sleep_interval,
            timeout=timeout
        )
        time.sleep(2)
        if not download_success:
            error_message = f"error occurred when the download url is {download_url}"
            self.log_error(error_message)
            shutil.rmtree(self.tmp_dir)
            os.makedirs(self.tmp_dir)
        else:
            tmp_dir_files = os.listdir(self.tmp_dir)
            if len(tmp_dir_files) != 1:
                raise ValueError()
            tmp_download_path = os.path.join(self.tmp_dir, tmp_dir_files[0])
            md5 = get_md5(tmp_download_path)
            
            # record the info of video
            uid = generate_pexels_video_uid(
                page_idx=page_idx,
                origin_idx=api_id,
                md5=md5
            )
            save_path = os.path.join(self.download_dir, f"{uid}.mp4")
            shutil.move(tmp_download_path, save_path)
            self.finish_api_id_list.append(api_id)
            
            video_info_dict = {
                "uid": uid,
                "name": None,
                "text": None,
                "free": True,
                "owner": None,
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
            self.monitor.videos_state_dict['finish_api_id_list'] = self.finish_api_id_list
            self.monitor.save_state_dict()
        
        
    def wait_for_download(
        self,
        sleep_interval: int=1,
        timeout: int=60
    ):
        elapsed_time = 0
        while elapsed_time < timeout:
            files = os.listdir(self.tmp_dir)
            if files:
                downloading = False
                for file in files:
                    if file.endswith('.crdownload'):
                        downloading = True
                        break  
                if not downloading:
                    return True
            time.sleep(sleep_interval)
            elapsed_time += sleep_interval
        return False