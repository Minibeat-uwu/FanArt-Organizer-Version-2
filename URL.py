import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import shutil
import pathlib as pl
import pandas as pd
import core
from pixivapi import *
import operator
from os.path import isfile,join
from os import listdir
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori



client=Client()
# You think there would be something in this pixiv acccount, nope you won't XD
client.login('dicker_max', 'DickerMax@MyWarehouse')
Location='D:/Projects/Results/Chibi'
Organized_Loc='D:/Projects/Results2'







def fileDestinationFinder( CodeNumber,PicLocation):
    temp=''
    for i in range(len(PicLocation)):
        
        if CodeNumber in PicLocation[i]:
            
            temp=PicLocation[i]
            break

    return temp


# Creates all the existing folder's name list in that directory.
def folderDestinationList(OrgList):
    foldList=[]
    for r,d,f in os.walk(OrgList):
        for folder in d:
            foldList.append(os.path.join(r,folder))
            
    return foldList

# Collect just the tags from the dict lists
def TagCollector(ID):
    test=client.fetch_bookmark(ID)
    Taggies=[]

    a=list(test.values())
    b=a[2]
    for i in range(len(b)):
        Taggies.append(operator.itemgetter('name')(b[i]))
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
            clean=Lili[i].replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_')
            loc=OLoc+'/'+clean
            tempLoc=OLoc+'/'+clean
            os.makedirs(tempLoc)

def TagsDestComparator(taggies,DestinationList):
    Trigger=False
    for i in range(len(taggies)):
        for j in range(len(DestiantionList)):
            if taggies[i]==DestinationList[j]:
                Trigger==True
                break


#          str       list    str
def Mover(FileCode, ArtTags, Destination,Piclc):
    #PicFile's location is == Dataset's Position
    # FileCode:

    # it's going to compare the art tags with the file names and see if there's any matches. If there's at least one match, it will move that bugger to that folder.
    for i in range(len(FileCode)):
        TagList=ArtTags[i]
        TagTrig=False
        count=0
        while TagTrig==False:
            
            for k in range(len(Destination)):
                    
                if TagList[count] in Destination[k]:
                    FileLoc=fileDestinationFinder(FileCode[i],Piclc)
                    # print(FileCode[i]+',         '+TagList[i]+' is in '+ Destination[j])
                    temp=Destination[k]
                    
                    # print(FileLoc+'         '+ temp)
                    try:
                        
                        shutil.move(FileLoc,temp)
                    except:
                        print('Failed to move: '+ Destination[k])
                    
                    TagTrig=True
                    break
            count=count+1
        

            












PicLoc=core.get_files_recursively(Location)
PicFile=[f for f in listdir(Location) if isfile(join(Location,f))]
Dataset=[]


for i in range(len(PicFile)):
    try:
        if '_' in PicFile[i]:
            temp=PicFile[i].split('_')
            
            Dataset.append(TagCollector(temp[0]))
            

    except:
        print('nope')


# for i in range(len(PicFile)):
#     try:
#         if '_' in PicFile[i]:
#             temp=PicFile[i].split('_')
#             # print(temp[0])
#             Dataset.append(TagCollector(temp[0]))
#     except:
#         print('Error reading file: ' + PicFile[i])
        
#     # print(temp)
#     # print(TagList)


te = TransactionEncoder()
te_ary=te.fit(Dataset).transform(Dataset)
df=pd.DataFrame(te_ary,columns=te.columns_)
Aprioried_List= apriori(df, min_support=0.05, use_colnames=True)

FolderCreator(Aprioried_List,Organized_Loc)

UpdatedFolderList=folderDestinationList(Organized_Loc)

# Pic Location position != PicFile position
# PicFile position == Dataset Position

# for i in range(len(PicLoc)):
    
#     print(PicLoc[i]+'       '+PicFile[i])


Mover(PicFile,Dataset, UpdatedFolderList,PicLoc)





        # if not os.path.isdir(temp_loc):
        #     os.makedirs(temp_loc)
        
    





# test=str(yeet.loc[54,'itemsets'])
# print(len(yeet.loc[54,'itemsets']))

# print(test)


# temp1,temp2=x.split(', ')

# trig=False
# loc=0
# for d in range(len(Dataset)):
#     if temp1 and temp2 in Dataset[d]:
#         trig=True
#         loc=d
#         break


# print(Dataset[loc])
# print(str(loc)+': '+str(trig))


# yeet.to_csv(r'example.csv', encoding='utf_8_sig', header=True)
# print(counter)






# print(Dataset)


# a=operator.itemgetter('tags')(test)
# b=