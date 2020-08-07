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


# Dictionary, save the tags



client=Client()
# You think there would be something in this pixiv acccount, nope you won't XD
client.login('dicker_max', 'DickerMax@MyWarehouse')
Location='D:/Projects/Results/Chibi'
Organized_Loc='D:/Projects/Results2'

# Collect just the tags from the dict lists
def TagCollector(ID):
    # Linked to the pixiv to collect the tags
    test=client.fetch_bookmark(ID)
    Taggies=[]

    # Position 2=tags
    a=list(test.values())
    b=a[2]
    for i in range(len(b)):
        teemp=operator.itemgetter('name')(b[i])
        clean=teemp.replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')

        Taggies.append(clean)
    return(Taggies)

# Creates a pairing folder. AList is the aprioried list, which will only take pairs that exists and creates a folder for it. 
def FolderCreator(AList,OLoc):
    Lili=[]

    # Creates a list of existing folders
    folders=folderDestinationList(OLoc)
    

    # Creates a list of pairs where there are no repetition to any tags
    for i in range(len(AList)):
        if len(AList.loc[i,'itemsets'])==2:
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
                    print(x)
                        
    
            # Now it's time to combine Lili(non repeating pairs) and folder list
            # In this section, it's going to compare the pre-existing folders and the Lili folders and see if there's any that needs to be added.
    for i in range(len(Lili)):
        trig=False
        for j in range(len(folders)):
            temp1, temp2=x.split(', ')
            if temp1 in folders[j]:
                trig=True
            if temp2 in folders[j]:
                trig=True
            
        if trig==False:
            try:
                
                clean=Lili[i].replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')
                print('Current shitty folder that is going to be created: '+ clean)
                loc=OLoc+'/'+clean
                tempLoc=OLoc+'/'+clean
                os.makedirs(tempLoc)
            except:
                print('Failed to create the folder')


# Creates all the existing folder's name list in that directory.
def folderDestinationList(OrgList):
    foldList=[]
    for r,d,f in os.walk(OrgList):
        for folder in d:
            foldList.append(os.path.join(r,folder))
            
    return foldList

def fileDestinationFinder( CodeNumber,PicLocation):
    temp=''
    for i in range(len(PicLocation)):
        
        if CodeNumber in PicLocation[i]:
            
            temp=PicLocation[i]
            break

    return temp



#          str       list    str
def Mover(FileCode, ArtTags, Destination,Piclc):
    #PicFile's location is == Dataset's Position
    # FileCode: Successful Files that passed the test

    # it's going to compare the art tags with the file names and see if there's any matches. If there's at least one match, it will move that bugger to that folder.
    for i in range(len(FileCode)):
        TagList=ArtTags[i]
        TagTrig=False
        count=0
        while TagTrig==False:
            

            # Issue: if there is no match to any of the folders, it skips the reset of counter... which ends up extending over it's limit. 
            for k in range(len(Destination)):
                # print('TagList length: '+str(len(TagList))+'    Current TagPosition: '+ str(count)+ '   Current Destination Position: '+str(k))
                # print(TagList[count]+'      '+Destination[k])
                if TagList[count] in Destination[k]:
                    FileLoc=fileDestinationFinder(FileCode[i],Piclc)
                    
                    # print(FileCode[i]+',         '+TagList[i]+' is in '+ Destination[j])
                    temp=Destination[k]
                    
                    # print(FileLoc+'         '+ temp)
                    try:
                        print('Moving: ' + FileCode[i] +'-> '+temp+ '      with matching: '+TagList[count] )
                        shutil.move(FileLoc,temp)
                        # print('moved')
                    except:
                        print('Failed to move: '+ Destination[k])

                    TagTrig=True
                    break
            
            count=count+1
                # Resets the counter when it goes through the stuff and end up not finding the results. 
            if count==len(TagList):
                print('No matching tags->folders to: '+str(FileCode[i]))
                count=0
                TagTrig=True
                                

            

def url_ok(url):
    r=requests.head(url)
    return r.status_code




# PicLoc:       Direction to the picture location
# PicFile:      List of Picture file's names 
# Dataset:      List of tags for each of the files
PicLoc=core.get_files_recursively(Location)
PicFile=[f for f in listdir(Location) if isfile(join(Location,f))]
Dataset=[]
SuccessFile=[]

test=0

# Collects all the tags for each PicFile
# There's a rate limit of 350 files consecutively. Once it hits 350, it stops us from collecting the data. 
temp=''
for i in range(len(PicFile)):
    try:
        if '_' in PicFile[i]:
            print(str(test)+' / '+str(len(PicFile)) + '     Completed', end='\r')
            temp=PicFile[i].split('_')
            
            Dataset.append(TagCollector(temp[0]))
            SuccessFile.append(PicFile[i])
            test=test+1
            
    except:
        
        # Test if the link is alive or not, if it's alive, it will wait for 5 min, if it's dead... skips to the next.
        url='https://www.pixiv.net/artworks/'+str(temp[0])
        teep=url_ok(url)
        if teep==404:
            print('Image: '+PicFile[i]+'        Currently does not have active link')
        else:
                
            
            print('Failed to collect the tag data for the image: '+ PicFile[i] + '. At position: '+ str(test))
            print('Going to restart the engine due to Pixiv API Rate Limit... wait bout 5 min')
            time.sleep(300)
            print("I'm back")
            if '_' in PicFile[i]:
                temp=PicFile[i].split('_')
                
                Dataset.append(TagCollector(temp[0]))
        


# print(test)
time.sleep(3)


# Lets see what would happen if we create a while loop of apriori after it goes through once. 

# Apriori Process:
te = TransactionEncoder()
te_ary=te.fit(Dataset).transform(Dataset)
df=pd.DataFrame(te_ary,columns=te.columns_)
Aprioried_List= apriori(df, min_support=0.05, use_colnames=True)

# print(type(Dataset[0][1]))



Aprioried_List.to_csv('test.csv')

# print('Hold your horse bois')
# time.sleep(3)

# # Creates all the new pairing type folders
# FolderCreator(Aprioried_List,Organized_Loc)

# print('Folder created')
# time.sleep(3)


# # Update the list of existing folders (old and new ones)
# UpdatedFolderList=folderDestinationList(Organized_Loc)

# # Moves the specific file to that location
# Mover(SuccessFile,Dataset, UpdatedFolderList,PicLoc)
