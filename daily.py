import encodings
import json
import os
import time
from datetime import datetime, timedelta
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
import logging
from tenacity import *
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger(__name__)


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
    for t in ['www','t','m']:
        userfiles = list_jsons(t)
        today = date.today()

        datestr =datetime(today.year, today.month, today.day-1).strftime("%Y-%m-%d")
        print(datestr)
        dailyupdatefiles=[x for x in userfiles if datestr in x]
        print(dailyupdatefiles)
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

        user = {}
        user['avatar_larger_uri'] = i['avatar']['jpeg']['large'].split('/')[-1]
        user['avatar_prefix'] =  i['avatar']['jpeg']['large'].split('/')[0]
        user['avatar_thumb_uri'] = i['avatar']['jpeg']['small'].split('/')[-1]
        user['nickname'] = i['name'].strip()
        user['uid'] = i['userId'].strip()
        user['sec_uid'] = i['secUserId'].strip()
        user['signature'] = i['bio'].strip()
        user['follower_count'] = i['stats']['followers']
        user['total_favorited'] = i['stats']['likes']
        if len(data.data) > 0:
            print('this user exist', uid, data.data)
            supabaseupdate("tiktoka_tiktok_users",user,uid)

        else:
            supabaseop("tiktoka_tiktok_users",user)

            # data = supabase_db.table(
            #     "tiktoka_tiktok_users").insert(user).execute()  

@retry(stop=stop_after_attempt(10), before=before_log(logger, logging.DEBUG))
def supabaseop(tablename,users):
    try:
        data = supabase_db.table(tablename).insert(users).execute()    
    except:
        raise Exception
@retry(stop=stop_after_attempt(10), before=before_log(logger, logging.DEBUG))
def supabaseupdate(tablename,user,uid):
    try:
        data = supabase_db.table(tablename).update(user).eq("uid", uid).execute()    
    except:
        raise Exception
dailyupdate()