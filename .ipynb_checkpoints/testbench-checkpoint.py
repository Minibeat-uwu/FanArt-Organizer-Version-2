import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
#plotting library for python
import matplotlib.pyplot as plt
#fundamental package for scientific computing w/ python
import numpy as np
import pandas as pd
from IPython.display import clear_output
from six.moves import urllib


x=[1,2,2.5,3,5]
y=[1,4,8,9, 15]
plt.plot(x,y,'ro')          #plot the dots for that x,y
plt.axis([0,6,0,20])
plt.plot(np.unique(x),np.poly1d(np.polyfit(x,y,1))(np.unique(x))) # plot the line of close fit
plt.show()




# print(tf.version)

