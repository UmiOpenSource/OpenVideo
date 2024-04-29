import hashlib
import os
import os.path as osp
import shutil
from glob import glob
import pathlib
import pyarrow.parquet as pq
from tqdm import tqdm
import os, re, json, argparse

import random
import math
from multiprocessing import  Process
from multiprocessing import cpu_count

def encode_parquet_file_pro(parquets_input,videos_dirs,sub_list):

    for parquet_path in sub_list:
        folder = pathlib.Path(parquet_path).stem
        parquet_path = os.path.join(parquets_input,parquet_path)
        parquet_file = pq.ParquetFile(parquet_path)
        for batch in tqdm(parquet_file.iter_batches(batch_size=1)):
            try:
                df = batch.to_pandas()
                id = df['id'][0]
                video = df['video'][0]
                md5 = hashlib.md5(video).hexdigest()

                info = {}
                info.update({"id":df['id'][0]})
                info.update({"md5":str(md5)})
                info.update({"tags":str(df['tags'][0])})
                info.update({"width":int(df['width'][0])})
                info.update({"height":int(df['height'][0])})
                info.update({"fps":int(df['fps'][0])})
                info.update({"url":str(df['url'][0])})

                os.makedirs(os.path.join(videos_dirs, folder,id+'_'+md5), exist_ok=True)
                with open(os.path.join(videos_dirs, folder,id+'_'+md5, "info.json"), "w", encoding='utf-8') as f:  ## 设置'utf-8'编码
                    json.dump(info, f, indent=2, sort_keys=True, ensure_ascii=False)

                os.makedirs(os.path.join(videos_dirs,folder),exist_ok=True)
                fn = osp.join(videos_dirs, folder, id+'_'+md5) +".mp4"
                with open(fn, 'wb') as f:
                    fc = f.write(video)
            except Exception as e:
                print("parquet_file: ",str(e))
                continue

def encode_parquet_file2(parquets_input,videos_dirs):
    assert (os.path.exists(parquets_input) == True)
    os.makedirs(videos_dirs,exist_ok=True)

    # if os.path.exists(args.videos_output) == True:
    #     shutil.rmtree(args.videos_output,ignore_errors=True)

    data_list = os.listdir(parquets_input)
    data_list = sorted(data_list)
    print(data_list)
    n_processes = 1

    # encode_parquet_file(args.parquets_input, args.videos_output,data_list)

    processes_list = []
    for n in range(n_processes):
        size = math.ceil(len(data_list) / n_processes)
        sub_list = data_list[n * size: min((n + 1) * size, len(data_list))]

        processes_list.append(Process(target=encode_parquet_file_pro, \
                                      args=(parquets_input, \
                                            videos_dirs, \
                                            sub_list)))
    for p in processes_list:
        p.start()
    for p in processes_list:
        p.join()

    for folder in sorted(os.listdir(videos_dirs)):
        str1 = "folder: " + str(folder) + " : " + str(
            len(glob(os.path.join(videos_dirs,folder,'*.mp4'))))

        print(str1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="encode parquet files ")
    parser.add_argument("--parquets_input", type=str,
                        # default=r"/mnt/data2/data/deep1/xcp/pexels/data",
                        default= r"E:\pexels",
                        help='parquet input dir')
    parser.add_argument("--videos_dirs", type=str,
                        # default=r'/mnt/data2/data/deep1/xcp/pexels-video',
                        default=r"E:\pexels-video",
                        help="videos_dirs dir")
    args = parser.parse_args()

    encode_parquet_file2(args.parquets_input, args.videos_dirs)