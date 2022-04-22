import encodings
import json
import os
import time
import pandas as pd
from datetime import datetime, timedelta
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载文件
load_dotenv(".env")
supabase_url = os.environ.get('supabase_url')
supabase_apikey = os.environ.get('supabase_apikey')
supabase_db: Client = create_client(
    supabase_url=supabase_url, supabase_key=supabase_apikey)

def list_jsons(path):
    # list files in img directory
    userfiles = []
    files = os.listdir(path)
    for file in files:
        # make sure file is an image
        if file.endswith(('.json')):
            userfiles_path = path +os.sep+ file
            userfiles.append(userfiles_path)
    return userfiles

def archives():
    allsecuid=[]

    alluserinfo=list()
    allusers = list()
    alllist=list()    
    for t in ['www','t','m']:
        MergeJson=list()

        userfiles = list_jsons(t)
        for filepath in userfiles:
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                with open(filepath, encoding='utf-8') as f:
                    obj = json.load(f)
                    # print(len(obj['user']))
                    MergeJson.extend(obj['user'])
                    user_list = obj['user']
                    savehotstar(user_list)

                    

archives()