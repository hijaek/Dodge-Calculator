import matplotlib
import numpy as np
import sklearn
from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


##first trying with logistic regression
df = pd.read_csv("finaldf1.csv", )


print df.describe()
print pd.crosstab(df['admit'], df['prestige'])


df.hist()
