from openvideo.video.base.uid import WEBSITE_UID


def generate_pexels_video_uid(
    page_idx: int,
    origin_idx: int,
    md5: str
) -> str:
    website_uid = WEBSITE_UID["pexels"] # 2
    page_uid = "{:02d}".format(page_idx)  # 2
    origin_uid = "{:08d}".format(int(origin_idx))  # 8
    md5_uid = md5[:4] # 4
    video_uid = website_uid + origin_uid + page_uid + md5_uid # 16
    return video_uid
    