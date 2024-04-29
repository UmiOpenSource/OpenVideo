
import os


os.environ["http_proxy"] = "http://127.0.0.1:10809"
# os.environ["https_proxy"] = "http://127.0.0.1:10809"

os.environ["all_proxy"] = "socks5://127.0.0.1:10808"



#验证SDK token
from modelscope.hub.api import HubApi
api = HubApi()
api.login('82b75562-3f1b-4ab8-a56e-cb282018db62')

#数据集下载
from modelscope.msdatasets import MsDataset
ds =  MsDataset.load('OpenVideo/pexels')
#您可按需配置 subset_name、split，参照“快速使用”示例代码