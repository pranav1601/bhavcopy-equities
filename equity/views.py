from django.shortcuts import render
import requests
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
import redis
from .forms import searchForm

# Create your views here.

def index(request):
    df=bhavcopy()
    r=redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
    with r.pipeline() as pipe:
        for index,row in df.iterrows():
            equity_name=row['SC_NAME']
            equity_desc={"code":row['SC_CODE'],"open":row['OPEN'],"high":row['HIGH'],"close":row['CLOSE'],"low":row['LOW']}
            pipe.hmset(equity_name.encode('utf-8'),equity_desc)
        pipe.execute()
    r.bgsave()
    val=''
    equity_dict={}
    search=searchForm()
    if request.method == 'POST':  
        search_value = request.POST['search_equity']
        val=search_value.strip().upper()
        if(len(val)>0):
            for key in sorted(r.keys("*"+val+"*")):
                equity_dict[key]=r.hgetall(key)
                print(equity_dict)
                return render(request,'index.html',context={'text':equity_dict,'form':search})
          
    
    for key in sorted(r.keys("*")):
        equity_dict[key]=r.hgetall(key)
    return render(request,'index.html',context={'text':equity_dict,'form':search})



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
    os.remove(target_zip)
    df=pd.read_csv(os.path.join(download_path,'EQ300421.CSV'))
    return df
