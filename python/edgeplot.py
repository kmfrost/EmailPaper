import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import re
import numpy as np

from math import log

#column_labels = list('ABCD')
#row_labels = list('WXYZ')
#data = np.random.rand(4,4)


edges=[]

def read_edgelist():
    with open('full_edgelist.csv','rb') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            d=dict()
            temp=re.split(' ',row[0])
            d['src']=temp[0]
            d['dst']=temp[1]
            d['num']=temp[2]
            edges.append(d)
    return edges

def read_job():
    jobs=[]
    with open('test_status.csv','rb') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            d=dict()
            temp=re.split(' ',row[0])
            d['pid']=temp[0]
            d['job']=temp[1]
            jobs.append(d)
    return jobs

def edge2mat(edges,people):
    data=np.zeros((len(people),len(people)))

    for i in range(len(people)):
        for j in range(len(people)):
            res=filter(lambda x:(x['src']==people[i] and x['dst']==people[j]),edges)
            if len(res)==0:
                pass
            elif len(res)==1:
                data[i][j]=log(float(res[0]['num']))
                #data[i][j]=res[0]['num']
            else:
                raise Exception('Should not have multiple entries')
    return data

def makeplot(data,people):
    fig, ax = plt.subplots()
    #heatmap = ax.pcolor(data, cmap=plt.get_cmap("Blues"))
#    heatmap = ax.pcolor(data, cmap=plt.cm.seismic)
#    heatmap = ax.pcolor(data, cmap=plt.cm.nipy_spectral)
    heatmap = ax.pcolor(data, cmap=plt.cm.jet)


    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    ax.set_xticklabels(people, minor=False, rotation='vertical')
    ax.set_yticklabels(people, minor=False)

    ax=plt.gca() #get the current axes
    PCM=ax.get_children()[2] #get the mappable, the 1st and the 2nd are the x and y axes
    cb = plt.colorbar(PCM, ax=ax) 
    cb.set_label(r'Emails Sent ($\log_{10}$ scale)')

    
if __name__=='__main__':
    edges=read_edgelist()
    jobs=read_job()

    src_people=set(map(lambda x:x['src'],edges))
    dst_people=set(map(lambda x:x['dst'],edges))
    people=sorted(list(src_people.union(dst_people)))
    people_dict=[]
    for i in range(len(people)):
        d=dict()
        d['pid']=people[i]
        d['role']=filter(lambda x:x['pid']==people[i],jobs)[0]['job']
        people_dict.append(d)

    people_dict_sorted=sorted(people_dict,key=lambda x:x['role'])
    for i in range(len(people_dict_sorted)):
        print people_dict_sorted[i]['role']

    data=edge2mat(edges,map(lambda x:x['pid'],people_dict_sorted))
    
    makeplot(data,map(lambda x:x['role'],people_dict_sorted))

    plt.show()
