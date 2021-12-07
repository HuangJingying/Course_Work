

```python
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
```




    [u'000001\t0000056\t0000094\t00059\t1008']




```python
#--filter by location in RDD
location_01077=lines.filter(lambda x:'01077' in x.split('\t')[3])
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


```python
result_location01077.saveAsTextFile("./homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location01077")
```


```python

```


```python

```
