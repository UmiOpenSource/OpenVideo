import os
import shutil
from openvideo.video.utils import cal_video_duration
from scenedetect import open_video, SceneManager, split_video_ffmpeg
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg


def split_video_into_scenes(
    video_path: str,
    save_dir: str,
    min_time: str = 5.0,
    max_time: str = 60.0,
    threshold: int = 27.0,
):
    # Open our video, create a scene manager, and add a detector.
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))
    scene_manager.detect_scenes(video, show_progress=True)
    scene_list = scene_manager.get_scene_list()
    
    # make dirs
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # split video
    split_video_ffmpeg(
        input_video_path=video_path, 
        scene_list=scene_list, 
        output_dir=save_dir, 
        show_progress=True
    )

    # check if the split videos is empty
    split_videos = os.listdir(save_dir)
    if split_videos == []:
        video_name = os.path.basename(video_path)
        shutil.copy(src=video_path, dst=os.path.join(save_dir, video_name))
        split_videos = os.listdir(save_dir)
    
    # filter
    for split_video_name in split_videos:
        if not split_video_name.endswith(".mp4"):
            continue
        split_video_path = os.path.join(save_dir, split_video_name)
        duration = cal_video_duration(split_video_path)
        if duration < min_time or duration > max_time:
            os.remove(split_video_path)