import pandas as pd
import numpy as np

data = pd.read_csv('play_tennis.csv', header=0)
print(data.head())

df = pd.DataFrame(data)
print(df.keys())

target = pd.DataFrame(data['play'])
print(target)
df = df.drop(['play'], axis=1)
print(df)

# Calculate Entropy


def entropy(s):
    ent = 0
    # Find unique values and their count
    # np.unique()'s return_counts argument returns the count of each unique element
    value, count = np.unique(s, return_counts=True)

    frequency = count/len(s)
    #print(frequency)
    for i in frequency:
        if i != 0:
            ent -= i * np.log2(i)
    return ent


#print(entropy(target))


def info_gain(x, y):
    gain = entropy(y)

    value, count = np.unique(x, return_counts=True)
    
    frequency = count/len(x)

    for i, j in zip(frequency, value):
        gain -= i*entropy(y[x == j])

    return gain
#Calculates the best attribute based on info gain
def best_attr(x, y):
    gain = []
    attr = []
    for x_attr in x:
        gain.append(info_gain(df[str(x_attr)],y))
        attr.append(x_attr)
    bat = np.argmax(gain)
    
    return bat , attr[bat], gain

attr_loc, attr_val, gain = best_attr(df,target)

'''returns a dictionary containing unique values of the best attribute as key and their corresponding 
index as keys''' 
def part(attr):
    new_df = {}
    for i in np.unique(attr):
        new_df[i] = (attr==i).nonzero()[0]
    return new_df

#fn to recursively split the decision tree based on best attribute
def split(x,y):
    if len(y) == 0 or len(y)==1:
        return y

    attr_loc, attr_val, gain = best_attr(x,y)

    ds = part(x.iloc[:,attr_loc])
    #print(ds)

    if np.all(np.array(gain) < 0.001):
        return y
  
    new_df =[]
    new_y = []
    for i,j in ds.items():
        y_sub = y.take(j,axis=0)
        x_sub = x.take(j,axis = 0)
        new_df.append(x_sub.drop([attr_val],axis=1))
        new_y.append(y_sub)
        
    #for i,j in zip(new_df,new_y):
        #print(i,j)
    result={}
    result[attr_val] = {}
    for i in range(0,len(new_df)):
        result[attr_val]["X_%s=%s"%(attr_val,i)]= split(new_df[i],new_y[i])
    return result    
    
result = split(df,target)    
print(result)
