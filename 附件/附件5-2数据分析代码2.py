# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 23:33:01 2018

@author: 黄晶莹
"""

import os
import numpy as np
import pandas as pd

from datetime import datetime
#from datetime import timedelta
#设置路径
os.chdir(r"D:\thu_course\fundamental_system_of_big_data\r_clean\new_all")
#读入文件
filename='final_ready.xlsx'
book=pd.read_excel(filename,header=0)
df=pd.DataFrame(book)

'''计算还款时间'''
df['还款时间']=df['到款时间']-df['填充后汇款日期']
print(df['还款时间'])

'''删除负的还款时间：国外供应商'''
#delta_t_lt1day = delta_t[delta_t < pd.Timedelta(1,'D')]
df=df[df['还款时间'] >= pd.Timedelta(1,'D')]
print(df.shape)
#print(df.info())
print(df.columns)
#写入xlsx
filename2='12_11/remove_negatime_all_final.xlsx'
df.to_excel(filename2, sheet_name='all')
#(3828, 33)
#Index(['ID', '业务单编号', '企业代码', '成本确认单编号', '客户单位名称', '收入确认单编号', '供应商名称', '供应商代码',
#       '费目名称', '起始节点', '终止节点', '实际付款金额', '填充后汇款日期', '实际到款金额', '到款时间', '回款时间',
#       '收款总金额', '收款申请单编号', '收入核销日期', '成本核销日期', '企业类型', '企业分类', '客户级别',
#       '最终注册资本', '成立日期', '公司类型', '所属行业', '所属地区', '物流方向', '联运方式代码', '业务单总价',
#       '总成本', '还款时间'],
#      dtype='object')
'''数据透视'''
'''中铁每天垫款金额'''
'''单日合计垫款金额'''
df1=df[['企业代码','成本确认单编号','填充后汇款日期','实际付款金额']]
#去重复
df1.drop_duplicates(['企业代码','成本确认单编号','填充后汇款日期','实际付款金额'],keep='first',inplace=True)
#[654 rows x 4 columns]
df_pivot1=pd.pivot_table(df1,index=["填充后汇款日期"],values=['实际付款金额'],aggfunc=np.sum)
print(df_pivot1.head(3))
filename2='12_11/daily_diankuanjine.xlsx'
df_pivot1.to_excel(filename2, sheet_name='daily_diankuanjine') 
'''日账目概念'''
'''累加垫款'''
df2=df[['企业代码','成本确认单编号','填充后汇款日期','实际付款金额', '到款时间',
      '实际到款金额', '收入确认单编号']]
df2=df2.drop_duplicates(['企业代码','成本确认单编号','填充后汇款日期','实际付款金额', '到款时间',
      '实际到款金额', '收入确认单编号'],keep='first',inplace=False)
#Reindexing after pandas.drop_duplicates
df2 = df2.reset_index(drop=True)
print(df2.head(10))
filename2='12_11/for_rizhangmu2.xlsx'
df2.to_excel(filename2, sheet_name='for_rizhangmu2')
#[1432 rows x 8 columns]


#df_pivot1=pd.pivot_table(df1,index=["收款申请单编号"],values=['收款总金额','到款时间'],aggfunc=np.sum)
#print(df_pivot1.head(3))
#filename2='12_11/daily_diankuanjine.xlsx'
#df_pivot1.to_excel(filename2, sheet_name='daily_diankuanjine') 


df3=df2[['企业代码','填充后汇款日期','实际付款金额', '到款时间','实际到款金额','收入确认单编号']]
#排序
#pd.sort_values("xxx",inplace=True)
df3.sort_values(by=['收入确认单编号','填充后汇款日期'],inplace=True)
df4=df3.drop_duplicates(['收入确认单编号'],keep='first',inplace=False)
df4 = df4.reset_index(drop=True)
#def datelist(beginDate, endDate): 
#    # beginDate, endDate是形如‘20160601’的字符串或datetime格式 
#    date_l=[datetime.strftime(x,'%Y-%m-%d %H:%M:%S') for x in list(pd.date_range(start=beginDate, end=endDate))] 
#    return date_l
#datalist=datelist('20180316 00:00:00','20181018 00:00:00')
#result1=pd.DataFrame(datalist,columns=['日期'])


result2=pd.DataFrame(list(pd.date_range(start='20180316 00:00:00', end='20181018 00:00:00')),columns=['日期'])
#result_qiye=pd.DataFrame(columns=list(pd.date_range(start='20180316 00:00:00', end='20181018 00:00:00')),index=range(150))
result_qiye2=pd.DataFrame(columns=['日期','企业代码','实际到款金额'],index=range(30000))
#j=0
#def caculate_jine(col,data,df3):
#    result=0
#    
#    din = datetime.strptime(str(data), '%Y-%m-%d %H:%M:%S')
#    for i in range(len(df3['填充后汇款日期'])):
#        dqian = datetime.strptime(str(df3.ix[i,'填充后汇款日期']), '%Y-%m-%d %H:%M:%S')
#        dhou = datetime.strptime(str(df3.ix[i,'到款时间']), '%Y-%m-%d %H:%M:%S')
#        if (dqian-din) <= pd.Timedelta(0,'D'):
#            if (dhou-din) > pd.Timedelta(0,'D'):
#                result = result+df3.ix[i,'实际到款金额']
#                #print(j,col)
#                result_qiye2.ix[j,'日期']=data
#                result_qiye2.ix[j,'企业代码']=df3.ix[i,'企业代码']
#                result_qiye2.ix[j,'实际到款金额']=df3.ix[i,'实际到款金额']
#                j=j+1
#                #print(result_qiye2.ix[j,:])
#
#    return result
#                    
#
#for i in range(len(result2['日期'])):
#    datatime=result2.ix[i,'日期']
#    jin_e = caculate_jine(i,datatime,df3)
#    result2.ix[i,'单日累计金额']=jin_e

#test =caculate_jine(result2.ix[0,'日期'],df3)
#jin_e = caculate_jine(0,result2.ix[0,'日期'],df3)

def caculate_jine(datamatrix,df3):

    j=0
    for m in range(len(datamatrix['日期'])):
        result=0
        data=datamatrix.ix[m,'日期']
        din = datetime.strptime(str(data), '%Y-%m-%d %H:%M:%S')
        for i in range(len(df3['填充后汇款日期'])):
            dqian = datetime.strptime(str(df3.ix[i,'填充后汇款日期']), '%Y-%m-%d %H:%M:%S')
            dhou = datetime.strptime(str(df3.ix[i,'到款时间']), '%Y-%m-%d %H:%M:%S')
            if (dqian-din) <= pd.Timedelta(0,'D'):
                if (dhou-din) > pd.Timedelta(0,'D'):
                    result = result+df3.ix[i,'实际到款金额']
                    #print(j,col)
                    result_qiye3.ix[j,'日期']=data
                    result_qiye3.ix[j,'企业代码']=df3.ix[i,'企业代码']
                    result_qiye3.ix[j,'实际到款金额']=df3.ix[i,'实际到款金额']
                    j=j+1
                    #print(result_qiye2.ix[j,:])
        datamatrix.ix[m,'单日累计金额']=result
        
    return datamatrix
                    


result2 = caculate_jine(result2,df3)

filename2='12_11/daily_danriheji3.xlsx'
result2.to_excel(filename2, sheet_name='daily_danriheji3') 
filename2='12_11/daily_danriheji3_result_qiye2.xlsx'
result_qiye2.to_excel(filename2, sheet_name='daily_danriheji3_result_qiye2')

result3=pd.DataFrame(list(pd.date_range(start='20180316 00:00:00', end='20181018 00:00:00')),columns=['日期'])
#result_qiye=pd.DataFrame(columns=list(pd.date_range(start='20180316 00:00:00', end='20181018 00:00:00')),index=range(150))
result_qiye3=pd.DataFrame(columns=['日期','企业代码','实际到款金额'],index=range(40000))
result3 = caculate_jine(result3,df4)
 
filename2='12_11/daily_danriheji4.xlsx'
result3.to_excel(filename2, sheet_name='daily_danriheji4') 
filename2='12_11/daily_danriheji4_result_qiye4.xlsx'
result_qiye3.to_excel(filename2, sheet_name='daily_danriheji4_result_qiye4')
#merge
#result_qiye2['日期']=result_qiye2['日期'].apply(datetime)
result_qiye4=result_qiye3
#df['DateTime'] = pd.to_datetime(df['DateTime'])
result_qiye4['日期']=pd.to_datetime(result_qiye4['日期'])

result_qiye4_merge=pd.merge(result_qiye4,result3,on='日期',how='left')

result_qiye4_pivot=pd.pivot_table(result_qiye4_merge,index=['日期','企业代码'],values=['实际到款金额'],aggfunc=np.sum)

filename2='12_11/daily_danriheji4_result_qiye4_pivot.xlsx'
result_qiye4_pivot.to_excel(filename2, sheet_name='daily_danriheji4_result_qiye4_pivot') 

result_qiye4_pivot2=pd.pivot_table(result_qiye4_merge,index=['企业代码','日期'],values=['实际到款金额'],aggfunc=np.sum)

filename2='12_11/daily_danriheji4_result_qiye4_pivot2.xlsx'
result_qiye4_pivot2.to_excel(filename2, sheet_name='daily_danriheji4_result_qiye4_pivot2') 
#######################how to merge?

result_qiye4_pivot2=pd.pivot_table(result_qiye4_merge,index=['企业代码','日期','单日累计金额'],aggfunc={'实际到款金额':'sum'})
filename2='12_11/daily_danriheji4_result_qiye4_pivot3.xlsx'
result_qiye4_pivot2.to_excel(filename2, sheet_name='daily_danriheji4_result_qiye4_pivot3')


#filename='12_11/daily_danriheji4_result_qiye4_pivot3.xlsx'
#book=pd.read_excel(filename,header=0)
#result_qiye4_pivot2=pd.DataFrame(book)
#result_qiye4_pivot2=result_qiye4_pivot2.fillna(method='ffill')
#
#result_qiye4_pivot2['单日企业欠款率']=result_qiye4_pivot2['实际到款金额']/result_qiye4_pivot2['单日累计金额']
#
#result_qiye4_pivot2['最大单日欠款率']=result_qiye4_pivot2['单日企业欠款率']
#result_qiye4_pivot2['平均单日欠款率']=result_qiye4_pivot2['单日企业欠款率']
#result_qiye4_pivot2['累计欠款总额']=result_qiye4_pivot2['实际到款金额']
#result_qiye4_pivot2['平均单日欠款总额']=result_qiye4_pivot2['实际到款金额']
#result_qiye4_pivot2['最大单日欠款总额']=result_qiye4_pivot2['实际到款金额']
#result_qiye4_pivot2['欠款总时间天']=result_qiye4_pivot2['日期']
#result_qiye4_pivot3=pd.pivot_table(result_qiye4_pivot2,index=['企业代码'],aggfunc={'累计欠款总额':'sum','欠款总时间天':'count','平均单日欠款率':'mean','平均单日欠款总额':'mean'
#                                   ,'最大单日欠款总额':'max','最大单日欠款率':'max'})
#filename2='12_11/daily_danriheji4_result_qiye4_statics.xlsx'
#result_qiye4_pivot3.to_excel(filename2, sheet_name='daily_danriheji4_result_qiye4_statics')


'''单日金额排名'''
#filename='12_11/daily_danriheji4_result_qiye4_pivot3.xlsx'
#book=pd.read_excel(filename,header=0)
#df=pd.DataFrame(book)
##fill for 数据透视
#df=df.fillna(method='ffill')
##单日企业欠款率
#df['单日企业欠款率']=df['实际到款金额']/df['单日累计金额']
##数据透视：日期 and get rank
#df['单日排名']=df['单日企业欠款率']
#df2=pd.pivot_table(df,index=['日期','企业代码'],values='单日企业欠款率', aggfunc=np.sum)
##df2=pd.pivot_table(df,index=['日期','企业代码'], aggfunc={'单日企业欠款率':'sum','单日排名':'rank'})

filename='12_11/daily_danriheji4_result_qiye4_pivot3.xlsx'
book=pd.read_excel(filename,header=0)
df=pd.DataFrame(book)
df=df.fillna(method='ffill')
#单日企业欠款率
df['单日企业欠款率']=df['实际到款金额']/df['单日累计金额']
#sort
df2=df.sort_values(by=['日期','实际到款金额'],inplace=False)
df2 = df2.reset_index(drop=True)
df3=df2
#Ranking order per group
#df["rank"] = df.groupby("group_ID")["value"].rank("dense", ascending=False)
df3["rankFrombig"] = df3.groupby("日期")["实际到款金额"].rank("dense", ascending=False)
#output
filename2='12_11/ranker_by_time_and_money_for_qiye2.xlsx'
df3.to_excel(filename2, sheet_name='ranker_jine2')
#df3.columns
#Out[143]: Index(['企业代码', '日期', '单日累计金额', '实际到款金额', '单日企业欠款率', 'rank', 'rankFrombig']
#add all rank
#单日排名如何累计？
#风险排名
df3_pivot_table=pd.pivot_table(df3,index=['企业代码'],values='实际到款金额', aggfunc=np.max)
#

#假定总垫款金额
dftmp=pd.DataFrame(data=10000000,index=range(len(df3_pivot_table)), columns=['假定总垫款金额'])
#df3_pivot_table['假定总垫款金额']=dftmp['假定总垫款金额']
df3_pivot_table['企业代码']=df3_pivot_table.index
df3_pivot_table=df3_pivot_table.reset_index(drop=True)
#concat
df3_pivot_table2=pd.concat([df3_pivot_table,dftmp],axis=1,sort=False)
#风险率排名
df3_pivot_table2['风险率排名']=df3_pivot_table2['实际到款金额']/df3_pivot_table2['假定总垫款金额']
df3_pivot_table2.sort_values(by='风险率排名',inplace=True)

filename2='12_11/ranker_by_money_result.xlsx'
df3_pivot_table2.to_excel(filename2, sheet_name='ranker_money')

'''还款时间排名'''
#filename='final_ready.xlsx'
#book=pd.read_excel(filename,header=0)
#df=pd.DataFrame(book)
#
#'''计算还款时间'''
#df['还款时间']=df['到款时间']-df['填充后汇款日期']
#print(df['还款时间'])
#
#'''删除负的还款时间：国外供应商'''
##delta_t_lt1day = delta_t[delta_t < pd.Timedelta(1,'D')]
#df=df[df['还款时间'] >= pd.Timedelta(1,'D')]
#print(df.shape)
##print(df.info())
#print(df.columns)
##写入xlsx
#filename2='12_11/remove_negatime_all_final.xlsx'
#df.to_excel(filename2, sheet_name='all')
filename2='12_11/remove_negatime_all_final.xlsx'
bookall=pd.read_excel(filename2,header=0)
dateall=pd.DataFrame(bookall)#3828
print(dateall.columns)
#Index(['ID', '业务单编号', '企业代码', '成本确认单编号', '客户单位名称', '收入确认单编号', '供应商名称', '供应商代码',
#       '费目名称', '起始节点', '终止节点', '实际付款金额', '填充后汇款日期', '实际到款金额', '到款时间', '回款时间',
#       '收款总金额', '收款申请单编号', '收入核销日期', '成本核销日期', '企业类型', '企业分类', '客户级别',
#       '最终注册资本', '成立日期', '公司类型', '所属行业', '所属地区', '物流方向', '联运方式代码', '业务单总价',
#       '总成本', '还款时间'],

timedate=dateall[['企业代码','填充后汇款日期','实际付款金额', '到款时间','实际到款金额','收入确认单编号','还款时间']]
#排序
#pd.sort_values("xxx",inplace=True)
timedate.sort_values(by=['收入确认单编号','填充后汇款日期'],inplace=True)
#去重复
timedate2=timedate.drop_duplicates(['收入确认单编号'],keep='first',inplace=False)#785

#每个企业总到款金额
timedate2['总到款金额']=timedate2['实际到款金额']
timedate2_pivot_table=pd.pivot_table(timedate2,index=['企业代码'],values='总到款金额', aggfunc=np.sum)
#merge
timedate3=pd.merge(timedate2_pivot_table,timedate2,how='outer',on='企业代码')
#timedate3.columns
#Out[101]: 
#Index(['企业代码', '总到款金额_x', '填充后汇款日期', '实际付款金额', '到款时间', '实际到款金额', '收入确认单编号',
#       '还款时间', '总到款金额_y']

#计算 norm 还款时间
timedate3['每次金额占比']=timedate3['实际到款金额']/timedate3['总到款金额_y']
timedate3['nomr还款时间']=timedate3['每次金额占比']*timedate3['还款时间']

#-45
timedate3['M']=timedate3['nomr还款时间']-45
timedate3['M7']=timedate3['M']/7

filename2='12_11/ranker_by_time_for_qiye.xlsx'
timedate3.to_excel(filename2, sheet_name='ranker_time')
#星期化
import math
for i in range(len(timedate3)):
    
    timedate3.ix[i,'week']=math.ceil(timedate3.ix[i,'M7'])#向上取整
#>45
timedate4=timedate3[timedate3['M']>0]#105

filename2='12_11/ranker_by_time_for_qiye2.xlsx'
timedate4.to_excel(filename2, sheet_name='ranker_time2')

#sum and count
timedate4['rank_time']=timedate4['week']
timedate4['counts']=timedate4['week']
timedate4_pivot_table=pd.pivot_table(timedate4,index=['企业代码'], aggfunc={'rank_time':'sum','counts':'count'})
timedate4_pivot_table['平均逾期时间排名']=timedate4_pivot_table['rank_time']/timedate4_pivot_table['counts']
#sort 总逾期时间（周）
timedate4_pivot_table.sort_values(by='rank_time',inplace=True)

filename2='12_11/ranker_by_time_result.xlsx'
timedate4_pivot_table.to_excel(filename2, sheet_name='ranker_time3')

'''业务渗透率'''
#filename2='12_11/remove_negatime_all_final.xlsx'
#bookall=pd.read_excel(filename2,header=0)
yewudan=pd.DataFrame(bookall)#
print(yewudan.columns)
yewudan=yewudan[['企业代码','业务单编号','供应商代码', '总成本','业务单总价','填充后汇款日期']]
#排序
#pd.sort_values("xxx",inplace=True)
yewudan.sort_values(by=['业务单编号','填充后汇款日期'],inplace=True)
#去重复
yewudan2=yewudan.drop_duplicates(['业务单编号'],keep='first',inplace=False)#2393
#从日期中取出月份
yewudan2['月份']=yewudan2['填充后汇款日期']
filename2='12_11/ranker_by_yewudan_for_qiye.xlsx'
yewudan2.to_excel(filename2, sheet_name='ranker_shentoulv')
#change date to month by excel

filename2='12_11/ranker_by_yewudan_for_qiye.xlsx'
yewudan2=pd.read_excel(filename2,header=0)
#yewudan2_pivot_table=pd.pivot_table(yewudan2,index=['企业代码','填充后汇款日期'], aggfunc={'业务单总价':'sum','业务单编号':'count'})



yewudan2_pivot_table2=pd.pivot_table(yewudan2,index=['月份','企业代码'], aggfunc={'业务单总价':'sum','业务单编号':'count'})
filename2='12_11/ranker_by_yewudan_month_for_qiye.xlsx'
yewudan2_pivot_table2.to_excel(filename2, sheet_name='ranker_shentoulv_m')

#月频率和总价排名
filename2='12_11/ranker_by_yewudan_month_for_qiye.xlsx'
yewudan3=pd.read_excel(filename2,header=0)
yewudan3=yewudan3.fillna(method='ffill')
#所有企业业务单总额和次数
yewudan3_pivot_table2=pd.pivot_table(yewudan2,index=['月份'], aggfunc={'业务单总价':'sum','业务单编号':'count'})
yewudan3_pivot_table2['月份']=yewudan3_pivot_table2.index
#merge
yewudan4=pd.merge(yewudan3,yewudan3_pivot_table2,how='outer',on='月份')
filename2='12_11/ranker_by_yewudan_month_and_all.xlsx'
yewudan4.to_excel(filename2, sheet_name='ranker_shentoulv_m')
filename2='12_11/ranker_by_yewudan_month_and_all.xlsx'
book2=pd.read_excel(filename2,header=0)
print(book2.columns)
print(book2.columns)
#Index(['月份', '企业代码', '业务单总价_x', '业务单编号_x', '业务单总金额排名', '业务单频次排名', '业务单月总金额',
#       '业务单编月总频次'],
#      dtype='object')
book2['金额占比']=book2['业务单总价_x']/book2['业务单月总金额']
book2['频次占比']=book2['业务单编号_x']/book2['业务单编月总频次']
filename2='12_11/ranker_by_yewudan_month_and_all_rate.xlsx'
book2.to_excel(filename2, sheet_name='ranker_shentoulv_m')

book2_pb=pd.pivot_table(book2,index=['企业代码'], aggfunc={'频次占比':'sum','金额占比':'sum'})
filename2='12_11/ranker_by_yewudan_qiye_result.xlsx'
book2_pb.to_excel(filename2, sheet_name='ranker_shentoulv_m')
#Ranking order per group
#yewudan3["业务单总金额排名"] = yewudan3.groupby("月份")["业务单总价"].rank("dense", ascending=False)
#yewudan3["业务单频次排名"] = yewudan3.groupby("月份")["业务单编号"].rank("dense", ascending=False)
#
#filename2='12_11/ranker_by_yewudan_month_result.xlsx'
#yewudan3.to_excel(filename2, sheet_name='ranker_shentoulv_m')
'''merge all'''
book2_pb['企业代码']=book2_pb.index
timedate4_pivot_table['企业代码']=timedate4_pivot_table.index
allmerge=pd.merge(df3_pivot_table2,book2_pb,on='企业代码',how='outer')
allmerge2=pd.merge(allmerge,timedate4_pivot_table,on='企业代码',how='outer')
allmerge2=allmerge2.fillna(0)
#ranker
allmerge2["均逾期时间排名"] = allmerge2.rank()
filename2='12_11/all_Data_result.xlsx'
allmerge2.to_excel(filename2, sheet_name='ranker_qiye_all')

