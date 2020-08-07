import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import shutil
import pathlib as pl
import pandas as pd
import numpy as np
import core
from pixivapi import *
import operator
import time
import requests
from os.path import isfile,join
from os import listdir
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import csv

# FanartDataDic={
#     "ArtLocation": '',           # Art's Location URL
#     "ArtFileFullName":'',        # Art's File Name
#     "ArtTags": [],               # Art's Taglist
#     "Trigger": False            # Boolean to see if it's moved or not. 

# }




Destination_Loc='D:/PicturesTestGround/2ndStage'

with open("D:/PicturesTestGround/1stStage/Human.txt","r") as fp:
    CompleteDataDic=json.load(fp)

# with open("D:/PicturesTestGround/1stStage/Human2.txt","r") as fp2:
#     CompleteDataDic=json.load(fp2)


# for i in range(len(DDList1)):
#     CompleteDataDic.append(DDList1[i])

# print(len(CompleteDataDic))

# np.savetxt('data.csv',CompleteDataDic,delimiter=",",fmt='%s')



def Aprioriset(List,TH):

    Dataset=[]
    # print(CompleteDataDic[1]["ArtTags"])
    
    # print(type(List[0]["ArtTags"]))

    for i in range(len(List)):
        if List[i]["Trigger"]==False:
            Dataset.append(List[i]["ArtTags"])
        

    # Apriori Process:
    te = TransactionEncoder()
    te_ary=te.fit(Dataset).transform(Dataset)
    df=pd.DataFrame(te_ary,columns=te.columns_)
    Aprioried_List= apriori(df, min_support=TH, use_colnames=True)

    # print(Aprioried_List)
    
    Aprioried_List.to_csv('te.csv')


    return Aprioried_List


def FolderCreator(AList,DLoc):
    Lili=[]
    Single=[]
    Ceiling=0
    # Creates a list of existing folders
    folders=DestinationList(DLoc)
    

    # Creates a list of pairs where there are no repetition to any tags
    for i in range(len(AList)):

        if Ceiling<len(AList.loc[i,'itemsets']):
            Ceiling=len(AList.loc[i,'itemsets'])
        
        if len(AList.loc[i,'itemsets'])==1:
            item=str(AList.loc[i,'itemsets'])
            x=item.replace('frozenset','').replace('({','').replace("'","").replace('})','')
            Single.append(x)

        elif len(AList.loc[i,'itemsets'])==2:
            # This process will take the pair tags from the Dataframe. 
            item=str(AList.loc[i,'itemsets'])
            x=item.replace('frozenset','').replace('({','').replace("'","").replace('})','')
            temp1, temp2=x.split(', ')
            trig=False
            

            if len(Lili)==0:
                Lili.append(x)
            else:
                trig=False
                for z in range(len(Lili)):
                    if temp1 in Lili[z]:
                        trig=True
                        # print('hit')
                    if temp2 in Lili[z]:
                        trig=True
                        # print('hit2')
                if trig==False:
                    
                    Lili.append(x)
                    
        
    
    # Now it's time to combine Lili(non repeating pairs) and folder list
    # In this section, it's going to compare the pre-existing folders and the Lili folders and see if there's any that needs to be added.
    if Ceiling==1:
        for i in range(len(Single)):
            trig=False
            
            for j in range(len(folders)):
                
                if Single[i] in folders[j]:
                    trig=True
                if Single[i] in folders[j]:
                    trig=True
                
            if trig==False:
                try:
                    clean=Single[i].replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')
                    print('Current shitty folder that is going to be created: '+ clean)
                    loc=DLoc+'/'+clean
                    tempLoc=DLoc+'/'+clean
                    os.makedirs(tempLoc)
                except:
                    print('Failed to create the folder')


    else:
        for i in range(len(Lili)):
            trig=False
            
            for j in range(len(folders)):
                temp1, temp2=Lili[i].split(', ')
                if temp1 in folders[j]:
                    trig=True
                if temp2 in folders[j]:
                    trig=True
                
            if trig==False:
                try:
                    clean=Lili[i].replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')
                    # print('Current shitty folder that is going to be created: '+ clean)
                    loc=DLoc+'/'+clean
                    tempLoc=DLoc+'/'+clean
                    os.makedirs(tempLoc)
                except:
                    print('Failed to create the folder')
    
    return(Ceiling)

def DestinationList(OrgList):
    foldList=[]
    for r,d,f in os.walk(OrgList):
        for folder in d:
            foldList.append(os.path.join(r,folder))
            
    return foldList

def Mover(CDD,Dest):
    
    for i in range(len(CDD)):

        if CDD[i]["Trigger"]==False:

            TagList=CDD[i]["ArtTags"]
            FileName=CDD[i]["ArtFileFullName"]
            FileURL=CDD[i]["ArtLocation"]
            trigger=False
            count=0
            while trigger==False:
                # print(FileName)
                # print(FileName +'   '+ str(count)+'/'+str(len(TagList))+': '+TagList[count]+'   '+str(TagList))
                
                for j in range(len(Dest)):
                    try:
                        if TagList[count] in Dest[j]:
                            try:
                                # print('Moving: ' + FileName +'-> '+Dest[j]+ '      with matching: '+TagList[count] )
                                shutil.move(FileURL,Dest[j])
                                CDD[i]["Trigger"]=True
                            except:
                                pass
                                # print('Failed to move: '+FileName +'-> '+Dest[j])
                            
                            trigger=True
                            break
                    except:
                        # print('Failed to move: '+FileName+ '        '+str(TagList)+ '   '+str(CDD[i]['Trigger']))
                        print('Failed to move: '+FileName)
                        CDD[i]['Trigger']=True
                        trigger=True
                        break
                
                count=count+1
                
                if count==len(TagList):
                    # print('No matching tags -> folders to: ' + FileName)
                    count=0
                    trigger=True
                
    
    
    return(CDD)
            
        
        



threshold=0.05

switch=False


while switch==False:
    counter=0

    AprList=Aprioriset(CompleteDataDic,threshold)

    Ceil=FolderCreator(AprList,Destination_Loc)

    DestinationFolders=DestinationList(Destination_Loc)

    CompleteDataDic=Mover(CompleteDataDic,DestinationFolders)

    
    for i in range(len(CompleteDataDic)):
        if CompleteDataDic[i]["Trigger"]==True:
            counter=counter+1
    
    if counter==len(CompleteDataDic):
        switch=True
    
    # if Ceil==0:
    if Ceil==0 and counter!=len(CompleteDataDic):
        # switch=True
        # 182 Files
        if threshold>0:
            threshold=threshold-0.01
            print('Current Threshold: '+str(threshold))
            
    if threshold<0:
        # for i in range(len(CompleteDataDic)):
        #     if CompleteDataDic[i]['Trigger']==False:
        #         print(CompleteDataDic[i]['ArtFileFullName']+ ':      ' +str(CompleteDataDic[i]['ArtTags']))
        switch=True
    
    print('current: '+str(counter)+'/'+str(len(CompleteDataDic)))
    time.sleep(3)
# "ArtFileFullName":'',        # Art's File Name
#     "ArtTags": [],               # Art's Taglist