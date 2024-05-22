import os, json, argparse
import shutil
from datetime import datetime
import subprocess
from tqdm import tqdm
from glob import glob
import pathlib
import math
from multiprocessing import Process
from multiprocessing import cpu_count

def video_splitting_pro(videos_dirs,event_timecode,sub_list):

    for dir in sub_list:
        if os.path.exists(os.path.join(videos_dirs, dir, event_timecode)) == False:
            print("no file:",os.path.join(videos_dirs, dir, event_timecode))
            continue

        f = open(os.path.join(videos_dirs, dir, event_timecode))
        video_timecodes = json.load(f)

        print("start dir: ", dir)

        # os.makedirs(output_folder, exist_ok=True)

        for video_path in tqdm(glob(os.path.join(videos_dirs,dir, "*.mp4"))):
            try:
                video_name = pathlib.Path(video_path).stem
                folder = pathlib.Path(video_path).stem

                # print("video_name ",video_name)
                timecodes = video_timecodes[pathlib.Path(video_path).name]

                if len(timecodes) == 1:
                    if os.path.exists(os.path.join(videos_dirs,dir,folder,video_name+"_0.mp4")) == True:
                        os.remove(os.path.join(videos_dirs,dir,folder,video_name+"_0.mp4"))

                    shutil.copyfile(video_path,os.path.join(videos_dirs,dir,folder,video_name+"_0.mp4"))
                else:

                    for i, timecode in enumerate(timecodes):
                        start_time = datetime.strptime(timecode[0], '%H:%M:%S.%f')
                        end_time = datetime.strptime(timecode[1], '%H:%M:%S.%f')
                        video_duration = (end_time - start_time).total_seconds()
                        if os.path.exists(os.path.join(videos_dirs,dir,folder,video_name+"_%i.mp4"%i)) == True:
                            os.remove(os.path.join(videos_dirs,dir,folder,video_name+"_%i.mp4"%i))

                        # ffmpg linux 编译按照 https://publit.io/community/blog/ffmpeg-with-cuda-and-gpu-accelerated-video-conversion
                        os.system(
                            "ffmpeg -hide_banner -loglevel panic  -ss %s -t %.3f  -i %s  %s" % (timecode[0],
                                                                                                              video_duration,
                                                                                                              video_path,
                                                                                                              os.path.join(
                                                                                                                  videos_dirs,
                                                                                                                  dir,
                                                                                                                  folder,
                                                                                                                  video_name + "_%i.mp4" % i)))

                        #ffmpeg window 编译按照 https://www.gyan.dev/ffmpeg/builds/
                        # os.system("ffmpeg -hide_banner -loglevel panic  -ss %s -t %.3f  -hwaccel cuda -i %s  %s"%(timecode[0],
                        #                                                                                  video_duration,
                        #                                                                                  video_path,
                        #                                                                                  os.path.join(videos_dirs,dir,folder,video_name+"_%i.mp4"%i)))
                        #
            except Exception as e:
                print(str(e))
                continue

        print("end dir: ", dir)


def video_splitting2(videos_dirs):
    event_timecode = "event_timecode.json"
    data_list = os.listdir(videos_dirs)
    n_processes = cpu_count()
    # n_processes = 10

    video_splitting_pro(videos_dirs, event_timecode, data_list)

    # processes_list = []
    # for n in range(n_processes):
    #     size = math.ceil(len(data_list) / n_processes)
    #     sub_list = data_list[n * size: min((n + 1) * size, len(data_list))]
    #
    #     processes_list.append(Process(target=video_splitting_pro, \
    #                                   args=(videos_dirs, \
    #                                         event_timecode, \
    #                                         sub_list)))
    # for p in processes_list:
    #     p.start()
    # for p in processes_list:
    #     p.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Event Stitching")
    parser.add_argument("--videos_dirs", type=str, default=r'E:\pexels-video')
    # parser.add_argument("--event_timecode", type=str, default='event_timecode.json')
    # parser.add_argument("--output_folder", type=str, default="E:\pexels-video-clip")
    args = parser.parse_args()

    video_splitting2(args.videos_dirs)




