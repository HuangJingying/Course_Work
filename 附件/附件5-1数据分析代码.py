# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 23:19:27 2018

@author: pants
"""
###1.制作数据透视


import os
# 
import numpy as np
import pandas as pd

from datetime import datetime
from datetime import timedelta
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


filename='12_11/daily_danriheji4_result_qiye4_pivot3.xlsx'
book=pd.read_excel(filename,header=0)
result_qiye4_pivot2=pd.DataFrame(book)
result_qiye4_pivot2=result_qiye4_pivot2.fillna(method='ffill')

result_qiye4_pivot2['单日企业欠款率']=result_qiye4_pivot2['实际到款金额']/result_qiye4_pivot2['单日累计金额']

result_qiye4_pivot2['最大单日欠款率']=result_qiye4_pivot2['单日企业欠款率']
result_qiye4_pivot2['平均单日欠款率']=result_qiye4_pivot2['单日企业欠款率']
result_qiye4_pivot2['累计欠款总额']=result_qiye4_pivot2['实际到款金额']
result_qiye4_pivot2['平均单日欠款总额']=result_qiye4_pivot2['实际到款金额']
result_qiye4_pivot2['最大单日欠款总额']=result_qiye4_pivot2['实际到款金额']
result_qiye4_pivot2['欠款总时间天']=result_qiye4_pivot2['日期']
result_qiye4_pivot3=pd.pivot_table(result_qiye4_pivot2,index=['企业代码'],aggfunc={'累计欠款总额':'sum','欠款总时间天':'count','平均单日欠款率':'mean','平均单日欠款总额':'mean'
                                   ,'最大单日欠款总额':'max','最大单日欠款率':'max'})
filename2='12_11/daily_danriheji4_result_qiye4_statics.xlsx'
result_qiye4_pivot3.to_excel(filename2, sheet_name='daily_danriheji4_result_qiye4_statics')




'''单日合计业务单'''
df1=df[['企业代码','业务单编号','业务单总价']]
#去重复
df1.drop_duplicates(['企业代码','成本确认单编号','填充后汇款日期','实际付款金额'],keep='first',inplace=True)
#[654 rows x 4 columns]
df_pivot1=pd.pivot_table(df1,index=["填充后汇款日期"],values=['实际付款金额'],aggfunc=np.sum)
print(df_pivot1.head(3))
filename2='12_11/daily_diankuanjine.xlsx'
df_pivot1.to_excel(filename2, sheet_name='daily_diankuanjine') 

'''每个企业总业务单数量'''
df_pivot=pd.pivot_table(df,index=["企业代码"],values=['业务单编号'],aggfunc=lambda x: len(x.unique()))
#ptaaa=aaa.pivot_table(aaa,index='A',values='B',aggfunc=lambda x: len(x.unique()))
print(df_pivot.head(3))
filename2=pd.ExcelWriter('qiye_yewudan2.xlsx')
df_pivot.to_excel(filename2, sheet_name='yequdan_counts_dup')

'''每个企业总交易金额'''
#取数据
df2=df[['企业代码','业务单编号','业务单总价']]
#去重复
df2.drop_duplicates(['企业代码','业务单编号','业务单总价'],keep='first',inplace=True)
df_pivot2=pd.pivot_table(df2,index=["企业代码"],values=['业务单总价'],aggfunc=np.sum)
print(df_pivot2.head(3))
#>>> writer = pd.ExcelWriter('output.xlsx')
#>>> df1.to_excel(writer,'Sheet1')
#>>> df2.to_excel(writer,'Sheet2')
#>>> writer.save()
filename2='yequdan_zongjia_sum_npsum.xlsx'
df_pivot2.to_excel(filename2, sheet_name='yequdan_zongjia_sum_npsum')
#filename2.save()

'''每个企业总垫款金额'''
#取数据
df4=df[['企业代码','成本确认单编号','填充后汇款日期','实际付款金额']]
#去重复
df4.drop_duplicates(['企业代码','成本确认单编号','填充后汇款日期','实际付款金额'],keep='first',inplace=True)
df_pivot4=pd.pivot_table(df4,index=["企业代码"],values=['实际付款金额'],aggfunc=np.sum)
print(df_pivot4.head(3))
#>>> writer = pd.ExcelWriter('output.xlsx')
#>>> df1.to_excel(writer,'Sheet1')
#>>> df2.to_excel(writer,'Sheet2')
#>>> writer.save()
filename2='yequdan_diankuan_sum_npsum.xlsx'
df_pivot4.to_excel(filename2, sheet_name='yequdan_diankuan_sum_npsum')

'''每个企业垫款金额占比'''
df5=pd.merge(df_pivot2,df_pivot4,how='outer',on='企业代码')
#[147 rows x 2 columns]
df5['垫款率']=df5['实际付款金额']/df5['业务单总价']
filename2='qiye_zongjia_diankuan_percent.xlsx'
df5.to_excel(filename2, sheet_name='qiye_zongjia_diankuan_percent')

'''时间'''
dftime=df[['企业代码','业务单编号','成本确认单编号','收入确认单编号','实际付款金额', '填充后汇款日期', '实际到款金额', '到款时间']]
dftime.drop_duplicates(['企业代码','业务单编号','成本确认单编号','实际付款金额', '填充后汇款日期', '实际到款金额', '到款时间','收入确认单编号'],keep='first',inplace=True)
dftime['回款时间']=dftime['到款时间']-dftime['填充后汇款日期']
#df['回款时间']=df['到款时间']-df['填充后汇款日期']
#print(df['回款时间'])
#删除负值
#delta_t_lt1day = delta_t[delta_t < pd.Timedelta(1,'D')]
dftime0=dftime[dftime['回款时间'] >= pd.Timedelta(1,'D')]

filename2='time_huankuanshijian2.xlsx'
dftime.to_excel(filename2, sheet_name='time_huankuanshijian2')

'''每个企业总垫款时间'''
dftime2=dftime[['企业代码','业务单编号','回款时间']]
#pd.sort_values("xxx",inplace=True)
dftime2.sort_values(by=['企业代码','业务单编号','回款时间'],inplace=True)
#df.sort_values(by='col1', ascending=False, na_position='first')
dftime2.drop_duplicates(['企业代码','业务单编号','回款时间'],keep='last',inplace=True)
#[9283 rows x 3 columns]
dftime2_pivot=pd.pivot_table(dftime2,index=["企业代码"],values=['回款时间'],aggfunc=np.sum)
#dftime2_pivot2=pd.pivot_table(dftime2,index=["企业代码"],values=['回款时间'],aggfunc=np.mean)

filename2='qiye_time_npsum.xlsx'
dftime2_pivot.to_excel(filename2, sheet_name='qiye_time_npsum')


'''每个企业总业务单发生频次（周）：统计每个企业代码业务单编号数量/交易时间*7'''
df3=df[['企业代码','业务单编号','起始节点', '终止节点','成本确认单编号','实际付款金额', '填充后汇款日期']]
#去重复
df3.drop_duplicates(['企业代码','成本确认单编号','填充后汇款日期','实际付款金额'],keep='first',inplace=True)
df_pivot3=pd.pivot_table(df3,index=["企业代码"],values=['实际付款金额'],aggfunc=lambda x: sum(x.unique()))
print(df_pivot3.head(3))
filename2="yequdan_jine_sum_1"
df_pivot3.to_excel(filename2, sheet_name='yequdan_jine_sum_1' )


