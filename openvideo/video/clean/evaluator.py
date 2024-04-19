import os
import cv2
import numpy as np
from openvideo.utils.file_utils import get_md5
from .key_frame import extract_key_frames


class VideoEvaluator:
    def __init__(self, video_path: str, key_frames_dir: str = None):
        self.video_path = video_path
        self.video_dir = os.path.dirname(video_path)
        
        # key frames
        if key_frames_dir is None:
            md5 = get_md5(video_path)
            key_frames_dir = os.path.join(self.video_dir, md5)
            extract_key_frames(
                video_path=video_path,
                save_dir=key_frames_dir,
                filename=md5
            )
        self.key_frames_dir = key_frames_dir  
        key_frames = os.listdir(self.key_frames_dir)
        self.key_frame_paths_list = list()
        for key_frame in key_frames:
            key_frame_path = os.path.join(self.key_frames_dir, key_frame)
            self.key_frame_paths_list.append(key_frame_path)
        
    def blurry_evaluate(self):
        laplace_vars = list()
        for key_frame_path in self.key_frame_paths_list:
            image = cv2.imread(key_frame_path)
            image = cv2.resize(image, dsize=(224, 224))
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_var = cv2.Laplacian(image_gray, cv2.CV_64F).var()
            laplace_vars.append(image_var)
        avg_lv = np.average(laplace_vars)
        return avg_lv