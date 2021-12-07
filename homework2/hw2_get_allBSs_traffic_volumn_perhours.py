
# coding: utf-8

# In[3]:


from pyspark.sql import Row
from pyspark.sql.types import *
import pyspark.sql.functions as f
from pyspark.sql.functions import lit
import pandas as pd
import numpy as np
sqlContext = SQLContext(sc)
lines=sc.textFile("/data/Traffic_1000BS_Final")

lines.take(1)
#device ID|start time|end time|location(base station ID)|traffic volumns(Bytes)|


# In[32]:


#1 map(key is location ID and time(h)) and reducebykey(add traffic volumns) get sum of traffic volumns for each BS per hour
# location=lines.map(lambda x:(int(x.split('\t')[1])/3600,
#    x.split('\t')[3],x.split('\t')[0],int(x.split('\t')[1]),
#                                  int(x.split('\t')[4])))
# location.take(1)
#[(0, u'00059', u'000001', 56, 1008)]
#hourtime,location,userid,starttime,traffic volumns
location=lines.map(lambda x:((int(x.split('\t')[1])/3600,
   x.split('\t')[3]), int(x.split('\t')[4])))
location.take(1)
#[((0, u'00059'), 1008)]
# hourtime,location,traffic_volumns


# In[ ]:


from operator import add 
#location.map(lambda x: (x[0])).take(1)
result_location=location.map(lambda x: (x[0],x[1])).reduceByKey(add)
result_location.take(10)

result_location.saveAsTextFile("./homework2/Data/hw2_sum_traffic_volumns_per_hour_of_allBSs")


# In[31]:


#[((82, u'00138'), 35586736), ((564, u'01035'), 14879278), ((599, u'00884'), 301674982), ((372, u'00334'), 1155499957), ((155, u'00010'), 9281051), ((440, u'00329'), 370850086), ((245, u'00492'), 38149947), ((350, u'00526'), 6489855), ((646, u'00071'), 97659590), ((431, u'00321'), 268419914)]
#result_location.saveAsTextFile("./homework2/Data/hw2_sum_traffic_volumns_per_hour_of_allBSs")


# In[ ]:


#2 map(key is location ID and time(week)) and reducebykey(average of traffic volumns)。


# In[ ]:


# remove three days
result_location.count()#529843
result_location2=result_location.filter(lambda x:x[0][0]<=4*7*24)
result_location2.take(10)
result_location2.count()#479713 #(529843-479713)%(3*24)
# [((82, u'00138'), 35586736), ((564, u'01035'), 14879278), ((599, u'00884'), 301674982), ((372, u'00334'), 1155499957), ((155, u'00010'), 9281051), ((440, u'00329'), 370850086), ((245, u'00492'), 38149947), ((350, u'00526'), 6489855), ((646, u'00071'), 97659590), ((431, u'00321'), 268419914)]


# In[ ]:


# week_location=result_location.map(lambda x: ((x[0][0]%168,x[0][1]),x[1]))#.reduceByKey(lambda x,y:x+y)#
# week_location.take(2)
# [((82, u'00138'), 35586736), ((60, u'01035'), 14879278)]
week_location=result_location2.map(lambda x: ((x[0][0]%168,x[0][1]),x[1])).reduceByKey(lambda x,y:(x+y)/2)#
week_location.take(10)
week_location.saveAsTextFile("./homework2/Data/hw2_sum_traffic_volumns_per_hour_of_allBSs_foldtoWeek")
# [((82, u'00138'), 31417421), ((14, u'00246'), 155320), ((112, u'00313'), 325755825), ((109, u'00317'), 137396231), ((166, u'00468'), 2769138), ((119, u'00260'), 5997901), ((53, u'00964'), 46446948), ((155, u'00010'), 9196681), ((97, u'00696'), 358659446), ((155, u'00612'), 57240490)]
# #[((82, u'00138'), 34702112), ((14, u'00246'), 638557), ((112, u'00313'), 325755825), ((109, u'00317'), 164988300), ((166, u'00468'), 4479238), ((119, u'00260'), 5997901), ((53, u'00964'), 65025847), ((155, u'00010'), 9196681), ((97, u'00696'), 222758465), ((155, u'00612'), 43375193)]

