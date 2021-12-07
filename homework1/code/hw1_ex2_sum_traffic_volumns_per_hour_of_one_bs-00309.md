

```python
from pyspark.sql import Row
from pyspark.sql.types import *
import pyspark.sql.functions as f
from pyspark.sql.functions import lit
import pandas as pd
import numpy as np
sqlContext = SQLContext(sc)
# lines=sc.textFile("/data/Traffic_1000BS_Final")
# lines.take(1)
#device ID|start time|end time|location(base station ID)|traffic volumns(Bytes)|
```


```python
#--filter by location in RDD
location_01077=lines.filter(lambda x:'00309' in x.split('\t')[3])
# location01077=location_01077.map(lambda x:(x.split('\t')[3],x.split('\t')[0],int(x.split('\t')[1]),int(x.split('\t')[1])/3600,
#                                  int(x.split('\t')[4])))
location01077=location_01077.map(lambda x:(int(x.split('\t')[1])/3600,
   x.split('\t')[3],x.split('\t')[0],int(x.split('\t')[1]),
                                 int(x.split('\t')[4])))
```


```python
location01077.take(10)
```




    [(10, u'00309', u'000001', 39104, 38065),
     (33, u'00309', u'000001', 121151, 2173),
     (49, u'00309', u'000001', 178488, 188305),
     (103, u'00309', u'000001', 371957, 69612),
     (129, u'00309', u'000001', 465654, 0),
     (129, u'00309', u'000001', 467397, 180),
     (134, u'00309', u'000001', 484248, 72611),
     (151, u'00309', u'000001', 544169, 8684),
     (153, u'00309', u'000001', 552418, 14665),
     (185, u'00309', u'000001', 667377, 22468)]




```python
from operator import add 

result_location01077=location01077.map(lambda x: (x[0],x[3])).reduceByKey(add)
result_location01077.take(10)
```




    [(0, 1109219),
     (644, 2317913882),
     (391, 1201809925),
     (138, 534492505),
     (529, 970227919),
     (276, 710673668),
     (23, 93648712),
     (667, 2689001084),
     (414, 889386693),
     (161, 583770571)]




```python
result_location01077.saveAsTextFile("./homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location00309")
```


```python
# result_location01077=sc.textFile("/user/huangjingying/homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location00309")
```


```python
# result_location01077.take(1)
```




    [u'(0, 1109219)']




```python
# result_location01077.repartition(1).saveAsTextFile("/user/huangjingying/homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location00309_onefile")
# #//textFile.repartition(1).saveAsTextFile 就能保存成一个文件
```


```python
# result_location01077.map(lambda x: (x.split(', ')[0].split('(')[1])).take(1)
```




    [u'0']




```python
# result_location01077.map(lambda x: (x.split(', ')[1].split(')')[0])).take(1)
```




    [u'1109219']




```python
#--DRR to dataframe
# schema = StructType([ 
#     #StructField('location_ID', StringType(), False),
#     #StructField('user_ID', StringType(), False),
#  StructField('DateTime', IntegerType(), False),
#  #StructField('EndDateTime', IntegerType(), False),
# StructField('traffic_volumns_sum',IntegerType(),False)])
# location01077_df = sqlContext.createDataFrame(result_location01077.map(lambda x: (x.split(', ')[0].split('(')[1],x.split(', ')[1].split(')')[0]), schema))
```


```python
# location01077_df.show()
```

    +---+----------+
    | _1|        _2|
    +---+----------+
    |  0|   1109219|
    |644|2317913882|
    |391|1201809925|
    |138| 534492505|
    |529| 970227919|
    |276| 710673668|
    | 23|  93648712|
    |667|2689001084|
    |414| 889386693|
    |161| 583770571|
    |552|1191327407|
    |299| 761178322|
    | 46| 151410315|
    |690|2557907750|
    |437| 680438081|
    |184| 560555698|
    |575|2164374366|
    |322| 875411159|
    | 69| 249396178|
    |713|2560922164|
    +---+----------+
    only showing top 20 rows
    



```python
# location01077_df.toPandas().to_csv("/home/huangjingying/homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location00309.csv")
```


```python

```
