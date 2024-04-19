import os
import numpy as np
from datetime import datetime


class VideoMonitor:
    def __init__(
        self,
        save_path: str,
        website: str
    ):
        self.save_path = save_path
        self.website = website
        self.videos_state_dict = dict()
        self.videos = dict()
        self.summary = dict()
        self.last_video = dict()
        self.downloaded_url_list = list()
        self.md5_list = list()
        self.videos_num = None
        self.free_num = None
        self.success_num = None
        self.fail_num = None
        self.sum_size = None
        
    def load_state(self):
        if os.path.exists(self.save_path):
            self.videos_state_dict = np.load(self.save_path, allow_pickle=True).item()
            self.videos = self.videos_state_dict['videos']
            self.summary = self.videos_state_dict['summary']
            self.last_video = self.videos_state_dict['last_video']
            self.downloaded_url_list = self.videos_state_dict['downloaded_url_list']
            self.md5_list = self.videos_state_dict['md5_list']
            self.last_save_time = self.videos_state_dict['last_save_time']
            self.videos_num = self.summary['videos_num']
            self.free_num = self.summary['free_num']
            self.success_num = self.summary['success_num']
            self.fail_num = self.summary['fail_num']
            self.sum_size = self.summary['sum_size']
        else:
            print(f"{self.save_path} is not found, thus generating a blank file.")
            self.videos_state_dict['videos'] = dict()
            self.videos_state_dict['summary'] = dict()
            self.videos_state_dict['summary']['videos_num'] = 0
            self.videos_state_dict['summary']['free_num'] = 0
            self.videos_state_dict['summary']['success_num'] = 0
            self.videos_state_dict['summary']['fail_num'] = 0
            self.videos_state_dict['summary']['sum_size'] = 0
            self.videos_state_dict['last_video'] = dict()
            self.videos_state_dict['downloaded_url_list'] = list()
            self.videos_state_dict['md5_list'] = list()
            self.videos_state_dict['last_save_time'] = str(datetime.now())
            self.save_state_dict()
        
    def update_state(self):
        # get the details
        self.videos_num = len(self.videos)
        self.success_num = 0
        self.fail_num = 0
        self.free_num = 0
        self.sum_size = 0
        for video_info_dict in self.videos.values():
            if video_info_dict["integrity"] == True:
                self.success_num += 1
            else:
                self.fail_num += 1
            if video_info_dict['free']:
                self.free_num += 1
            self.sum_size += video_info_dict['size']
        self.summary['videos_num'] = self.videos_num
        self.summary['free_num'] = self.free_num
        self.summary['success_num'] = self.success_num
        self.summary['fail_num'] = self.fail_num
        self.summary['sum_size'] = self.sum_size
        self.videos_state_dict['videos'] = self.videos
        self.videos_state_dict['summary'] = self.summary
        self.videos_state_dict['last_video'] = self.last_video
        self.videos_state_dict['downloaded_url_list'] = self.downloaded_url_list
        self.videos_state_dict['last_save_time'] = str(datetime.now())
        
    def save_state_dict(self):
        np.save(self.save_path, self.videos_state_dict)

    def add_item(self, video_info_dict: dict) -> bool:
        if video_info_dict['md5'] not in self.md5_list:
            self.md5_list.append(video_info_dict['md5'])
            video_uid = video_info_dict['uid']
            self.videos[video_uid] = video_info_dict
            if video_info_dict["integrity"] == True:
                self.last_video = video_info_dict
                self.downloaded_url_list.append(video_info_dict['download_url'])
            return True
        else:
            return False