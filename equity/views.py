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
from django.http.response import HttpResponse
import mimetypes

# Create your views here.

def index(request):
    df=bhavcopy()
    r=redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
    with r.pipeline() as pipe:
        for index,row in df.iterrows():
            equity_name=row['SC_NAME']
            equity_desc={"code":str(row['SC_CODE']),"open":str(row['OPEN']),"close":str(row['CLOSE']),"high":str(row['HIGH']),"low":str(row['LOW'])}
            pipe.hmset(equity_name.encode('utf-8'),equity_desc)
        pipe.execute()
    r.bgsave()
    val=''
    equity_dict={}
    search=searchForm()
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    # Define text file name
    filename = 'EQ300421.CSV'
    # Define the full file path
    filepath = os.path.join(download_path,'equities.CSV')
    if request.method == 'POST':  
        search_value = request.POST['search_equity']
        val=search_value.strip().upper()
        download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
        # Define text file name
        filename = 'EQ300421.CSV'
        # Define the full file path
        filepath = os.path.join(download_path,'equities.csv')
        if(len(val)>0):
            filtered_dict={}
            if os.path.exists(filepath):
                os.remove(filepath)
            with open(filepath, 'a') as f:
                f.write("{},{},{},{},{},{}\n".format("Name", "Code","Open","Close","High","Low"))
                for key in sorted(r.keys()):
                    if 'celery' not in key:
                        if val.lower() in key or val.upper() in key:
                            filtered_dict[key]=r.hgetall(key)
                            f.write("{},{},{},{},{},{}\n".format(key,filtered_dict[key]["code"],filtered_dict[key]["open"],filtered_dict[key]["close"],filtered_dict[key]["high"],filtered_dict[key]["low"] ))
            
            return render(request,'index.html',context={'text':filtered_dict,'form':search})
          
    if os.path.exists(filepath):
        os.remove(filepath)
    with open(filepath, 'a') as f:
        f.write("{},{},{},{},{},{}\n".format("Name", "Code","Open","Close","High","Low"))
        for key in sorted(r.keys("*")):
            if 'celery' not in key:
                equity_dict[key]=r.hgetall(key)
                f.write("{},{},{},{},{},{}\n".format(key,equity_dict[key]["code"],equity_dict[key]["open"],equity_dict[key]["close"],equity_dict[key]["high"],equity_dict[key]["low"] ))
    
    return render(request,'index.html',context={'text':equity_dict,'form':search})

def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    # Define text file name
    filename = 'EQ300421.CSV'
    # Define the full file path
    filepath = os.path.join(download_path,'equities.CSV')
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

def bhavcopy():
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    target_zip = download_path+'/'+ 'hello'+'.zip'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    url='http://www.bseindia.com/download/BhavCopy/Equity/EQ300421_CSV.ZIP'
    # url='https://www.bseindia.com/download/BhavCopy/Equity/EQ030521_CSV.ZIP'
    response = requests.get(url,headers=headers, timeout=5)
    with open(target_zip, "wb") as file:
        file.write(response.content)
        file.close()
    with zipfile.ZipFile(target_zip, "r") as compressed_file:
        compressed_file.extractall(Path(target_zip).parent)
    os.remove(target_zip)
    df=pd.read_csv(os.path.join(download_path,'EQ300421.CSV'))
    return df
