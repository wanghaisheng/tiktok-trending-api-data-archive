import encodings
import json
import os
import time
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

                    


def dailyupdate():
    allsecuid=[]

    alluserinfo=list()
    allusers = list()    
    for t in ['www','t','m']:
        userfiles = list_jsons(t)
        today = date.today()

        date =datetime(today.year, today.month, today.day).strftime("%Y-%m-%d")

        dailyupdatefiles=[x for x in userfiles if date in x]
        for filepath in dailyupdatefiles:
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                with open(filepath, encoding='utf-8') as f:
                    obj = json.load(f)
                    user_list = obj['user']
                    savehotstar(user_list)

     


def savehotstar(stars):

    items = [item for item in stars]
    for i in items:
        uid = i['userId'].strip()
        data = supabase_db.table("tiktoka_tiktok_users").select(
            'uid').eq("uid", uid).execute()
        # print(type(data))
        # print('existing db',len(supabase_db.table("tiktoka_douyin_users").select('uid').execute()[0]),data,data[0])
        if len(data.data) > 0:
            print('this user exist', uid, data.data)
        else:
            user = {}
            user['avatar_larger_uri'] = i['avatar']['jpeg']['large'].split('/')[-1]
            user['avatar_prefix'] =  i['avatar']['jpeg']['large'].split('/')[0]
            user['avatar_thumb_uri'] = i['avatar']['jpeg']['small'].split('/')[-1]
            user['nickname'] = i['name'].strip()
            user['uid'] = i['uid'].strip()
            user['sec_uid'] = i['secUserId'].strip()
            user['signature'] = i['bio'].strip()
            user['follower_count'] = i['stats']['followers'].strip()
            user['total_favorited'] = i['stats']['likes'].strip()
            
            data = supabase_db.table(
                "tiktoka_tiktok_users").insert(user).execute()
dailyupdate()