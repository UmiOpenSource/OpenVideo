
import cv2
from multiprocessing import Pool
from collections import defaultdict
import os, sys, re, json, argparse
from datetime import datetime, timedelta
from pytz import timezone
from tqdm import tqdm
import numpy as np

import random
import pathlib
import math
from glob import glob
from multiprocessing import  Process
from multiprocessing import cpu_count

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from modelscope.models import Model

import subprocess

def extract_frames(input_file: str, output_dir: str):
    """
    使用FFmpeg每隔一秒从视频中提取关键帧并以时间命名保存。

    参数：
    input_file: 输入视频文件路径。
    output_dir: 输出关键帧的目录。
    """

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 构建FFmpeg命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'fps=1',
        '-vsync', '0',
        f'{output_dir}/frame-%03d.jpg'
    ]
    subprocess.run(ffmpeg_cmd)

def video_quality_ass(videos_dirs):
    #download from https://www.modelscope.cn/models/iic/cv_man_image-quality-assessment/summary
    model = Model.from_pretrained('PreProcess/cv_man_image-quality-assessment')
    image_quality_assessment_pipeline = pipeline(Tasks.image_quality_assessment_mos, model=model,device='gpu')

    for dir in os.listdir(videos_dirs):
        videos_path = glob(os.path.join(videos_dirs,dir,"*.mp4"))

        for video_path in tqdm(videos_path):
            folder = pathlib.Path(video_path).stem

            info = {}
            with open(os.path.join(videos_dirs,dir,folder,"info.json"),'r', encoding='utf-8') as f:
                info = json.load(f)

                cap = cv2.VideoCapture(video_path)
                ret, frame = cap.read()
                if ret:
                    img = cv2.resize(frame,(224,224))
                    img_file = os.path.join(videos_dirs,dir,folder,"temp.jpg")
                    cv2.imwrite(img_file,img)
                    re_score = image_quality_assessment_pipeline(img_file)[OutputKeys.SCORE]
                    info.update({"video_quality_score": re_score * 100})
                    os.remove(img_file)

            with open(os.path.join(videos_dirs,dir,folder,"info.json"), "w", encoding='utf-8') as f:
                json.dump(info, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Quality Assessment")
    parser.add_argument("--videos_dirs", type=str, default=r'E:\pexels-video')
    args = parser.parse_args()

    video_quality_ass(args.videos_dirs)