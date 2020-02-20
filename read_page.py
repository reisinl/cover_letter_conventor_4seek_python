import json
import os
import time
from datetime import datetime

import requests
import timestring as timestring
from bs4 import BeautifulSoup
from docx import Document

# The server anti-crawling mechanism will determine whether the User-Agent in the client's request header is from a
# real browser. Therefore, we often use Requests to specify that the UA pretends to be a browser to initiate a request.
headers = {'user-agent': 'Mozilla/5.0'}
# template file path
template_file = "./template/template.docx"
# output path
out_put_path = "./output/"
# job url list file path
job_list_file = "./job_list/jobs.txt"


def read_job_list_url():
    job_array = []
    for job in open(job_list_file, 'r'):
        job_array.append(job)
    return job_array


def analyze_url(job_array):
    for job_url in job_array:
        job_url = job_url.replace('\n', '')
        res = requests.get(job_url, headers=headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        job = soup.find('script', {'data-automation': 'server-state'}).string
        job_info = job.replace(r'\u002F', '/').replace('\n', '').split("window.SK_DL = ")[1]
        quota_index = job_info.rfind(';');
        print(job_info[:quota_index] + '');

        job_object = json.loads(job_info[:quota_index] + '');
        job_location = job_object['jobLocation']
        job_area = job_object['jobLocation']
        job_title = job_object['jobTitle']
        job_list_date = timestring.Date(job_object['jobListingDate'])
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        out = datetime.strptime(job_object['jobListingDate'], f)
        job_date = out.strftime("%d %b %Y")
        job_company = job_object['advertiserName'];

        replace_dict = {
            "job_title": job_title.strip(),
            "job_date": job_date.strip(),
            "job_company": job_company.strip(),
            "job_area": job_area.strip(),
            "apply_date": time.strftime("%d %b %Y", time.localtime())
        }

        save_file(replace_dict)


def save_file(replace_dict):
    doc = Document(template_file)
    for para in doc.paragraphs:
        for i in range(len(para.runs)):
            for key, value in replace_dict.items():
                if key in para.runs[i].text:
                    print(key + "-->" + value)
                    para.runs[i].text = para.runs[i].text.replace(key, value)

    # get apply date
    apply_time = time.strftime("%Y-%m-%d", time.localtime())
    apply_company = replace_dict["job_company"]

    new_file_path = out_put_path + apply_time + "/" + apply_company + "/"
    mkdir(new_file_path)

    doc.save(new_file_path + "Cover letter_Leo Liu.docx")


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    job_list = read_job_list_url()
    analyze_url(job_list)
