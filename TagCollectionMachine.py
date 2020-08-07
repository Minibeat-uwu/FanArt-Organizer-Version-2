import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import shutil
import pathlib as pl
import pandas as pd
import core
from pixivapi import *
import operator
import time
import requests
from os.path import isfile,join
from os import listdir
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

import requests
from bs4 import BeautifulSoup as soup
import json




client=Client()
# You think there would be something in this pixiv acccount, nope you won't XD
client.login('dicker_max', 'DickerMax@MyWarehouse')
Location='D:/PicturesTestGround/1stStage/Human'
Organized_Loc='D:/PicturesTestGround/2ndStage'

# PicLoc: art location url
# PicFile: Full File Name of the art

PicLoc=core.get_files_recursively(Location)
PicFile=[f for f in listdir(Location) if isfile(join(Location,f))]
FullDataset=[]


counter=0


def TagCollectorVer2(ID):
    
    Taggies2=[]
    IDString=str(ID)
    url='https://www.pixiv.net/en/artworks/'+str(ID)
    r=requests.get(url)
    html=soup(r.content,'html.parser')
    x=html.find("meta", {"id": "meta-preload-data"}).get("content")

    Data=json.loads(x)
    # print('hi')
    for i in range(len(Data["illust"][IDString]['tags']['tags'])):
        teemp=Data["illust"][IDString]['tags']['tags'][i]['tag']
        clean=teemp.replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')

        Taggies2.append(clean)
    # print(Taggies2)
    return Taggies2



def fileDestinationFinder( CodeNumber,PicLocation):
    temp=''
    for i in range(len(PicLocation)):
        
        if CodeNumber in PicLocation[i]:
            
            temp=PicLocation[i]
            break

    return temp

def url_ok(url):
    r=requests.head(url)
    return r.status_code

FanartDataDic={
    "ArtLocation": '',           # Art's Location URL
    "ArtFileFullName":'',        # Art's File Name
    "ArtTags": [],               # Art's Taglist
    "Trigger": False            # Boolean to see if it's moved or not. 

}


for i in range(len(PicFile)):
    


    try:
        if '_' in PicFile[i]:
            temp=PicFile[i].split('_')
            print(str(counter)+' / '+str(len(PicFile)) + '     Completed', end='\r')
            yeet=fileDestinationFinder(PicFile[i],PicLoc)

            FanartDataDic["ArtFileFullName"]=PicFile[i]
            FanartDataDic["ArtLocation"]=yeet
            FanartDataDic["ArtTags"]=TagCollectorVer2(temp[0])
            FullDataset.append(FanartDataDic.copy())

            
            # print(FanartDataDic)
            
            # Dataset.append(TagCollector(temp[0]))
            # SuccessFile.append(PicFile[i])
            counter=counter+1

            
    
    except Exception as e:
        test=str(e)
        if '404' in test:

            print('Image: '+PicFile[i]+'        Currently does not have active link')
            # shutil.move(PicLoc[i],'D:/PicturesTestGround/1stStage/No Link')
        elif '400' in test:
            print('Just have a bad day man... It was just a bad request, no biggie: '+PicFile[i])
            # shutil.move(PicLoc[i],'D:/PicturesTestGround/1stStage/No Link')

        else:
            print('Failed to collect the tag data for the image: '+ PicFile[i] + '. At position: '+ str(counter))
            shutil.move(yeet,'D:/PicturesTestGround/1stStage/No Link')
            # print('Going to restart the engine due to Pixiv API Rate Limit... wait bout 5 min')
            # time.sleep(300)
            # print("I'm back")

            # try:
            #     if '_' in PicFile[i]:
                    
            #         temp=PicFile[i].split('_')
            #         yeet=fileDestinationFinder(PicFile[i],PicLoc)


            #         FanartDataDic["ArtFileFullName"]=PicFile[i]
            #         FanartDataDic["ArtLocation"]=yeet
            #         FanartDataDic["ArtTags"]=TagCollectorVer2(temp[0])

            #         # print(FanartDataDic)
            #         FullDataset.append(FanartDataDic.copy())
            #         counter=counter+1
            # except Exception as e:
            #     test=str(e)
            #     if '404' in test:

            #         print('Image: '+PicFile[i]+'        Currently does not have active link')
            #         # shutil.move(PicLoc[i],'D:/PicturesTestGround/1stStage/No Link')
            #     elif '400' in test:
            #         print('Just have a bad day man... It was just a bad request, no biggie: '+PicFile[i])
            #         # shutil.move(PicLoc[i],'D:/PicturesTestGround/1stStage/No Link')



    # except:
        
    #     # Test if the link is alive or not, if it's alive, it will wait for 5 min, if it's dead... skips to the next.
    #     url='https://www.pixiv.net/artworks/'+str(temp[0])
    #     # print(url)
    #     teep=url_ok(url)
    #     if teep==404:
    #         print('Image: '+PicFile[i]+'        Currently does not have active link')
    #     else:

    #         print('Failed to collect the tag data for the image: '+ PicFile[i] + '. At position: '+ str(counter))
    #         print('Going to restart the engine due to Pixiv API Rate Limit... wait bout 5 min')
    #         time.sleep(300)
    #         print("I'm back")
    #         if '_' in PicFile[i]:
                
    #             temp=PicFile[i].split('_')
                
    #             FanartDataDic["ArtFileFullName"]=PicFile[i]
    #             FanartDataDic["ArtLocation"]=fileDestinationFinder(PicFile[i],PicLoc)
    #             FanartDataDic["ArtTags"]=TagCollector(temp[0])

    #             # print(FanartDataDic)
    #             FullDataset.append(FanartDataDic.copy())
    #             counter=counter+1



# print(FullDataset)

with open("D:/PicturesTestGround/1stStage/Human.txt","w") as fp:   # Pickling
    json.dump(FullDataset,fp)










# def TagCollector(ID):
#     # Linked to the pixiv to collect the tags
#     test=client.fetch_bookmark(ID)
#     Taggies=[]

#     # Position 2=tags
#     a=list(test.values())
#     b=a[2]
#     for i in range(len(b)):
#         teemp=operator.itemgetter('name')(b[i])
#         clean=teemp.replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')

#         Taggies.append(clean)
#     return(Taggies)