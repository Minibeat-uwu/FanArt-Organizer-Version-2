import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pathlib as pl
import pandas as pd
import click
from pixivapi import *
import operator
import time
import requests
from os.path import isfile,join
from os import listdir
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import json
import 2ndStage

@main.command('Organizer')
@main.argument('Picture_Batch_Location', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@main.argument('1st_Stage_Location',type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))

def Organize_Projec(Picture_Batch_Location, 1st_Stage_Location):
    PicFile=[f for f in listdir(Picture_Batch_Location) if isfile(join(Picture_Batch_Location,f))]

    1stStageList=DestinationList(1st_Stage_Location)

    for i in range()
