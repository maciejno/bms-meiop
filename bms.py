import pandas as pd
import numpy as np
import os

#path = os.path.realpath('lab_zdalne2.csv')
#print(path)
data = pd.read_csv('lab_zdalne.csv')
print(data)
t = data[data.columns[0]]
print(t)
