import numpy as np 
import random
import pandas as pd
from itertools import combinations

items_set = ['beer','burger','milk','onion','potato']
max_trn = 20

data=np.random.randint(2, size=(random.randint(1,max_trn),len(items_set)))
df = pd.DataFrame(data)
df.columns = items_set
print(df)    

def candidate_gen(df,items,level,global_freq):

    candidate_set = []
    if level <=1:
        for i in combinations(items,level):            
            p_s = df[list(i)].all(axis=1).sum()
            p_sp = df[list(i)].all(axis=1).sum()/len(df)
            candidate_set.append((",".join(i),p_s,p_sp))      

        candidate_set = pd.DataFrame(candidate_set, columns=["Candidate", "Support","Support %"])

    elif level == 2:
        for i in combinations(items,level):
            p_s = df[list(i)].all(axis=1).sum()
            p_sp = df[list(i)].all(axis=1).sum()/len(df)
            candidate_set.append((i,p_s,p_sp))      

        candidate_set = pd.DataFrame(candidate_set, columns=["Candidate", "Support","Support %"])

    else:  
        sets = []
        i_set = []
        for i in items:
            sets.append(i)
        
        sets = np.unique(sets)  
        
        c = []
        for i in combinations(sets,level):
            c.append(i)
                
        if len(c)!=0:
            
            for i in c:
                ss = subsets(i,level)
                c1 = []
                for k in combinations(items_set,1):
                    c1.append(k)
                if i in ss:
                   ss.pop()
            
                for j in c:
                   if j in ss:
                      ss.remove(j)
                for j in c1:
                    if j in ss:
                        ss.remove(j)  
                
                if all(z in global_freq for z in ss) == True:
                    i_set.append(i)      
        
        
        for i in i_set:
            p_s = df[list(i)].all(axis=1).sum()
            p_sp = df[list(i)].all(axis=1).sum()/len(df)
            candidate_set.append((i,p_s,p_sp))

        candidate_set = pd.DataFrame(candidate_set, columns=["Candidate", "Support","Support %"])     


    return candidate_set 

def subsets(s,level):
    if s == []:
        return [s]
    sets = [s]
    for i in range(0,level):
        tmp_subset = subsets(s[:i]+s[i+1:],i)
        for subset in tmp_subset:
            if subset not in sets:
                sets.append(subset)
    return sets  

def freq_set(candidate_set, min_sup):
    dropdf = []
    for i in range(len(candidate_set)):
        if candidate_set["Support %"][i] < min_sup:
            dropdf.append(i)

    fr_set = candidate_set.drop(candidate_set.index[dropdf])  
    return fr_set

min_sup = float(input("Enter Minimum support : "))
datasets = np.array_split(df, 2)

global_sets = []
global_frequent = []
print(datasets)    
for n in datasets:
    new_df = n
    local_frequent_sets = []
    
    candidate_set = candidate_gen(new_df,new_df[items_set],1,local_frequent_sets)
    print(candidate_set)

    frequent_set = freq_set(candidate_set,min_sup)
    print("Level 1 Frequent Set : \n",frequent_set)
    for y in frequent_set["Candidate"]:
        local_frequent_sets.append(y)

    l = 2
    while l <= len(items_set):
        C = candidate_gen(new_df,frequent_set["Candidate"],l,local_frequent_sets)
        print("Candidate Set of level ",l)
        print(C)  
        L = freq_set(C,min_sup)
        print("Frequent Set of level ",l)
        print(L)
        for o in L["Candidate"]:
            local_frequent_sets.append(o)
        l=l+1   

        if len(L) == 0:
            break 

    print("Frequent Sets :")
    print(local_frequent_sets)
    

    global_sets=set(set(global_sets) | set(local_frequent_sets)) 
print("\nGlobal Candidates :")       
print(global_sets)

c = []
j=0
for i in global_sets:
    if isinstance(i, tuple):
        d = candidate_gen(df,list(i),len(i),global_sets)
        d.index = [j]
        c.append(d)
        j = j+1
    else:
        d = candidate_gen(df,[i],1,global_sets)
        d.index = [j]
        c.append(d)
            
        j=j+1

f = pd.concat(c)
fr = freq_set(f,min_sup)
print("Global Frequent \n",fr)
