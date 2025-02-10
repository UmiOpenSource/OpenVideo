<h1 align="center">
<img src="docs/assets/openvideo-logo2.png" width="600">
</h1><br>

<div>
    <a href="https://huggingface.co/OpenVideo"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-OpenVideo-yellow"></a>
    <a href="https://www.modelscope.cn/organization/OpenVideo"><img src="https://img.shields.io/badge/ModelScope-OpenVideo-blue"></a>
    <a href="https://openxlab.org.cn/usercenter/UmiMarch"><img src="https://cdn-static.openxlab.org.cn/app-center/openxlab_app.svg"></a>
    <a href="https://wisemodel.cn/organization/OpenVideo"><img src="https://img.shields.io/badge/WiseModel-OpenVideo-purple"></a>
    <a href="https://www.twitter.com/UmiOpenVideo"><img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/UmiOpenVideo"></a>
</div>

[![PyPi version](https://badgen.net/pypi/v/openvideo/)](https://pypi.org/pypi/openvideo/)
[![PyPI pyversions](https://img.shields.io/badge/dynamic/json?color=blue&label=python&query=info.requires_python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdata4co%2Fjson)](https://pypi.python.org/pypi/openvideo/) 
[![Downloads](https://static.pepy.tech/badge/openvideo)](https://pepy.tech/project/openvideo)
[![GitHub stars](https://img.shields.io/github/stars/UmiMarch/OpenVideo.svg?style=social&label=Star&maxAge=8640)](https://GitHub.com/UmiMarch/OpenVideo/stargazers/)

OpenVideo专注于文生视频领域，旨在为全球的AI研究者提供高质量、多样化的视频数据，并配套相应的数据收集、清洗、标注工具，为人工智能产业的发展提供助力。



## 🚀 里程碑
- **2024/06/30**: （要发布的内容）
- **2024/05/30**: 
- **2024/04/30**: 
- **2024/03/30**: 



## ⭐ 核心内容

### 高质量开源视频数据集


|   数据集   |   规格   |               类别               |           大小            |                    下载                    |
| :--------: | :------: | :------------------------------: | :-----------------------: | :----------------------------------------: |
| Pexels-Raw | 720p / ? | 简单描述一下视频数据集的覆盖范围 | 1250h / 200k+ clips / ?GB | [huggingface]()<br />[ModelScope]() <br /> |



### 人工精校标注

- 

### 数据处理工具包

- 

### 数据标注平台

-  

### 其它

- 




## ⚡快速开始

### 快速安装

您可以使用PyPI安装稳定版本，只需要在命令行输入以下命令:

```bash
$ pip install openvideo
```

或者通过Github获取最新版本:

```bash
$ pip install -U https://github.com/UmiMarch/OpenVideo/archive/master.zip # with --user for user install (no root)
```

``OpenVideo`` 依赖的包如下所示:

```
huggingface_hub>=0.22.2
tqdm>=4.66.1
wget>=3.2
requests>=2.31.0
aiohttp>=3.9.3
async_timeout>=4.0.3
moviepy>=1.0.3
opencv-python>=4.9.0.80
selenium>=4.19.0
scenedetect>=0.6.3
texttable>=1.7.0
bs4>=0.0.2
```

### 使用实例 —— 视频数据下载

* Mixkit [https://mixkit.co/free-stock-video/](https://mixkit.co/free-stock-video/)
```python
from openvideo.video.fetch import MixkitVideoFetch
 
mixkit_fetch = MixkitVideoFetch(root_dir="your/video/save/path")
mixkit_fetch.download_with_category_page_idx(
    category="sky", # 视频类型
    page_idx=1, # 从第几页开始下载
    start_idx=22, # 从第几个视频开始下载
    platform="linux" # 运行平台
)
```

* Pixabay [https://pixabay.com/zh](https://pixabay.com/zh)
```python
from openvideo.video.fetch import PixabayVideoFetch

pixabay = PixabayVideoFetch("your/video/save/path")
pixabay.download(
    chrome_exe_path=r"your/chrome/exe/path",
    username="your/pixabay/username",
    password="your/pixabay/password",
    headless=False,
    platform="windows" # 目前只支持windows
)
```

* Pexels [https://www.pexels.com/](https://www.pexels.com/)
```python
from openvideo.video.fetch import PexelsVdieoFetch, PexelsAPI

# 第一步，调用API获得视频链接
pexels_api = PexelsAPI(
    api="your/pexels/api", 
    save_path="pexels_api.npy"
)
pexels_api.fetch_api(
    start_page=1, # 起始页
    end_page=2, # 最终页
    save_api_dict_every_pages=1 # 每多少页保存一次
)

# 第二步，下载视频
pexels = PexelsVdieoFetch("pexels")
pexels.download(
    api_npy_save_path="pexels_api.npy", 
    chrome_exe_path=r"your/chrome/exe/path",
    headless=False
)
```

## 👨‍💻 贡献者

（提供帮助的开发者头像/主页）



## 🙏 致谢

（引用的其它开源工具）



## ✨ 分享交流

[微信群二维码/discord群(?)]




## ©️ 许可协议

项目遵循 [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) / [The MIT License](https://opensource.org/licenses/MIT) / [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) (?) 开源协议。 



## 📚 引用

```bibtex
（如果有引用论文的话）
```
