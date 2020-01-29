import json
import os
from datetime import datetime

import requests
import timestring as timestring
from bs4 import BeautifulSoup

# 服务器反爬虫机制会判断客户端请求头中的User-Agent是否来源于真实浏览器，所以，我们使用Requests经常会指定UA伪装成浏览器发起请求
headers = {'user-agent': 'Mozilla/5.0'}


# https://zhuanlan.zhihu.com/p/90855359

# 获取目标网址第几页
def getalldoc(ii):
    # 字符串拼接成目标网址
    testurl = "https://www.seek.co.nz/job/40700523"
    # 使用request去get目标网址
    res = requests.get(testurl, headers=headers)
    # 更改网页编码--------不改会乱码
    res.encoding = "utf-8"
    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(res.text, "html.parser")

    job = soup.find('script', {'data-automation': 'server-state'}).string
    job_info = job.replace(r'\u002F', '/').replace('\n', '').split("window.SK_DL = ")[1]
    quota_index = job_info.rfind(';');
    print(job_info[:quota_index] + '');

    job_object = json.loads(job_info[:quota_index] + '');
    job_location = job_object['jobLocation']
    job_area = job_object['jobArea']
    job_title = job_object['jobTitle']
    job_list_date = timestring.Date(job_object['jobListingDate'])
    f = "%Y-%m-%dT%H:%M:%S.%fZ"
    out = datetime.strptime(job_object['jobListingDate'], f)
    job_date = out.strftime("%d %b %Y")




def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


def getall():
    for i in range(1, 2, 1):
        getalldoc(i)


if __name__ == "__main__":
    getall()
