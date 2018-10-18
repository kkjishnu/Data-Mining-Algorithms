import numpy as np 
import random


data = [1, 2, 3, 5, 9, 11, 4, 15, 17, 20, 21]

k = 2

def medoids(k,data):
    medoid = []
    for i in range(k):
        medoid.append(random.choice(data))
    return medoid

def distance(a,b):
    return abs(b-a)

current_medoid = medoids(k,data)
print(current_medoid)

def dist_matrix(current_medoid):
    dist = []
    for i in current_medoid:
        temp_dist = []
        for j in data:
            temp_dist.append(distance(i,j))
        dist.append(temp_dist)      

    return dist

distances = dist_matrix(current_medoid)
print(distances)
distances1 = np.vstack(np.array(distances).T)
print(distances1)

def assign(medoids, distances,data):
    cluster = dict.fromkeys(medoids)
    dist = []
    for i in range(len(data)):
        d = np.argmin(distances[i])
        dist.append(np.min(distances[i]))
        if cluster[medoids[d]] is None:
            cluster[medoids[d]] = [data[i]]
        else:
            cluster[medoids[d]].append(data[i])         
    return cluster, dist    

clusters1, distances1 = assign(current_medoid,distances1,data)

print(clusters1)

new_medoid = medoids(k,data)
print(new_medoid)
distances = dist_matrix(new_medoid)
distances2 = np.vstack(np.array(distances).T)
print(distances2)

def cal_change(data,distances1,distances2):
    changes = []
    for i in range(len(data)):
        changes.append(distances1[i] - np.min(distances2[i]))
    return changes

change = cal_change(data,distances1,distances2)
print(np.sum(change))

while np.sum(change) < 0:
    cl1, d1 = assign(new_medoid,distances2,data)
    new_medoid = medoids(k,data)
    print(new_medoid)
    distances = dist_matrix(new_medoid)
    distances2 = np.vstack(np.array(distances).T)
    print(distances2)
    change = cal_change(data,d1,distances2)
    print(np.sum(change))

    print(cl1)