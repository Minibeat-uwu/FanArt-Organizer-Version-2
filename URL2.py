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

df=pd.read_csv('example.csv', index_col=0)

print(df)
test=df.itemsets.tolist()
x={test.replace('frozenset','').replace('{','').replace("'","").replace('}','') for x in test}
print(x)
