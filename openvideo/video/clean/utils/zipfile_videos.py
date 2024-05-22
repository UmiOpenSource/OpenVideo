
import os, argparse
import zipfile
from tqdm import tqdm

import random
import math
from multiprocessing import  Process
from multiprocessing import cpu_count
import pathlib

def dfs_get_zip_file(input_path,result):

    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(os.path.join(input_path,file)):
            dfs_get_zip_file(os.path.join(input_path,file),result)
        else:
            if pathlib.Path(file).suffix == ".mp4":
                continue
            result.append(os.path.join(input_path,file))

def zip_file_prp(videos_dirs,zip_output,sub_list):
    for dir in sub_list:

        print("dir :",dir)
        zipfilename = str(dir)+".zip"

        filelists = []
        dfs_get_zip_file(os.path.join(videos_dirs,dir), filelists)

        f = zipfile.ZipFile(os.path.join(zip_output,zipfilename), 'w', zipfile.ZIP_DEFLATED)
        for file in tqdm(filelists):
            fpath = file.replace(videos_dirs, '')
            f.write(file,fpath)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tar video files ")

    parser.add_argument("--videos_dirs", type=str,
                        default=r'/mnt/data2/data/deep1/xcp/pexels-clean',
                        # default=r"Y:\deep1\xcp\test",
                        help="videos_dirs dir")

    parser.add_argument("--zip_output", type=str,
                        default=r"/mnt/data2/data/deep1/xcp/pexels-clean-zip",
                        # default= r"Y:\deep1\xcp\test_output",
                        help='parquet input dir')

    args = parser.parse_args()

    import multiprocessing
    multiprocessing.set_start_method('spawn')

    os.makedirs(args.zip_output,exist_ok=True)

    data_list = os.listdir(args.videos_dirs)

    # zip_file_prp(args.videos_dirs,args.zip_output,data_list)

    n_processes = cpu_count()

    processes_list = []
    for n in range(n_processes):
        size = math.ceil(len(data_list) / n_processes)
        sub_list = data_list[n * size: min((n + 1) * size, len(data_list))]

        processes_list.append(Process(target=zip_file_prp, \
                                      args=(args.videos_dirs, \
                                            args.zip_output, \
                                            sub_list)))
    for p in processes_list:
        p.start()
    for p in processes_list:
        p.join()

    for file in sorted(os.listdir(args.zip_output)):
        print(file,"\n")





