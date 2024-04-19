import os
import shutil
import traceback
from tqdm import tqdm
from bs4 import BeautifulSoup
from openvideo.video.base.data import VideoData
from openvideo.video.base.dataset import VideoDataset
from openvideo.utils.file_utils import download, get_md5
from openvideo.video.fetch.utils import download_view_source
from .uid import generate_mixkit_video_uid, CATEGORY_PAGE_NUM, CATEGORY_UID2, CATEGORY_UID


class MixkitVideoFetch(VideoDataset):
    def __init__(self, root_dir: str, clear_tmp: bool=True):
        super().__init__(
            website="mixkit", 
            root_dir=root_dir,
            clear_tmp=clear_tmp
        )
            
    def download(
        self, 
        platform: str="windows",
        restart: bool=False
    ):
        last_video_info = self.monitor.last_video
        if last_video_info == dict():
            restart = True
        if restart:
            for category, page_num in CATEGORY_PAGE_NUM.items():
                print(f"download the {category} with {page_num} pages")
                for page_idx in range(page_num):
                    self.download_with_category_page_idx(
                        category=category,
                        page_idx=page_idx+1,
                        start_idx=0,
                        platform=platform
                    ) 
        else:
            last_video_uid = last_video_info['uid']
            category_idx = last_video_uid[2:4]
            category_idx_int = int(category_idx)
            last_category = CATEGORY_UID2[category_idx]
            last_page_idx = int(last_video_uid[4:6])
            last_inner_idx = int(last_video_uid[6:8])
            message = f"Starting from category({last_category}), page_idx({last_page_idx}), "
            message += f"idx({last_inner_idx})..."
            print(message)
            for category, page_num in CATEGORY_PAGE_NUM.items():
                cur_category_idx_int = int(CATEGORY_UID[category])
                if cur_category_idx_int < category_idx_int:
                    continue
                print(f"download the {category} with {page_num} pages")
                for page_idx in range(page_num):
                    if cur_category_idx_int == category_idx_int:
                        if page_idx+1 < last_page_idx:
                            continue
                    self.download_with_category_page_idx(
                        category=category,
                        page_idx=page_idx+1,
                        start_idx=last_inner_idx if cur_category_idx_int == category_idx_int else 0,
                        platform=platform
                    )

    def download_with_category_page_idx(
        self,
        category: str, 
        page_idx: int,
        start_idx: int,
        platform: str,
    ):
        # download view source
        fetch_page_url = f"https://mixkit.co/free-stock-video/{category}/?page={page_idx}"
        view_source_download_path = os.path.join(self.cache_dir, f"{category}_{page_idx}.html")
        if not os.path.exists(view_source_download_path):
            download_view_source(
                website="mixkit",
                url=fetch_page_url,
                save_path=view_source_download_path,
                platform=platform
            )
        
        # read data from html
        with open(view_source_download_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        # unprocess download url
        html_unprocess_download_urls = soup.find_all(class_="item-grid-video-player__video-wrapper")
        unprocess_download_urls = [video.find('video')['src'] for video in html_unprocess_download_urls]
        # text and origin url
        html_origin_urls = soup.find_all(class_="item-grid-card__title")
        origin_urls = ["https://mixkit.co" + video.find('a')['href'] for video in html_origin_urls]
        
        for idx, unprocess_download_url in tqdm(enumerate(unprocess_download_urls), 
                                                desc=f"Download Page {page_idx}"):
            if idx < start_idx:
                continue
            # download the origin page's view source
            origin_url = origin_urls[idx]
            origin_url_download_path = os.path.join(self.cache_dir, f"{category}_{page_idx}_{idx}.html")
            try:
                self.download_video(
                    origin_url=origin_url,
                    origin_url_download_path=origin_url_download_path,
                    unprocess_download_url=unprocess_download_url,
                    category=category,
                    page_idx=page_idx,
                    idx=idx,
                    platform=platform
                )
            except Exception as e:
                error_message = traceback.format_exc()
                self.log_error(error_message)
            
    def download_video(
        self, 
        origin_url: str,
        origin_url_download_path: str, 
        unprocess_download_url: str,
        category: str, 
        page_idx: int, 
        idx: int, 
        platform: str
    ):
        if not os.path.exists(origin_url_download_path):
            download_view_source(
                website="mixkit",
                url=origin_url,
                save_path=origin_url_download_path,
                platform=platform
            )
        # read data from html
        with open(origin_url_download_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        owner = soup.find(class_="item-page__contributor-link")['href'][1: -1]    
        name = soup.find(class_="item-page__title").text
        try:
            text = soup.find(class_="item-page__description").text
        except:
            text = None
        highest_str_resolution = soup.find_all(class_="video-item__download-label")[-1].text
        resolution = '4k' if '4K' in highest_str_resolution else '1080p'
        
        # process the unprocess_download_url
        download_url = unprocess_download_url.replace("/preview/", "/download/")
        if resolution == '4k':
            download_url = download_url.replace("-small", "-4k")
        else:
            download_url = download_url.replace("-small", "-1080")

        # check if is downloaded sucessfully 
        if download_url in self.monitor.downloaded_url_list:
            return
        
        # download
        tmp_filename =  f"{category}_{page_idx}_{idx}_tmp.mp4"
        tmp_download_path = os.path.join(self.tmp_dir, tmp_filename)
        download_success = self.download_one_instance(
            download_url=download_url,
            download_path=tmp_download_path
        )
        if not download_success:
            error_message = f"error occurred when the download url is {download_url}"
            self.log_error(error_message)
            self.clear_tmpfile(tmp_download_path)
            return
        
        # if download sucessfully, check the md5
        # if md5 already exists, change the download url
        # then re-download the file and get md5 again
        md5 = get_md5(tmp_download_path)
        if md5 in self.monitor.md5_list:
            self.clear_tmpfile(tmp_download_path)
            error_message = f"A video with the same md5 code ({md5}) already exists, download_url: {download_url}"
            self.log_error(error_message)
            download_url = unprocess_download_url.replace("/preview/", "/download/")
            download_url = download_url.replace("-small", "")
            download_success = self.download_one_instance(
                download_url=download_url,
                download_path=tmp_download_path
            )
            if not download_success:
                error_message = f"error occurred when the download url is {download_url}"
                self.log_error(error_message)
            md5 = get_md5(tmp_download_path)
            if md5 in self.monitor.md5_list:
                error_message = f"A video with the same md5 code ({md5}) already exists, download_url: {download_url}"
                self.log_error(error_message)
                self.clear_tmpfile(tmp_download_path)
                return
        
        # record the info of video
        uid = generate_mixkit_video_uid(
            category=category,
            page_idx=page_idx,
            inner_idx=idx,
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
    
    def clear_tmpfile(self, tmp_download_path: str):
        if os.path.exists(tmp_download_path):
            os.remove(tmp_download_path)
    
    def download_one_instance(
        self, 
        download_url: str, 
        download_path: str
    ):
        download_success = True
        try:
            download(download_path, download_url)
        except:
            download_success = False
            error_message = f"error occurred when the download url is {download_url}"
            self.log_error(error_message)
        return download_success   
            