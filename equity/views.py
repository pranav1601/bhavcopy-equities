from django.shortcuts import render
import csv, os
from pathlib import Path
from django.http.response import HttpResponse
import mimetypes

from .utils import redis_save,redis_search,bhavcopy
from .forms import searchForm

# Create your views here.

def index(request):
    redis_save()
    val=''
    equity_dict={}
    search=searchForm()
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    filepath = os.path.join(download_path,'equities.csv')
    if request.method == 'POST':  
        filtered_dict={}
        search_value = request.POST['search_equity']
        val=search_value.strip().upper()
        if(len(val)>0):
            filtered_dict=redis_search(val,filepath)
        return render(request,'index.html',context={'text':filtered_dict,'form':search})
    equity_dict=redis_search('',filepath)
    return render(request,'index.html',context={'text':equity_dict,'form':search})

def download_file(request):
    download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
    filename = 'equities.csv'
    filepath = os.path.join(download_path,'equities.csv')
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response