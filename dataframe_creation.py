#### I want to create a new dataframe to be modeled
####
#### Steps
####  1) First pull the original csv file created from extract_part function and add team index
####  2) Make pieces that will go in to the final table (each will have 800 rows. 400 games * 2 teams per game)
####  3) Join the pieces into a final table. (800 rows)
####  4) Partition the final table into two, so that each row becomes independent of each other and write csv

#### Prereq
####  1) csv file from extract_part function


import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

########################## 1 ##########################

##extracted data
df = pd.read_csv("lol_df.csv")

index_col=[]
for i in range(0, len(df)/5):
    index_col.append(i)
    index_col.append(i)
    index_col.append(i)
    index_col.append(i)
    index_col.append(i)
    
df['index']=index_col
df.head()

########################## 2 ##########################

##group by team and summing the variables
partitioned=df.iloc[::,5:]
summed=partitioned.groupby('index').sum()
#print summed.head()
#print len(summed.columns)

##small test on how to differently partition table
#partitioned=df[:].ix[:,5:]
#summed=partitioned.groupby('index').sum()
#print summed.head()
#print len(summed.columns)


########################## 3 ##########################

#now we want a final df
loldf= pd.DataFrame()

#casting the response variable column into integer
loldf['winner']=[df['winner'][i] for i in range(0,len(df), 5)]

#creating dummy variable columns
side_dummy = pd.get_dummies([df['side'][i] for i in range(1,len(df), 5)], prefix='side')
loldf[[i for i in side_dummy.columns]] = side_dummy
#len(df.columns)

#adding the group-sum data.
loldf[[i for i in summed.columns]]=summed[[i for i in summed.columns]]
#loldf.tail()

####TO ADD A NEW COLUMN, ADD HERE ###



########################## 4 ##########################

#####partitioning the datafile into two, so that each rows are independent
finaldf1=loldf.iloc[::2, :]
#finaldf1.head()
finaldf2=loldf.iloc[1::2, :]
#finaldf2.head()


#####write into csv
with open('finaldf1', 'w', encoding='UTF-8', newline='') as testfile:
            a = csv.writer(testfile, delimiter=',')
            a.writerows(finaldf1)

with open('finaldf2', 'w', encoding='UTF-8', newline='') as testfile:
            a = csv.writer(testfile, delimiter=',')
            a.writerows(finaldf2)
#done!
################################################################################################################################
