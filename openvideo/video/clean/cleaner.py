import os
import shutil
from tqdm import tqdm
from datetime import datetime
from .key_frame import extract_key_frames
from .scenes_split import split_video_into_scenes
from .evaluator import VideoEvaluator
from openvideo.utils.file_utils import get_md5
from openvideo.video.utils import check_video_integrity


class VideoCleaner:
    def __init__(
        self, 
        src_dir: str, 
        out_dir: str,
        log_path: str=None,
        video_min_time: str=5.0,
        video_max_time: str=60.0,
        split_threshold: int=27.0,
        blur_detect: bool=True,
        blur_threshold: float=500.0
    ):
        self.src_dir = src_dir
        self.out_dir = out_dir
        self.video_min_time = video_min_time
        self.video_max_time = video_max_time
        self.split_threshold = split_threshold
        self.blur_detect = blur_detect
        self.blur_threshold = blur_threshold
        
        # logger
        if log_path is None:
            log_path = os.path.join(out_dir, "log.txt")
        self.log_path = log_path
        
        # makedirs
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        # video path
        self.src_video_path_list = list()
        videos = os.listdir(src_dir)
        for video_name in videos:
            video_path = os.path.join(src_dir, video_name)
            self.src_video_path_list.append(video_path)
        
    def clean(self):
        for video_path in tqdm(self.src_video_path_list):
            # check integrity
            if check_video_integrity(video_path) == False:
                message = f"The video {video_path} is not complete."
                self.log_error(message)
                continue
            
            # video name/path
            video_name = os.path.basename(video_path)
            video_name: str
            video_name = video_name.replace(".mp4", "")
            save_dir = os.path.join(self.out_dir, video_name)
       
            # split
            split_video_into_scenes(
                video_path=video_path,
                save_dir=save_dir,
                min_time=self.video_min_time,
                max_time=self.video_max_time,
                threshold=self.split_threshold
            )
            
            # extract key frames
            split_videos = os.listdir(save_dir)
            for split_video_name in split_videos:
                if not split_video_name.endswith(".mp4"):
                    continue
                split_video_path = os.path.join(save_dir, split_video_name)
                md5 = get_md5(split_video_path)
                split_save_dir = os.path.join(save_dir, md5)
                extract_key_frames(
                    video_path=split_video_path,
                    save_dir=split_save_dir,
                    filename=md5
                )
                rename_path = os.path.join(save_dir, md5+".mp4")
                os.rename(src=split_video_path, dst=rename_path)
    
                if self.blur_detect:
                    eval = VideoEvaluator(
                        video_path=rename_path, 
                        key_frames_dir=split_save_dir
                    )
                    avg_vars = eval.blurry_evaluate()
                    if avg_vars < self.blur_threshold:
                        message = f"Remove: {split_save_dir} with avg_vars({avg_vars})."
                        self.log_error(message)
                        shutil.rmtree(split_save_dir)
                        os.remove(rename_path)
    
    def log_error(self, error_message: str):
        cur_time = str(datetime.now())
        error_message = f"{cur_time}: {error_message}\n"
        with open(self.log_path, "a") as log_file:
            log_file.write(error_message)