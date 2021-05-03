import csv, zipfile, os
import requests
from datetime import datetime, timedelta
from io import TextIOWrapper, StringIO
import pandas as pd
import os
import zipfile
import requests
from pathlib import Path
from datetime import datetime, timedelta

def bhavcopy():
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    target_zip = download_path+'/'+ 'hello'+'.zip'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    url='http://www.bseindia.com/download/BhavCopy/Equity/EQ300421_CSV.ZIP'
    response = requests.get(url,headers=headers, timeout=5)
    with open(target_zip, "wb") as file:
        file.write(response.content)
        file.close()
    with zipfile.ZipFile(target_zip, "r") as compressed_file:
        compressed_file.extractall(Path(target_zip).parent)
    df=pd.read_csv(os.path.join(download_path,'EQ300421.CSV'))
    return df