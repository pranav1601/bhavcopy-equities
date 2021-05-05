from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
import glob
from django.shortcuts import render
import requests
import zipfile
from pathlib import Path
from datetime import datetime, timedelta,date
import mimetypes



@shared_task(name = "bhavcopy_csv")
def download_bhavcopy():
    today = date.today()
    d3 = today.strftime("%d/%m/%y")
    d,m,y=str(d3).split('/')
    date_bhavcopy=(d+m+y)
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    files=glob.glob(download_path+'/*.CSV')
    for f in files:
        os.remove(f)
    target_zip = download_path+'/'+ 'hello'+'.zip'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    url='https://www.bseindia.com/download/BhavCopy/Equity/EQ'+date_bhavcopy+'_CSV.ZIP'
    response = requests.get(url,headers=headers, timeout=5)
    with open(target_zip, "wb") as file:
        file.write(response.content)
        file.close()
    with zipfile.ZipFile(target_zip, "r") as compressed_file:
        compressed_file.extractall(Path(target_zip).parent)
    if os.path.exists(target_zip):
        os.remove(target_zip)