# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 10:50:09 2019

@author: 黄晶莹
"""
'''for homework1 experient #2'''

import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
os.chdir(r"D:\thu_course2\moving_data_analysis\homework1\ex2")

bs='01077'
#bs='00309'
#bs='00332'
filename='part_'+bs+'.txt'
traffic_volumns=pd.read_table(filename,sep=',',header=None)
traffic_volumns.columns=['time_hour','traffic_volumns_sum']
traffic_volumns.replace("\(","",regex =True,inplace =True)
traffic_volumns.replace("\)","",regex =True,inplace =True)
traffic_volumns=traffic_volumns.astype(np.int64)
traffic_volumns.sort_values(by=["time_hour"],inplace=True)


#  1 plot lines of traffic_volumns vs time(hours) for one base station
plt.figure(figsize=(12,8))
plt.plot(traffic_volumns['time_hour'],traffic_volumns['traffic_volumns_sum'])
#plt.legend(loc='best')#upper left
plt.ylabel('traffic volumns ',fontsize=25)
plt.xlabel("time(hour)",fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.title(bs,fontsize=25)
plt.savefig('plot_location'+bs+'_traffic_volumns_sumEachHour.png',dpi=600)

# 2  trend component & 2.2 periodical component & # 2.2 residual componnent
from statsmodels.tsa.seasonal import seasonal_decompose
traffic_volumns = traffic_volumns.set_index('time_hour')
traffic_volumns_decompose = seasonal_decompose(traffic_volumns['traffic_volumns_sum'], freq=24, two_sided=False)

traffic_volumns['trend'] = traffic_volumns_decompose.trend
traffic_volumns['seasonal'] = traffic_volumns_decompose.seasonal
traffic_volumns['resid'] = traffic_volumns_decompose.resid

def plot_decompose_result(traffic_volumns,col):
    plt.figure(figsize=(12,8))
    plt.plot(traffic_volumns.index,traffic_volumns[col])
    #plt.legend(loc='best')#upper left
    ymin, ymax = plt.ylim() # return the current xlim
    #plt.xlim( 0, ymax ) # set the xlim to xmin, xmax
    plt.ylim( 0, ymax) # set the ylim to xmin, xmax
    plt.ylabel(col+' of traffic volumns ',fontsize=25)
    plt.xlabel("time(hour)",fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.title(bs,fontsize=25)

    plt.savefig(col+'_bin24_location'+bs+'_traffic_volumns_sumEachHour.png',dpi=600)

plot_decompose_result(traffic_volumns,'trend')
plot_decompose_result(traffic_volumns,'seasonal')
#plot_decompose_result(traffic_volumns,'resid')
col='resid'
plt.figure(figsize=(12,8))
plt.plot(traffic_volumns.index,traffic_volumns[col])
#plt.legend(loc='best')#upper left
ymin, ymax = plt.ylim() # return the current xlim
#plt.xlim( 0, ymax ) # set the xlim to xmin, xmax
#plt.ylim( 0, ymax) # set the ylim to xmin, xmax
plt.ylabel(col+' of traffic volumns ',fontsize=25)
plt.xlabel("time(hour)",fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.title(bs,fontsize=25)
plt.savefig(col+'_bin24_location'+bs+'_traffic_volumns_sumEachHour.png',dpi=600)

