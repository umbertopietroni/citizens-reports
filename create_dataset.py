import pandas as pd
import numpy as np
pd.set_option('max_columns', 120)
pd.set_option('max_colwidth', 5000)


#import matplotlib.pyplot as plt
#import seaborn as sns
#%matplotlib inline
#plt.rcParams['figure.figsize'] = (12,8)

segnalazioni = pd.read_csv('dataset.csv',low_memory=False) 
#print(segnalazioni.head(3))
print (segnalazioni.columns)
print(segnalazioni.shape)

segnalazioni.head()
