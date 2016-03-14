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


def addindex(dfr):
    index_col=[]
    for i in range(0, len(dfr)/5):
        index_col.append(i)
        index_col.append(i)
        index_col.append(i)
        index_col.append(i)
        index_col.append(i)
    dfr['index']=index_col

#addindex(df)
#addindex(hikari)

########################## 2 ##########################

##group by team and summing the variables
def hijaeframe(dfr):
    ##groupby index and sum
    partitioned=dfr.iloc[::,5:]
    summed=partitioned.groupby('index').sum()
    
    #final dataframe
    loldf= pd.DataFrame()
    loldf['winner']=[dfr['winner'][i] for i in range(0,len(dfr), 5)]
    
    #side - dummy variable
    side_dummy = pd.get_dummies([dfr['side_1'][i] for i in range(1,len(dfr), 5)], prefix='side')
    loldf[[i for i in side_dummy.columns]] = side_dummy
    
    loldf[[i for i in summed.columns]]=summed[[i for i in summed.columns]]
    loldf['newwin']=(loldf['win']/loldf['game_cnt'])*100
    loldf['topsin']=loldf['tpg']*(loldf['kpg']+loldf['apg'])
    loldf['ggg']=( (loldf['ddpg']-(loldf['cs']*350)) / (loldf['dpg']) )
    return loldf

model_blue = hijaeframe(df).iloc[::2, :]



def hijaelogr(dfr):
    logr = sm.Logit(dfr['winner'], dfr[['newwin','topsin','kpg','dpg','apg','ggg']]) #:10]|blue.columns[14:]])
    return logr


###  make this into class-objects later
### 
hijaem = hijaelogr(model_blue).fit()
print hijaem.summary()
print np.exp(hijaem.params)


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
loldf= pd.DataFrame()


loldf['winner']=[df['winner'][i] for i in range(0,len(df), 5)]
#creating dummy variable columns

side_dummy1 = pd.get_dummies([df['side_1'][i] for i in range(1,len(df), 5)], prefix='side1')
#side_dummy2 = pd.get_dummies([df['side_2'][i] for i in range(1,len(df), 5)], prefix='side2')

loldf[[i for i in side_dummy1.columns]] = side_dummy1
#loldf[[i for i in side_dummy2.columns]] = side_dummy2

len(df.columns)
#adding rest of columns
loldf[[i for i in summed.columns]]=summed[[i for i in summed.columns]]

loldf['newwin']=(loldf['win']/loldf['game_cnt'])*100
loldf['topsin']=loldf['tpg']*(loldf['kpg']+loldf['apg'])
loldf['dpd']=( (loldf['ddpg']-(loldf['cs']*900) ) / (loldf['dpg']) ) / 1000

loldf.head(2)
#yay done!
################################################################################################################################
