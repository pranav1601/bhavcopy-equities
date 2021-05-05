import pandas as pd
import os
from pathlib import Path
import redis
import glob
from datetime import datetime

def redis_save():
    r=redis.StrictRedis(host="redis", port=6379, charset="utf-8", decode_responses=True)
    df=bhavcopy()
    with r.pipeline() as pipe:
        for index,row in df.iterrows():
            equity_name=row['SC_NAME']
            equity_desc={"code":str(row['SC_CODE']),"open":str(row['OPEN']),"close":str(row['CLOSE']),"high":str(row['HIGH']),"low":str(row['LOW'])}
            pipe.hmset(equity_name.encode('utf-8'),equity_desc)
        pipe.execute()
    r.bgsave()

def redis_search(val,filepath):
    r=redis.StrictRedis(host="redis", port=6379, charset="utf-8", decode_responses=True)
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
    
    return filtered_dict

def bhavcopy():
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    curr_bhavcopy=''
    for file_name in glob.iglob(download_path+'/*.CSV', recursive=True):
        curr_bhavcopy=file_name
    df=pd.read_csv(os.path.join(download_path,curr_bhavcopy))
    return df

def text_util():
    curr_time=datetime.now()
    today=datetime.today().weekday()
    if(today==6 or today==5):
        return("You are looking at Friday's data")
    if(curr_time.hour<18):
        return('If you want to view the Equity information for today, tune in after 6 pm')
    return('')
    