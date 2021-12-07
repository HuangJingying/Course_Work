

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
location_01077=lines.filter(lambda x:'00332' in x.split('\t')[3])
# location01077=location_01077.map(lambda x:(x.split('\t')[3],x.split('\t')[0],int(x.split('\t')[1]),int(x.split('\t')[1])/3600,
#                                  int(x.split('\t')[4])))
location01077=location_01077.map(lambda x:(int(x.split('\t')[1])/3600,
   x.split('\t')[3],x.split('\t')[0],int(x.split('\t')[1]),
                                 int(x.split('\t')[4])))
```


```python
location01077.take(10)
```




    [(7, u'00332', u'000001', 26707, 13986),
     (9, u'00332', u'000001', 32846, 12749),
     (16, u'00332', u'000001', 57664, 27827),
     (31, u'00332', u'000001', 113412, 18810),
     (31, u'00332', u'000001', 113631, 8187),
     (31, u'00332', u'000001', 114312, 5408886),
     (32, u'00332', u'000001', 117495, 2674),
     (32, u'00332', u'000001', 117617, 0),
     (33, u'00332', u'000001', 120644, 10281),
     (33, u'00332', u'000001', 120687, 20429)]




```python
from operator import add 

result_location01077=location01077.map(lambda x: (x[0],x[3])).reduceByKey(add)
result_location01077.take(10)
```




    [(0, 477367),
     (644, 939648978),
     (391, 539618369),
     (138, 219882053),
     (529, 316417588),
     (276, 292647833),
     (23, 35382262),
     (667, 884334908),
     (414, 386489399),
     (161, 244809381)]




```python
result_location01077.saveAsTextFile("./homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location00332")
```


```python
# result_location01077=sc.textFile("/user/huangjingying/homework1/ex2/hw1_ex2_sum_traffic_volumns_per_hour_of_location00332")
```


```python
# result_location01077.take(2)
```
