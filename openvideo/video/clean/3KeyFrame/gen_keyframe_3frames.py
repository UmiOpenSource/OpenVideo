import cv2
import os
import argparse
import multiprocessing
from multiprocessing import cpu_count
from itertools import repeat
from tqdm import tqdm

def extract_keyframes(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract and save the first frame
    ret, first_frame = cap.read()
    if ret:
        keyframe_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_keyframe_first.jpg"
        first_frame_path = os.path.join(output_dir, keyframe_name)
        cv2.imwrite(first_frame_path, first_frame)

    # Extract and save the middle frame (rounded down if odd count)
    middle_frame_index = frame_count // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_index)
    ret, middle_frame = cap.read()
    if ret:
        keyframe_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_keyframe_middle.jpg"
        middle_frame_path = os.path.join(output_dir, keyframe_name)
        cv2.imwrite(middle_frame_path, middle_frame)

    # Reset to the beginning and extract the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    cap.read()  # Skip first frame as we already have it
    for _ in range(frame_count - 2):  # Skip all frames until the last one
        cap.read()

    ret, last_frame = cap.read()
    if ret:
        keyframe_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_keyframe_end.jpg"
        last_frame_path = os.path.join(output_dir, keyframe_name)
        cv2.imwrite(last_frame_path, last_frame)

    cap.release()

def get_video_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.mp4', '.avi', '.mkv'))]

def process_videos_parallel(directory, output_base_dir):
    video_files = get_video_files(directory)

    num_processes = cpu_count()
    with multiprocessing.Pool(num_processes) as pool:
        with tqdm(total=len(video_files), desc='Extracting Keyframes') as pbar:
            for _ in pool.imap_unordered(extract_keyframes_with_progress_update, zip(video_files, repeat(output_base_dir))):
                pbar.update(1)

def extract_keyframes_with_progress_update(args):
    video_path, output_base_dir = args
    output_dir = os.path.join(output_base_dir, os.path.splitext(os.path.basename(video_path))[0])
    try:
        extract_keyframes(video_path, output_dir)
        return True  # Indicate success for tqdm update
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        return False  # Indicate failure for tqdm update (not used here, but could be useful for logging)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate keyframe use diff")
    parser.add_argument("--input_video_dir", type=str, default=r'pexels-video')
    parser.add_argument("--output_keyframe_dir", type=str, default=r'pexels-video-keyframe')
    args = parser.parse_args()
    process_videos_parallel(args.input_video_dir, args.output_keyframe_dir)
    
# Usage:
# python gen_keyframe_3frames.py --input_video_dir input_video_dir --output_keyframe_dir output_keyframe_dir

