# Extracting Keyframes from Videos
The section includes the code of three algorithms for extracting keyframes from videos
.

## Method 1: Use frame diff
```
python gen_keyframe_usediff.py --input_video_dir input_video_dir --output_keyframe_dir output_keyframe_dir
```

## Method 2: Use first, middle, and last frame as keyframes
```
python gen_keyframe_3frames.py --input_video_dir input_video_dir --output_keyframe_dir output_keyframe_dir
```

## Method 3: Use IFrame
```
python gen_keyframe_IFrame.py --input_video_dir input_video_dir --output_keyframe_dir output_keyframe_dir
```