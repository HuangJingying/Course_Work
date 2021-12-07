# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:10:23 2019

@author: 黄晶莹
"""
'''for homework1 experient #3 '''
import os
import pandas as pd
import numpy as np
import copy
from matplotlib import pyplot as plt

os.chdir(r"D:\thu_course2\moving_data_analysis\homework1\ex3")

# file get from hdfs
list_data=pd.read_table("hw1_ex3_countsof_edges_per_hour_allBSs_.txt",skiprows=1,
                        names=['use_ID','use_ID.1','Weight'],sep="\t",
                        dtype={'use_ID':str,'use_ID.1':str})
list_data.columns
list_data.shape

list_data2=copy.deepcopy(list_data)

list_data2.loc[list_data['use_ID']>list_data['use_ID.1'],'use_ID']=list_data.loc[list_data['use_ID']>list_data['use_ID.1'],'use_ID.1']
list_data2.loc[list_data['use_ID']>list_data['use_ID.1'],'use_ID.1']=list_data.loc[list_data['use_ID']>list_data['use_ID.1'],'use_ID']

# get final data : edge(usr_id,user_id)-weight
data=pd.pivot_table(list_data2,index=['use_ID','use_ID.1'],values=['Weight'],aggfunc=np.sum)
data.to_csv("hw1_ex3_countsof_edges_per_hour_allBSs_corrected.txt",sep="\t",index=True,header=False)

# reread file
data=pd.read_table("hw1_ex3_countsof_edges_per_hour_allBSs_corrected.txt",skiprows=1,
                        names=['use_ID','use_ID.1','Weight'],sep="\t",
                        dtype={'use_ID':str,'use_ID.1':str})
data.shape

'''-----------------------graph analysis-----------------'''
#----------get number of nodes
data2=copy.deepcopy(data)
data2.columns=['use_ID.1','use_ID','Weight']

nodes=pd.concat([data[['use_ID']].drop_duplicates(),data2[['use_ID']].drop_duplicates()],axis=0,sort=True).drop_duplicates()
nodes.shape #(29238, 1)
# ----------get number of edges/links
len(data[['Weight']]) #116575
nodes.loc[0,'number of nodes']=len(data[['Weight']])
nodes.to_csv("hw1_ex3_number_of_nodes.txt",sep='\t',index=False)
#-----------average_degree 
#度(Degree)：所有与它连接点的个数之和
#度（Degree）：节点的度是指与其相连的边数，如果一个节点有3个边，那么这个节点的度就是
#无向图：所有点的度数总和/节点数。节点的度越高，连接它的点就越多，说明该点越关键。
degree1=pd.pivot_table(data,index=['use_ID'],values=['use_ID.1'],aggfunc="count")
degree1.columns=['degree1']
degree2=pd.pivot_table(data,index=['use_ID.1'],values=['use_ID'],aggfunc="count")
degree2.columns=['degree2']

degree_each_node=pd.merge(degree1,degree2,left_index=True,right_index=True,how='outer')
degree_each_node.fillna(0,inplace=True)
degree_each_node['degree']=degree_each_node['degree1']+degree_each_node['degree2']
average_degree=np.sum(degree_each_node['degree'])/len(nodes)
average_degree #7.9742116423832
# save file
degree_each_node.reset_index(inplace=True)
degree_each_node.columns=['user_id', 'degree1', 'degree2', 'degree']
degree_each_node.sort_values(by=['degree'],inplace=True,ascending=False)
degree_each_node.reset_index(inplace=True)
degree_each_node.loc[0,'average_degree']=average_degree
degree_each_node[['user_id','degree','average_degree']].to_csv("hw1_ex3_degree_each_node.txt",sep='\t',index=False)

plt.figure(figsize=(12,8))

plt.hist(degree_each_node['degree'],bins=100,rwidth=1,alpha=0.6, log=True)
plt.xlabel('degree',fontsize=25)
plt.ylabel("number of degree",fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.title("distribution of node's degree",fontsize=25)
plt.axvline(average_degree,color='black',label='average degree:7.97')
plt.legend()
plt.savefig('plot_distribution_of_user_degree.png',dpi=600)



#-------------------graph diameter & average path length

#使用x个节点到其他所有节点距离，然后取平均，作为近似值(x>2)
#分别计算距离某节点一跳的节点个数，二跳的节点个数

alldata=pd.concat([data,data2],axis=0,sort=True).drop_duplicates()

num_of_link=2
def get_links(links1,remove_id):
    links2=pd.merge(links1,alldata[['use_ID','use_ID.1']],left_on='use_ID.1',right_on='use_ID.1',
                    suffixes=['','.'+str(num_of_link)],how='left')
#    

    aa =set(remove_id)
    bb = set(links2.iloc[:,-1])
    #求差集，在B中但不在A中
    userid_diff = list(bb.difference(aa))#
    links2_result=pd.DataFrame(user,columns=['use_ID'],index=range(len(userid_diff)))
    links2_result['use_ID.1']=userid_diff

    return links2_result

average_path_to_allusers=pd.DataFrame(index=range(2000),columns=['user_ID','average_path_to_allusers'])

number_OF_nodes=len(nodes)
user_list=np.random.randint(0,number_OF_nodes,2000)
for index in range(2000):
    user=nodes.iloc[user_list[index],0]
    print(index)
    #26036
    #user='110884'
    average_path_to_allusers.loc[index,'user_ID']=user
    links1=alldata[alldata['use_ID']==user].iloc[:,1:3]
    remove_id=list(set(links1.iloc[:,0]))+list(set(links1.iloc[:,1]))
    i=1
    path_to_alluser=(len(remove_id)-1)*1
    while ((len(remove_id)<number_OF_nodes)&(len(remove_id)>0)):
        
        
        links2_result=get_links(links1,remove_id)
        remove_id2=list(remove_id+list(set(links2_result.iloc[:,1])))
        print('remove_id:',len(remove_id2))
        i=i+1
        path_to_alluser=path_to_alluser+(len(remove_id2)-len(remove_id))*i
        print('average_path_one_user',i,path_to_alluser)
        links1=copy.deepcopy(links2_result)
        remove_id=remove_id2


    average_path_to_allusers.loc[index,'average_path_to_allusers']=path_to_alluser/(number_OF_nodes-1)

average_path_to_allusers.loc[0,'Approximate diameter']=np.sum(average_path_to_allusers['average_path_to_allusers'])/2000

average_path_to_allusers.to_csv("hw1_ex3_average_path_to_allusers.txt",sep='\t',index=False)

average_path_to_allusers=pd.read_table("hw1_ex3_average_path_to_allusers.txt",sep='\t')

plt.figure(figsize=(12,8))

plt.hist(average_path_to_allusers.loc[:,'average_path_to_allusers'],bins=100,range=(1,8),rwidth=1,alpha=0.6, log=True)
plt.xlabel('average path length',fontsize=25)
plt.ylabel("",fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.title("distribution of average path length",fontsize=25)
plt.axvline(average_path_to_allusers.loc[0,'Approximate diameter'],color='black',label='Approximate diameter:'+str(average_path_to_allusers.loc[0,'Approximate diameter'].round(2)))
plt.legend()
plt.savefig('plot_distribution_of_average_path_length.png',dpi=600)




    
# plot the complementary cumulative distribution function互补累积分布函数 of user's
# degree in the contact graph , and using a suitable distribution to do curve fitting.

# get distribution of degree
degree_each_node['number of occurrences']=degree_each_node['degree']
degree_counts=pd.pivot_table(degree_each_node,values=['number of occurrences'],index=['degree'],aggfunc="count")


##  plot CCDF

s=degree_counts.sum()
cdf = degree_counts.cumsum(0)/s #from https://gist.github.com/yamaguchiyuto/504eb5482fc73f046f6b
#plt.plot(cdf.index,cdf.iloc[:,0])
ccdf = 1-cdf
 
plt.figure(figsize=(12,8))
plt.plot(np.log10(ccdf.index),np.log10(ccdf.iloc[:,0]),label='CCDF')
a,b = np.polyfit(np.log10(ccdf.index[:-1]),np.log10(ccdf.iloc[:-1,0]),1) 
x=np.random.rand(100)*2.8
plt.plot(x,a*x+b,'--',alpha=0.6,label='y='+str(a.round(2))+'x+'+str(b.round(2)))
plt.xlabel('log10(degree)',fontsize=25)
plt.ylabel("log10(CCDF)",fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.legend(fontsize=15)
plt.savefig('plot_CCDF_of_user_degree2.png',dpi=600)

#---- caculate the clustering coefficient of the 5 top users with the largest node degree
degree_each_node['user_id'].head(5)
#5        000009
#26144    131916
#23801    122166
#8597     049993
#1        000002


# 目标节点邻居节点相连的概率
clustering_coefficient_pd=pd.DataFrame(index=range(5),columns=['user_id','user_degree','clustering_coefficient'])
for index in range(5):
    print(index)
    user=degree_each_node.loc[index,'user_id']
    clustering_coefficient_pd.loc[index,'user_id']=user
    clustering_coefficient_pd.loc[index,'user_degree']=degree_each_node.loc[index,'degree']
    ## 目标节点的邻居节点的个数N
    links1=alldata[alldata['use_ID']==user].iloc[:,1:3]
    nerbors=sorted(links1.iloc[:,1])
    # N个邻居节点间存在边的个数为M
    nerbor_link=data[(data['use_ID'].isin(nerbors)& data['use_ID.1'].isin(nerbors))]
    # 聚类系数M/(N(N-1) *2
    clustering_coefficient_pd.loc[index,'clustering_coefficient']=len(nerbor_link)/(len(nerbors)*(len(nerbors)-1)/2)
clustering_coefficient_pd.to_csv("hw1_ex3_clustering_coefficient_of_5_top_user.txt",sep='\t',index=False)



# finish



