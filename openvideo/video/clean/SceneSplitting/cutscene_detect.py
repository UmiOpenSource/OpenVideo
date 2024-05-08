from scenedetect import detect, ContentDetector
from tqdm import tqdm
import cv2
import os, re, json, argparse
from tqdm import tqdm
import pathlib

import random
import math
from glob import glob
import multiprocessing
from multiprocessing import cpu_count
from multiprocessing import  Process

def cutscene_detection(video_path, cutscene_threshold=27, max_cutscene_len=10):
    # scene_list = detect(video_path, ContentDetector(threshold=cutscene_threshold, min_scene_len=15), start_in_scene=True)
    scene_list = detect(video_path,
                        ContentDetector(threshold=cutscene_threshold, min_scene_len=15),
                        show_progress=False)

    end_frame_idx = [0]

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if len(scene_list) == 0:
        end_frame_idx.append(frame_count)
    else:
        for scene in scene_list:
            new_end_frame_idx = scene[1].get_frames()
            while (new_end_frame_idx-end_frame_idx[-1]) > (max_cutscene_len+2)*fps: # if no cutscene at min_scene_len+2, then cut at min_scene_len
                end_frame_idx.append(end_frame_idx[-1] + int(max_cutscene_len*fps))
            end_frame_idx.append(new_end_frame_idx)
    
    cutscenes =[]
    for i in range(len(end_frame_idx)-1):
        cutscenes.append([end_frame_idx[i], end_frame_idx[i+1]])

    return cutscenes

def write_json_file(data, output_file):
    data = json.dumps(data, indent = 4)
    def repl_func(match: re.Match):
        return " ".join(match.group().split())
    data = re.sub(r"(?<=\[)[^\[\]]+(?=])", repl_func, data)
    data = re.sub(r'\[\s+', '[', data)
    data = re.sub(r'],\s+\[', '], [', data)
    data = re.sub(r'\s+\]', ']', data)
    with open(output_file, "w") as f:
        f.write(data)

def cutscenes_pro(videos_input,cutscene_threshold,max_cutscene_len,cutscene_frame_idx,sub_list):

    for dir in sub_list:
        if os.path.exists(os.path.join(videos_input,dir,cutscene_frame_idx)) == True:
            continue

        print("dir:",dir,"\n")
        video_cutscenes = {}
        videos_path = glob(os.path.join(videos_input,dir,'*.mp4'))
        for video_path in tqdm(videos_path):
            try:
                cutscenes_raw = cutscene_detection(video_path, cutscene_threshold, max_cutscene_len)
                video_cutscenes[pathlib.Path(video_path).name] = cutscenes_raw
            except Exception as e:
                print(str(e))

        write_json_file(video_cutscenes, os.path.join(videos_input,dir,cutscene_frame_idx))
        print("dir: ",dir)

def cutscenes(videos_dirs,cutscene_threshold,max_cutscene_len):
    cutscene_frame_idx = "cutscene_frame_idx.json"
    data_list = os.listdir(videos_dirs)
    random.shuffle(data_list)

    # cutscenes_pro(videos_dirs,
    #               cutscene_threshold,
    #               max_cutscene_len,
    #               cutscene_frame_idx,
    #               data_list)

    n_processes = cpu_count()
    processes_list = []


    for n in range(n_processes):
        size = math.ceil(len(data_list) / n_processes)
        sub_list = data_list[n * size: min((n + 1) * size, len(data_list))]

        processes_list.append(Process(target=cutscenes_pro, \
                                      args=(videos_dirs, \
                                            cutscene_threshold, \
                                            max_cutscene_len, \
                                            cutscene_frame_idx,\
                                            sub_list)))
    for p in processes_list:
        p.start()
    for p in processes_list:
        p.join()

    print("----end")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cutscene Detection")
    parser.add_argument("--videos_dirs", type=str, default=r'E:\pexels-video')
    parser.add_argument("--cutscene_threshold", type=int, default=25)
    parser.add_argument("--max_cutscene_len", type=int, default=5)
    # parser.add_argument("--output_json_file", type=str, default="cutscene_frame_idx.json")
    args = parser.parse_args()

    cutscenes(args.videos_dirs,args.cutscene_threshold,args.max_cutscene_len)


