from scenedetect import detect, ContentDetector
from tqdm import tqdm
import cv2
import os, re, json, argparse
from tqdm import tqdm


import random
import math
from glob import glob
from multiprocessing import  Process
from multiprocessing import cpu_count


def cutscene_detection(video_path, cutscene_threshold=27, max_cutscene_len=10):
    # scene_list = detect(video_path, ContentDetector(threshold=cutscene_threshold, min_scene_len=15), start_in_scene=True)
    scene_list = detect(video_path, ContentDetector(threshold=cutscene_threshold, min_scene_len=15),
                        show_progress=False)

    end_frame_idx = [0]

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

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

def cutscenes(videos_input,cutscene_threshold,max_cutscene_len,output_json_file,sub_list):

    for dir in sub_list:
        video_cutscenes = {}
        output_json_file = os.path.join(videos_input,dir,output_json_file)
        for video_path in tqdm(os.listdir(os.path.join(videos_input,dir))):
            video_path = os.path.join(videos_input,dir,video_path)
            cutscenes_raw = cutscene_detection(video_path, cutscene_threshold, max_cutscene_len)
            video_cutscenes[video_path.split("/")[-1]] = cutscenes_raw

        write_json_file(video_cutscenes, output_json_file)
        print("dir: ",dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cutscene Detection")
    parser.add_argument("--videos_input", type=str, default=r'/mnt/data2/data/deep1/xcp/pexels-video')
    parser.add_argument("--cutscene_threshold", type=int, default=25)
    parser.add_argument("--max_cutscene_len", type=int, default=5)
    parser.add_argument("--output_json_file", type=str, default="cutscene_frame_idx.json")
    args = parser.parse_args()

    data_list = os.listdir(args.videos_input)
    n_processes = cpu_count()

    # cutscenes(args.videos_input,
    #           args.cutscene_threshold,
    #           args.max_cutscene_len,
    #           args.output_json_file,
    #           data_list)

    processes_list = []
    for n in range(n_processes):
        size = math.ceil(len(data_list) / n_processes)
        sub_list = data_list[n * size: min((n + 1) * size, len(data_list))]

        processes_list.append(Process(target=cutscenes, \
                                      args=(args.videos_input, \
                                            args.cutscene_threshold, \
                                            args.max_cutscene_len, \
                                            args.output_json_file,\
                                            sub_list)))
    for p in processes_list:
        p.start()
