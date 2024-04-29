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

def encode_parquet_file(input_root,output_root,sub_list):

    for parquet_path in sub_list:
        folder = pathlib.Path(parquet_path).stem
        parquet_path = os.path.join(input_root,parquet_path)
        # folder = os.path.basename(parquet_path).split('.')[0]
        parquet_file = pq.ParquetFile(parquet_path)
        for batch in tqdm(parquet_file.iter_batches(batch_size=1)):
            try:
                df = batch.to_pandas()
                id = df['id'][0]
                video = df['video'][0]
                md5 = hashlib.md5(video).hexdigest()

                info = {}
                info.update({"id":str(df['id'][0])})
                info.update({"md5":str(md5)})
                info.update({"tags":str(df['tags'][0])})
                info.update({"width":str(df['width'][0])})
                info.update({"height":str(df['height'][0])})
                info.update({"fps":str(df['fps'][0])})
                info.update({"url":str(df['url'][0])})

                os.makedirs(os.path.join(output_root, folder,id+'_'+md5), exist_ok=True)
                with open(os.path.join(output_root, folder,id+'_'+md5, "info.json"), "w", encoding='utf-8') as f:  ## 设置'utf-8'编码
                    json.dump(info, f, indent=2, sort_keys=True, ensure_ascii=False)

                os.makedirs(os.path.join(output_root,folder),exist_ok=True)
                fn = osp.join(output_root, folder, id+'_'+md5) +".mp4"
                with open(fn, 'wb') as f:
                    fc = f.write(video)
            except Exception as e:
                print("parquet_file: ",str(e))
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="encode parquet files ")
    parser.add_argument("--parquets_input", type=str,
                        # default=r"/mnt/data2/data/deep1/xcp/pexels/data",
                        default= r"E:\pexels",
                        help='parquet input dir')
    parser.add_argument("--videos_output", type=str,
                        # default=r'/mnt/data2/data/deep1/xcp/pexels-video',
                        default=r"E:\pexels-video",
                        help="video ouput dir")
    args = parser.parse_args()

    assert (os.path.exists(args.parquets_input) == True)
    # if os.path.exists(args.videos_output) == True:
    #     shutil.rmtree(args.videos_output,ignore_errors=True)

    data_list = os.listdir(args.parquets_input)
    data_list = sorted(data_list)
    print(data_list)
    n_processes = 4

    for folder in sorted(os.listdir(args.videos_output)):
        str1 = "------------folder: " + str(folder) + " " + str(len(os.listdir(os.path.join(args.videos_output, folder))))
        print(str1)


    # encode_parquet_file(args.parquets_input, args.videos_output,data_list)

    processes_list = []
    for n in range(n_processes):
        size = math.ceil(len(data_list) / n_processes)
        sub_list = data_list[n * size: min((n + 1) * size, len(data_list))]

        processes_list.append(Process(target=encode_parquet_file, \
                                      args=(args.parquets_input, \
                                            args.videos_output,\
                                            sub_list)))
    for p in processes_list:
        p.start()
        # p.join()