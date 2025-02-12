import pandas as pd
from tqdm import tqdm
import os, re, glob
import argparse


def decode_parquet_files(parquet_dir, save_dir):

    parquet_files = glob.glob(os.path.join(parquet_dir, '*.parquet'))

    for parquet_file in tqdm(parquet_files):
        # get subdir name in parquet file
        subdir_name = os.path.splitext(os.path.basename(parquet_file))[0]
        output_dir = os.path.join(save_dir, subdir_name)
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"file name: {parquet_file}")
        
        try:
            df = pd.read_parquet(parquet_file)

            for index, row in df.iterrows():
                file_id = row['id']
                # text normalization
                file_id = re.sub(r'[<>:"/\\|?*]', '_', file_id)
                text_content = row['text']
                video_content = row['video']
                # print(f"Processing file_id: {file_id}")
                # print(f"type(text_content): {type(text_content)}")

                if isinstance(text_content, bytes):
                    try:
                        # decode text 
                        text_content_str = text_content.decode('utf-8')
                    except UnicodeDecodeError:
                        # if failed, replace error chars 
                        text_content_str = text_content.decode('utf-8', errors='replace')
                        print(f"{UnicodeDecodeError} in {file_id}.txt")
                else:
                    text_content_str = text_content 

                # save text
                text_filename = f"{file_id}.txt"
                text_path = os.path.join(output_dir, text_filename)
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text_content_str)
                # print(f'save text: {text_path}')

                # save video
                video_filename = f"{file_id}.mp4"
                video_path = os.path.join(output_dir, video_filename)
                with open(video_path, 'wb') as f:
                    f.write(video_content)
                # print(f'save video: {video_path}')
                
        except Exception as e:
            print(f"Error in {parquet_file}: {str(e)}")
            continue

    print("finished!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="decode parquet files ")
    parser.add_argument("--parquet_dir", type=str,
                        default=r"./pexels/data",
                        help='parquet input dir')

    parser.add_argument("--save_dir", type=str,
                        default=r"./pexels-video",
                        help="videos save dir")
    args = parser.parse_args()

    decode_parquet_files(args.parquet_dir, args.save_dir)

