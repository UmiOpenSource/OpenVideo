from openvideo.video.base.uid import WEBSITE_UID


def generate_pixabay_video_uid(
    page_idx: int,
    inner_idx: int,
    origin_idx: int,
    md5: str
) -> str:
    website_uid = WEBSITE_UID["pixabay"] # 2
    page_uid = "{:02d}".format(page_idx)  # 2
    inner_uid = "{:02d}".format(inner_idx)  # 2
    origin_uid = "{:06d}".format(int(origin_idx))  # 6
    md5_uid = md5[:4] # 4
    video_uid = website_uid + page_uid + inner_uid + origin_uid + md5_uid # 16
    return video_uid
