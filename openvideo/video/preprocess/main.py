# import logging
# from modelscope.utils.logger import get_logger
# logger = get_logger(log_level=logging.ERROR)

import os, sys, re, json, argparse

from PreProcess import *
from SceneSplitting import *
from KeyFrame import *
# from OpticalFlow import *
from utils import *



def video_clean_pipline(videos_dirs,cutscene_threshold,max_cutscene_len,eventcut_threshold):
    print("video_quality_assessment")
    video_quality_assessment.video_quality_ass(videos_dirs)
    print("cutscene_detect.cutscenes")
    cutscene_detect.cutscenes(videos_dirs,cutscene_threshold,max_cutscene_len)
    event_stitching.event_stitching2(videos_dirs,eventcut_threshold)
    video_splitting.video_splitting2(videos_dirs)
    gen_keyframe_3frames.process_videos_parallel(videos_dirs)
    gen_keyframe_IFrame.process_videos_parallel(videos_dirs)

    # gen_keyframe_usediff.process_videos_parallel(videos_dirs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenVideo Clean")
    parser.add_argument("--videos_dirs", type=str,
                        default=r'Y:\deep1\xcp\pexels-video')
                        # default= r"/mnt/data2/data/deep1/xcp/pexels-video")

    parser.add_argument("--cutscene_threshold", type=int, default=25)
    parser.add_argument("--max_cutscene_len", type=int, default=5)
    parser.add_argument("--eventcut_threshold", type=float, default=0.6)
    args = parser.parse_args()

    # encode_parquet_file.encode_parquet_file2(args.parquets_input, args.videos_dirs)

    video_clean_pipline(args.videos_dirs,
                        args.cutscene_threshold,
                        args.max_cutscene_len,
                        args.eventcut_threshold)