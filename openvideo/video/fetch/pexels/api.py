import os
import json
import time
import subprocess
import numpy as np
from tqdm import tqdm
from openvideo.utils.file_utils import print_dict_as_table


class PexelsAPI:
    def __init__(
        self, 
        api: str, 
        save_path: str
    ) -> None:
        self.api = api
        self.save_path = save_path
        if os.path.exists(self.save_path):
            self.api_dict = np.load(self.save_path, allow_pickle=True).item()
            self.videos_dict = self.api_dict['videos']
            self.last_api_info = self.api_dict['last_api_info']
            self.summary = self.api_dict['summary']
            self.api_id_list = self.api_dict['api_id_list']
            self.show_info()
        else:
            self.api_dict = dict()
            self.api_dict["last_api_info"] = dict()
            self.api_dict["summary"] = dict()
            self.api_dict['videos'] = dict()
            self.api_dict['api_id_list'] = list()
            self.videos_dict = self.api_dict['videos']
            self.last_api_info = self.api_dict['last_api_info']
            self.summary = self.api_dict['summary']
            self.api_id_list = self.api_dict['api_id_list']
            print(f"{self.save_path} not find, generating a blank file...")
            np.save(self.save_path, self.api_dict)
    
    def show_info(self):
        print("summary is as followed")
        print_dict_as_table(self.summary)
        print("last api is as followed")
        print_dict_as_table(self.last_api_info)
        
    def fetch_api(
        self,
        start_page: int,
        end_page: int,
        save_api_dict_every_pages: int=10
    ):
        for page_idx in tqdm(range(start_page, end_page, 1)):
            time.sleep(1)
            command = f'curl -s -H "Authorization: {self.api}" "https://api.pexels.com/videos/popular/?page={page_idx}?per_page=50"'
            result = subprocess.check_output(command, shell=True)
            try:
                video_json_list = json.loads(result)['videos']
            except:
                print(f"skip page {page_idx}")
                continue
            for video_json in video_json_list:
                api_id = video_json['id']
                resolution = video_json['video_files'][0]['quality']
                origin_url = video_json['url']
                download_url = f"https://www.pexels.com/zh-cn/download/video/{api_id}"
                api = {
                    "api_id": api_id,
                    "origin_url": origin_url,
                    "download_url": download_url,
                    "resolution": resolution,
                    "page": page_idx
                }
                if api_id not in self.api_id_list:
                    self.api_id_list.append(api_id)
                    self.videos_dict[api_id] = api
                    self.last_api_info = api
            if (page_idx - start_page + 1) % save_api_dict_every_pages == 0:
                self.save_api_dict()
        
    def save_api_dict(self):
        hd_num = 0
        sd_num = 0
        uhd_num = 0
        mobile_num = 0
        total_num = 0
        for value in self.videos_dict.values():
            if value['resolution'] == "sd":
                sd_num += 1
            elif value['resolution'] == 'hd':
                hd_num += 1
            elif value['resolution'] == 'uhd':
                uhd_num += 1
            elif value['resolution'] == 'mobile':
                mobile_num += 1
            total_num += 1
        self.summary = dict()
        self.summary['sd_num'] = sd_num
        self.summary['hd_num'] = hd_num
        self.summary['uhd_num'] = uhd_num
        self.summary['mobile_num'] = mobile_num
        self.summary['total_num'] = total_num
        self.api_dict['summary'] = self.summary
        self.api_dict['last_api_info'] = self.last_api_info
        self.api_dict['video'] = self.videos_dict
        self.api_dict['api_id_list'] = self.api_id_list
        np.save(self.save_path, self.api_dict)