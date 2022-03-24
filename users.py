import encodings
import json
import os
import time
import pandas as pd
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
allsecuid=[]
alluserinfo=[]
allusers = []
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
    print(len(MergeJson))
    MergeJson= list({elem["secUserId"]:elem for elem in MergeJson}.values())
    alllist.extend(MergeJson)
alllist= list({elem["secUserId"]:elem for elem in alllist}.values())

with open("full.json", 'w') as output_file:
    json.dump(alllist, output_file)


    #             user_list = obj['user']
    #             # print(filepath,len(user_list))
    #             # items = [item for item in user_list]
    #             for item in user_list:
    #                 # print(i['user_info']['sec_uid'])
    #                 # print(i)
    #                 # time.sleep(30)
    #                 if item['secUserId'] in allusers:
    #                     pass
    #                 else:
    #                     allsecuid.append(item['secUserId'])
    #                     user={}
    #                     user['nickname']=item['name']
    #                     user['id']=item['userId']
    #                     user['uniqid']=item['id']
    #                     user['sec_uid']=item['secUserId']
    #                     alluserinfo.append(user)    

    #                     allusers.append(item)

     
    # allsecuid=list(set(allsecuid))
    # alluserinfo= list({elem["sec_uid"]:elem for elem in alluserinfo}.values())
    # allusers= list({elem["secUserId"]:elem for elem in allusers}.values())

    # with open('data/'+t+'-allusers.json', 'a+', encoding='utf-8') as f:
    #     json.dump(allusers, f, ensure_ascii=False, indent=4)
    # with open('data/'+t+'-allsecuid.txt', 'a+', encoding='utf-8') as f:
    #     json.dump(allsecuid, f, ensure_ascii=False, indent=4)
    # with open('data/'+t+'-alluserinfo.json', 'a+', encoding='utf-8') as f:
    #     json.dump(alluserinfo, f, ensure_ascii=False, indent=4)
