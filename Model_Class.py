## I previously used continuous scripts to model and test. 
## But I find this method increasingly inefficient mainly because it's not scalable
## I want to do more wildly fun tests and analysis in bigger scales
## This file creates a class "model" to provide a logit model object for analysis

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from patsy import dmatrices
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn import metrics
from sklearn import linear_model
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import RFE
from sklearn.datasets import make_classification



class model(object):
    
    ###defining dataframe, y & X
    def __init__(self, df):
        self.df = df
        self.y , self.X = dmatrices('winner ~game_cnt + win + loss + win_rate+ kda + kpg + \
                                    dpg+ apg + gpg + ddpg + dtpg + tpg + cs + topsin + kapg + \
                                    newwin + ggg', df, return_type="dataframe")
        self.y = np.ravel(self.y.iloc[::,1:])
    
    
    #returns a model object of the dataframe given
    def modeling(self):
        loggr = LogisticRegression(C=10000000)
        model= RFECV(estimator=loggr, step=1, cv=5)
        model= model.fit(self.X,self.y)
        return model
    
    
    #make a df that could provide info for accuracy prediction depending on 'percentage' threshold
    def thrsh_df(self, percentage):
        to55=[]
        for score in model_obj.predict_proba(self.X)[:,1]:
            if score >= percentage:
                to55.append(1)
            else:
                to55.append(0)

        checkdf=pd.DataFrame()
        checkdf['score']=model.predict_proba(X)[:,1]
        checkdf['prediction']=model.predict(y)
        checkdf['real']=y
        checkdf['to55']=to55
        return checkdf

    
    #returns the accuracy of the prediction depending on 'percentage' threshold
    #win arguement takes 1 for win pred., 0 for loss pred.
    def thrsh_accuracy(self, percentage, win):
        thrsh_df(percentage, win)

        popo=0
        pone=0
        for i in range(0, len(self.df)):
            if df['to55'][i] == win:
                if df['real'][i] == win:
                    popo=popo+1
                else:
                    pone=pone+1
        return float(popo)/float(popo+pone)

    #returns the accuracy score of the test set onto the model you fit.
    def test_score(self, x2, y2):
        return self.model.score(x2, y2)
    
