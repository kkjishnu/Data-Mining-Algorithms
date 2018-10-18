import numpy as np 
import math
import pandas as pd

data = pd.read_csv('play_tennis.csv', header=0)
print(data.head())

df = pd.DataFrame(data)
print(df.keys())

target = pd.DataFrame(data['play'])
print(target)
df = df.drop(['play'], axis=1)
print(df)

def gini_index(y):
    gini = 1
    value,count = np.unique(y,return_counts=True)
    proportion=count.astype('float')/len(y)

    for i in proportion:
        gini -= math.pow(i,2)

    return gini    

print(gini_index(target))

def gini_split(x,y):
    gs = 0
    value, count = np.unique(x, return_counts=True)
    
    #frequency = count/len(x)

    for i, j in zip(count, value):
        gs += i*gini_index(y[x == j])/len(y)
        

    return gs

print(gini_split(df['outlook'],target))

def best_attr(x, y):
    gs = []
    attr = []
    for x_attr in x:
        gs.append(gini_split(df[str(x_attr)],y))
        attr.append(x_attr)
    bat = np.argmin(gs)
    print(gs)
    
    return bat , attr[bat]

attr_loc, attr_val = best_attr(df,target)
print(attr_loc)
print(attr_val)
