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


## 📚数据集


|    来源    | 规格 | 时长 |    条目     |
| :--------: | :--: | :--: | :---------: |
| Pexels-Raw | 720p | 672h | 106k+ clips |

### 下载方式：

从[ModelScope](https://www.modelscope.cn/datasets/OpenVideo/pexel-0808-complete-final-test)下载：

```bash
git clone https://user_id:access_token@www.modelscope.cn/datasets/OpenVideo/pexel-0808-complete-final-test.git
```

从[huggingface](https://huggingface.co/datasets/OpenVideo/pexel-0808-complete-final-test)下载：

```bash
git clone https://user_id:access_token@huggingface.co/datasets/OpenVideo/pexel-0808-complete-final-test
```

(user_id是用户名，access_token需要在设置里生成)

### 解压脚本：




## ⚡工具说明


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

### 视频标注平台

我们开发了一款基于Rust语言的[视频标注平台](https://huggingface.co/spaces/OpenVideo/GPT4o-Azure-Caption-Pixel)，旨在高效生成图像、视频等多种媒体的标签。该平台支持调用当前最先进的AI模型，如GPT-4o、Gemini、Claude3等，支持多提示输入和灵活的配置选项。其设计注重高性能，能够实现每秒处理100次查询，任务处理能力可扩展至2亿次。借助100个API账号，该工具可在8小时内合成包含20万条视频的数据集。所有输出内容均按模型和提示进行分类整理，确保结构清晰，便于后续研究与应用的集成。

![image-20250123193428569](C:\Users\Lenovo.LAPTOP-SKL8TDNF\AppData\Roaming\Typora\typora-user-images\image-20250123193428569.png)

（如遇显示问题，可换Edge浏览器查看）



### 标注校验平台

我们提供了一个[视频标注校验平台](https://huggingface.co/spaces/OpenVideo/AIL-Caption-lalala-Dup)，对已标注的视频数据集，可以在页面上进行标注查看、校验、修改。

**使用方式：**

1. 打开HuggingFace链接（如遇显示问题，可换Edge浏览器查看）；

2. 输入[个人token](https://huggingface.co/settings/tokens)；

   ![image-20250114200437826](C:\Users\Lenovo.LAPTOP-SKL8TDNF\AppData\Roaming\Typora\typora-user-images\image-20250114200437826.png)

   ![image-20250114200520285](C:\Users\Lenovo.LAPTOP-SKL8TDNF\AppData\Roaming\Typora\typora-user-images\image-20250114200520285.png)

   3. 通过标注平台播放视频，查看对应的标注文本，修改标注文本和切换下一个视频。

   

**对于用户自定义数据集需要满足：**

1. 数据集与代码在同一平台上（例如，数据集托管在huggingface）；

2. 修改代码中的[数据集路径]([run.py · OpenVideo/AIL-Caption-lalala-Dup at main](https://huggingface.co/spaces/OpenVideo/AIL-Caption-lalala-Dup/blob/main/run.py#L7))。



### **数据迁移**

我们提供了一个通用的[数据迁移平台](https://huggingface.co/spaces/OpenVideo/HF_To_MS)，用于将HuggingFace的数据集迁移到ModelScope，方便数据集在不同地区的网络下访问和使用。

**使用方式：**

输入HuggingFace的个人token、HuggingFace的数据集路径、ModelScope的个人token和ModelScope对应的仓库目录，点击Submit即可以后台运行的方式将数据集从HuggingFace复制到ModelScope对应的仓库中

![image-20250114203129668](C:\Users\Lenovo.LAPTOP-SKL8TDNF\AppData\Roaming\Typora\typora-user-images\image-20250114203129668.png)



## 👨‍💻 贡献者

爬虫算法： @yangming @heatingma @ZZY @晚来风雪

数据来源： @yangming @晚来风雪 @杰杰杰

数据清洗： @一马平川  @zjukop @伊小布

Prompt:      @Tiger.C @dpyneo @巧克力

模型打标：  @YUE @zjukop

校验平台：  @YUE @晚来风雪

数据回流：  @晚来风雪 @heatingma

人工校验：  @一马平川 @dpyneo @杨嘉昊 @flipped @yi @belive @思恩

项目调研：  @dingby @believe

美学指导：  @图拉 @杨嘉昊

文档：@ZZY @枪枪

项目统筹：@巧克力

## 🙏 致谢

服务器/资金支持：李白人工智能实验室

存储/海外专线：HuggingFace、ModelScope、OPENDataLab

分享交流：@shoulder @王铁震 @杨欢 @新年京

参与讨论：@前仰跳投 @浮羽 @MYX @Winniy @GUI @Planet

## ✨ 分享交流






## ©️ 许可协议

项目遵循 [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 开源协议。 



