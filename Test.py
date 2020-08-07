import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import shutil
import pathlib as pl
import core
import program as po
import pandas as pd

 

DanbooruPos = 'danbooru-resnet_custom_v1-p3'


DirList=['D:/PicturesTestGround/1stStage/Chibi','D:/PicturesTestGround/1stStage/Food','D:/PicturesTestGround/1stStage/Scenery',
         'D:/PicturesTestGround/1stStage/Animal','D:/PicturesTestGround/1stStage/Human', 'D:/PicturesTestGround/1stStage/Other']

# Chibi, Food, Scenery, Animal, Human, Other

# 1: human, 2: No_Human 0: Other
# tags that I can use:
# girl, boy, no_human, scenery, animal, food, chibi,

def Sections_Creator(tags, results):
    Sections = [0, 0, 0, 0, 0]
    for i in range(len(tags)):
        # 0: no human, 1: yes human
        # human=0
        # scenery=0       tag#: 3806
        # animal=0        tag#: 183
        # food=0          tag#: 1634
        # chibi=0         tag#: 946

        #    C , F , S , A , H

        if results[i] > 0.5:
            if "girl" in tags[i]:
                if Sections[4] < results[i]:
                    Sections[4] = results[i]

            elif "boy" in tags[i]:
                if Sections[4] < results[i]:
                    Sections[4] = results[i]

            if i == 183:    # Animal
                Sections[3] = results[i]
            if i == 946:    # Chibi
                Sections[0] = results[i]
            if i == 1634:   # Food
                Sections[1] = results[i]
            if i == 3806:   # Scenery
                Sections[2] = results[i]

    return(Sections)

def Movers(Trig):
    try:
        if max(Section_results)==0 and Trig==0:
                shutil.move(PicLoc,DirList[5])
        else:
            if Trig!=0:
                for x in range(len(Section_results)):
                    if Section_results[x]!=0:
                        shutil.move(PicLoc,DirList[x])
                        break
                shutil.move(PicLoc,DirList[4])    
                
            else:
                TrigPt = Section_results.index(max(Section_results))
                if(TrigPt==0):      # Chibi
                    shutil.move(PicLoc,DirList[0])
                elif(TrigPt==1):    # Food
                    shutil.move(PicLoc,DirList[1])
                elif(TrigPt==2):    # Scenery
                    shutil.move(PicLoc,DirList[2])
                elif(TrigPt==3):    # Animal
                    shutil.move(PicLoc,DirList[3])
                
                
    except:
        pass


        
List_files = core.get_files_recursively('E:/Otaku Fan Arts/Pictures')

for i in range(len(List_files)):
    
    PicLoc = List_files[i]
    
    try:
        tags, results = po.evaluate_project(DanbooruPos, PicLoc)
        # Section_results: Human, Animal, Chibi, Food, Scenery
        
        Section_results = Sections_Creator(tags, results)
        
        Human=Section_results.pop(4)
        # print(PicLoc + ': ' + str(Section_results))

        Movers(Human)
        print(str(i)+'/'+str(len(List_files))+ '    Current File: '+PicLoc, end='\r')


    except:
        print('Failed to evaluate the image: '+ str(PicLoc))

    









# if Section_results[0] != 0:

# else:
#     for i in range(4):
#         if PicCateg < Section_results[i+1]:


# if human==0:
#     pass
# else:
#     pass
