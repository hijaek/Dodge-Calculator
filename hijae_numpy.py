import numpy as np
import pandas as pd

data={
	'game1': {
		'hijae': ['kda','gold','kill','death'],
		'puree': ['kda','gold','kill','death']
		},

	'game2':	{
		'hijae': ['kda','gold','kill','death'],
		'puree': ['kda','gold','kill','death']
		}
    }

data2={
		'game1': [['hijae','kda','gold','kill','death'],
				  ['puree', 'kda','gold','kill','death']]
}
s = pd.Series(pd.Series(pd.Series(data2)))

mydict= dict()
mydict[1]=[]
print(data2['game1'][0])



