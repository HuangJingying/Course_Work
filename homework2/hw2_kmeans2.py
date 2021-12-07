# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 15:15:49 2019

@author: 黄晶莹
"""

import numpy as np 
import torch
import pandas as pd
from matplotlib import pyplot as plt

import os

os.chdir(r"D:\thu_course2\moving_data_analysis\homework2")
#-------------read data
volumns=pd.read_table("hw2_sum_traffic_volumns_per_hour_of_allBSs_foldtoWeek.txt",sep=',',header=None)

volumns.replace("\(","",regex =True,inplace =True)
volumns.replace("\)","",regex =True,inplace =True)

volumns.columns=['time','location_id','traffic_volumns']

volumns[['time','traffic_volumns']]=volumns[['time','traffic_volumns']].astype(np.int64)
##---normalization z-score
##3)	标准化，（traffic volumns (每小时)-对所有基站求平均值）/标准差
#volumns_average=pd.pivot_table(volumns,index=["time"],values=["traffic_volumns"],aggfunc=[np.mean,np.std])
##test=volumns[volumns['time']==1]
##np.std(test["traffic_volumns"],ddof=1)
##---get average
#volumns['norm_traffic_volumns']=(volumns['traffic_volumns']-volumns_average.iloc[:,0])/volumns_average.iloc[:,1]
#
##save
#volumns.to_csv("hw2_sum_traffic_volumns_per_hour_of_allBSs_foldtoWeek_norm.txt",sep='\t',index=False)

# -----------dataframe transfer
volumns_trans=volumns[volumns['time']==0]
volumns_trans.columns=['time','location_id',str(0)+'h']
volumns_trans=volumns_trans[['location_id',str(0)+'h']]
timelist=sorted(volumns['time'].drop_duplicates())
for hour in timelist[1:]:
    print(hour)
    volumns_hour=volumns[volumns['time']==hour]
    volumns_hour.columns=['time','location_id',str(hour)+'h']
    volumns_trans=pd.merge(volumns_trans,volumns_hour[['location_id',str(hour)+'h']],on='location_id',how='outer')

#--fill nan with 0
volumns_trans.fillna(0,inplace=True)   

#-----------norm by z-score
volumns_trans.index=volumns_trans['location_id']
volumns_trans.pop('location_id')
#标准化，（traffic volumns (每小时)-对所有基站求平均值）/标准差
#计算各列数据总和并作为新列添加到末尾
#df['Col_sum'] = df.apply(lambda x: x.sum(), axis=1)
volumns_trans.loc['average']=volumns_trans.apply(lambda x: x.mean(), axis=0)
volumns_trans.loc['average']
volumns_trans.loc['std']=volumns_trans.apply(lambda x: x.std(), axis=0)
volumns_trans.loc['std']
#volumns_trans.pop('average')
volumns_trans_norm=(volumns_trans.iloc[:-2,:]-volumns_trans.loc['average'])/volumns_trans.loc['std']
volumns_trans_norm.to_csv("hw2_sum_traffic_volumns_per_hour_of_allBSs_foldtoWeek_norm.txt",sep='\t',index=True)
#=======================================================================================

#volumns_trans_norm=pd.read_table("hw2_sum_traffic_volumns_per_hour_of_allBSs_foldtoWeek_norm.txt",sep='\t',index=0)


##=========--testing data
#df=np.random.randint(low=0,high=1000000000,size=(1000,168))
#
##--randomly select k points as cluster centroids
#init_center_index = np.random.choice(np.arange(df.shape[0]), size=10)
#
#init_center = df[init_center_index,:]
#=============================================
#--caculate N-K points to each centroid distance 
def cal_dist(data, center):
    '''
    Input:
        data: N x dim N is the total number of data points
        center: K x dim K is the number of center 
    Return: N x K which are distances from N points to the K centers 
    '''
    # To ensure that the center has the shape of k x 1 x dim for get distance

#    print(data.dtype)
    data = torch.tensor(data)
    center = torch.tensor(center)
    center = torch.reshape(center, [center.shape[0],1, -1])   # ! reshape: 3dim: k,1,dim(168)
    # get Euclidean distance
    diff = data - center  # Nx168-Kx1x168=KxNx168
    dist = np.sqrt(torch.sum(diff**2, dim=2))  # dim=2: sum for third dim  =KxN
    dist = dist.t()  # NxK
    
    return dist.data.cpu().numpy()

#cal_dist(df,init_center)
#计算新、旧中心点的距离
def cal_center_dist(old_center, new_center, thresh):
    error = 0
    square = (old_center - new_center)**2    # square num_centers x 168
    dist = np.sqrt(np.sum(square, axis=1))   #前一次和这一次的聚类中心的欧氏距离  dist num_centers x 1
    print(dist)
    error = np.sum(dist > thresh)
    print(error)
    return error == 0
    
#聚类    
def k_means(data, num_clusters, num_iters, thresh_hold=0.00001):
    '''data:Nx168'''
    #init center/K point
    init_center_index = np.random.choice(np.arange(data.shape[0]), size=num_clusters)
    #init center point
    init_center = data[init_center_index, :]
    new_center = init_center.copy()
    
    
    #--aassign N-K points to cluster 
    # 迭代
    for i in range(num_iters):
        init_center = new_center.copy()
        #cal dis between all point to all center
        dist = cal_dist(data, init_center)
        #--get the min distance from point to centroid
        bs_center_index = np.argmin(dist, axis=1) # argmax return min's index of each row(axis=1)
        #--assign 
        for j in range(num_clusters):
            #choose points which belong to the j th cluster
            cluster_points = data[(bs_center_index==j).nonzero(),:] # nonzero: return True's index
            cluster_points=cluster_points.squeeze()
            #update the cluster center  
            print(cluster_points.shape)
            new_center[j, :] = np.mean(cluster_points,axis=0) 
            print(np.mean(cluster_points,axis=0).shape)
        if cal_center_dist(init_center, new_center, thresh_hold):
            print("error is 0")
            break
        
    return new_center


# 计算每一个聚类的半径 每一个聚类里面的点到聚类中心的距离的平均值
def cal_cluster_radius(data, cluster_centers):
    '''
    input:
        data: N x 168        all data points
        cluster_centers: n_cluster x 168       all cluster center points
    return:
        cluster_radius: 1 x cluser_centers_num    each cluster;s radius
    '''
    cluster_radius = np.zeros([1, cluster_centers.shape[0]])
     
    dist = cal_dist(data, cluster_centers)
    bs_center_index = np.argmin(dist, axis=1)
     
    for i in range(cluster_centers.shape[0]):
        cluster_points = data[(bs_center_index==i).nonzero(),:]
        cluster_points=cluster_points.squeeze()
        cluster_dist = cal_dist(cluster_points, cluster_centers[i].reshape([1, -1]))
        #print('center dist shape',cluster_dist.shape)
        cluster_radius[0,i] = cluster_dist.mean()
    return cluster_radius


# 计算每一个聚类的点的数目
def cal_cluster_points_num(data, cluster_centers):
    '''
    input:
        data: N x 168   all data points
        cluster_center: n_cluster x 168   all cluster center points
    return:
        cluster_nums: 1 x cluster_centers_num   each cluser's data points number
    '''
    cluster_nums = np.zeros([1,cluster_centers.shape[0]])
    dist = cal_dist(data, cluster_centers)
    bs_center_index = np.argmin(dist, axis=1)
    for i in range(cluster_centers.shape[0]):
        points_num = (bs_center_index==i).nonzero()[0].shape[0]
        cluster_nums[0,i] = points_num
    return cluster_nums


##---get k curve
#k_curve=pd.DataFrame(columns=['average distance to centroid'],index=range(2,25))
#for i in range(2,25):
#    print(i)
#    numofcluster=i
#    result_center=k_means(volumns_trans_norm.iloc[:,:].values,numofcluster,1000,0.00001)
#    result_center_radius=cal_cluster_radius(volumns_trans_norm.iloc[:,:].values,result_center)
#    k_curve.iloc[i-2,0]=np.sum(result_center_radius)/numofcluster
#


#plt.figure(figsize=(12,8))
#plt.plot(k_curve)
##plt.legend(loc='best')#upper left
#plt.ylabel(k_curve.columns,fontsize=25)
#plt.xlabel("k",fontsize=25)
#plt.xticks(fontsize=25)
#plt.yticks(fontsize=25)
#plt.ylim(0,10)
#
#plt.title("centroid_NO."+str(center_NO),fontsize=25)
#plt.savefig('plot_centroid_NO_'+str(center_NO)+'_traffic_volumns_EachHour.png',dpi=600)

numofcluster=20
result_center=k_means(volumns_trans_norm.iloc[:,:].values,numofcluster,1000,0.0000001)
pd.DataFrame(result_center).to_csv("hw2_centroid_of_"+str(numofcluster)+"_cluster.txt",sep='\t',index=True)

result_center_radius=cal_cluster_radius(volumns_trans_norm.iloc[:,:].values,result_center)
pd.DataFrame(result_center_radius).to_csv("hw2_radius_of_"+str(numofcluster)+"_cluster.txt",sep='\t',index=True)

result_center_point=cal_cluster_points_num(volumns_trans_norm.iloc[:,:].values,result_center)
pd.DataFrame(result_center_point).to_csv("hw2_point_num_of_"+str(numofcluster)+"_cluster.txt",sep='\t',index=True)

#remove norm and get center_traffic_volumns
center_traffic=pd.DataFrame(result_center,columns=volumns_trans.columns)#.apply(lambda x: print (x),axis=1)#
center_traffic_volumns=center_traffic*volumns_trans.loc['std']+volumns_trans.loc['average']
center_traffic_volumns.columns=range(168)
#  plot lines of traffic_volumns vs time(hours) for one centroid
def plot_center_traffic(center_traffic,center_NO):
    plt.figure(figsize=(12,8))
    plt.plot(center_traffic.columns,center_traffic.iloc[center_NO,:])
    #plt.legend(loc='best')#upper left
    plt.ylabel('traffic volumns ',fontsize=25)
    plt.xlabel("time(hour)",fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
#    plt.xlim(0,168)
    plt.title("centroid_NO."+str(center_NO),fontsize=25)
    plt.savefig('plot_centroid_NO_'+str(center_NO)+'_traffic_volumns_EachHour.png',dpi=600)
    
plot_center_traffic(center_traffic_volumns,0)

for i in range(numofcluster):
    plot_center_traffic(center_traffic_volumns,i)
