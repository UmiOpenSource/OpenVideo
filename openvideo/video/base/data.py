import os
from typing import Tuple
from datetime import datetime
from openvideo.utils.file_utils import get_md5
from openvideo.video.utils import cal_video_duration, check_video_integrity


class VideoData:
    def __init__(
        self,
        video_info_dict: dict=None,
        basic_info_include: bool=False,
        uid: str=None,
        name: str=None,
        text: str=None,
        free: bool=None,
        owner: str=None,
        save_path: str=None,
        website: str=None,
        origin_url: str=None,
        download_url: str=None,
        resolution: str=None,
        duration: float=None,
        integrity: bool=False,
        md5: str=None,
        size: int=None,
        last_modified_datetime: str=None
    ):
        """
        Initializes a VideoData object, which stores information about a video file. This class can load video
        details from a dictionary or directly through parameters provided at initialization. It includes functionality
        to retrieve basic information about the video such as its path, website origin, URLs, resolution, duration, 
        integrity, size, and last modification time.

        Args:
            video_info_dict (dict, optional): 
                A dictionary containing video information. If provided, the object
                will be initialized with data from this dictionary.
            basic_info_include (bool, optional): 
                Indicates whether to include basic video information (duration, integrity, size, 
                and last modification time) from the video_info_dict or to retrieve it anew. 
            uid (str, optional): 
                The uid of the video.
            text (str, optional): 
                The text of the video.
            free (str, optional): 
                Wheter the video is free.
            owner (str, optional): 
                The owner of the video.
            name (str, optional): 
                The name of the video.
            save_path (str, optional): 
                The file path where the video is saved.
            website (str, optional): 
                The website from which the video was downloaded.
            origin_url (str, optional): 
                The original URL of the video.
            download_url (str, optional): 
                The URL used to download the video.
            resolution (str, optional): 
                The resolution of the video.
            duration (float, optional): 
                The duration of the video in seconds.
            integrity (bool, optional): 
                Indicates whether the video file is considered to be intact and playable.
            md5 (str, optional): 
                The md5 of the video.                   
            size (int, optional): 
                The size of the video file in bytes.
            last_modified_datetime (str, optional): 
                The last modified date and time of the video file as a formatted string.
        """
        if video_info_dict is not None:
            self.load_info_from_dict(
                video_info_dict=video_info_dict,
                basic_info_include=basic_info_include
            )
        else:
            self.uid = uid
            self.name = name
            self.text = text
            self.free = free
            self.owner = owner
            self.save_path = save_path
            self.website = website
            self.origin_url = origin_url
            self.download_url = download_url
            self.resolution = resolution
            self.duration = duration
            self.integrity = integrity
            self.md5 = md5
            self.size = size
            self.last_modified_datetime = last_modified_datetime
        
    def load_info_from_dict(
        self, 
        video_info_dict: dict, 
        basic_info_include: bool=False
    ) -> None:
        # download info
        self.uid = video_info_dict.get('uid')
        self.name = video_info_dict.get('name')
        self.text = video_info_dict.get('text')
        self.free = video_info_dict.get('free')
        self.owner = video_info_dict.get('owner')
        self.save_path = video_info_dict.get('save_path')
        self.website = video_info_dict.get('website')
        self.origin_url = video_info_dict.get('origin_url')
        self.download_url = video_info_dict.get('download_url')
        self.resolution = video_info_dict.get('resolution')

        # basic info
        if basic_info_include:
            record_lmd = video_info_dict['last_modified_datetime']
            current_lmd = self.get_modified_time()
            if record_lmd != current_lmd:
                self.last_modified_datetime = current_lmd
                self.duration, self.integrity = self.check_integrity()
                self.size = self.get_size()
                self.md5 = get_md5(self.save_path)
            else:
                self.last_modified_datetime = video_info_dict['last_modified_datetime']
                self.duration = video_info_dict['duration']
                self.integrity = video_info_dict['integrity']
                self.size = video_info_dict['size']
                self.md5 = video_info_dict['md5']
        else:
            self.last_modified_datetime = self.get_modified_time()
            self.duration, self.integrity = self.check_integrity()
            self.size = self.get_size()
            self.md5 = get_md5(self.save_path)
    
    def get_video_info_dict(self) -> dict:
        video_info_dict = {
            'uid': self.uid,
            'name': self.name,
            'text': self.text,
            'free': self.free,
            'owner': self.owner,
            'save_path': self.save_path,
            'website': self.website,
            'origin_url': self.origin_url,
            'download_url': self.download_url,
            'resolution': self.resolution,
            'duration': self.duration,
            'integrity': self.integrity,
            'md5': self.md5,
            'size': self.size,
            'last_modified_datetime': self.last_modified_datetime
        }
        return video_info_dict
    
    def get_size(self) -> int:
        size = os.path.getsize(self.save_path)
        size = size / 1024 / 1024
        return size
    
    def get_modified_time(self) -> str:
        # Get the last modified time in seconds since the epoch
        last_modified_timestamp = os.path.getmtime(self.save_path)
        # Convert the timestamp to a datetime object
        last_modified_datetime = datetime.fromtimestamp(last_modified_timestamp)
        # Format the datetime object as a string
        last_modified_time = last_modified_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return last_modified_time
    
    def check_integrity(self) -> Tuple[float, bool]:
        duration = cal_video_duration(self.save_path)
        integrity = check_video_integrity(self.save_path)
        return duration, integrity
    
    def __repr__(self) -> str:
        f"{self.__class__.__name__}({self.uid})"