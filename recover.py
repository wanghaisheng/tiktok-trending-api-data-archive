import os

with open('m.json-commit-id.txt') as f:
    mids=f.readlines()
print(len(mids))


with open('www.json-commit-id.txt') as f:
    wwwids=f.readlines()
print(len(wwwids))


with open('t.json-commit-id.txt') as f:
    tids=f.readlines()
print(len(tids))

for id in tids:
   with open('t-recover.sh','a+') as fw:
        id=id.strip()
        fw.write('git show '+id+':t.json >'+'t/t'+'-'+id+'.json'+'\n')


for id in wwwids:
   with open('www-recover.sh','a+') as fw:
        id=id.strip()
        fw.write('git show '+id+':www.json >'+'www/www'+'-'+id+'.json'+'\n')



for id in mids:
   with open('m-recover.sh','a+') as fw:
        id=id.strip()
        fw.write('git show '+id+':m.json >'+'m/m'+'-'+id+'.json'+'\n')