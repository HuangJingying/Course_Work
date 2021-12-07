

```python
#pyspark --master=yarn
#from pyspark import SparkContext
#sc = SparkContext("local")
```


```python
lines=sc.textFile("/data/Traffic_1000BS_Final")
```


```python
lines.cache()  #//会调用persist(MEMORY_ONLY)，但是，语句执行到这里，并不会缓存rdd，这是rdd还没有被计算生成
```


```python
lines.take(1) 
#device ID|start time|end time|location(base station ID)|traffic volumns(Bytes)|
```


```python
#1.1 average traffic consumption of each user 
user=lines.map(lambda x:(x.split('\t')[0],int(x.split('\t')[4])))#把每一行映射成 (user，流量 )的键值对：
user.take(10)
```


```python
user_average=user.reduceByKey(lambda x,y: (x+y)/2)
```


```python
user_average.take(100)
```


```python
#help(operator)
```


```python
user_average.saveAsTextFile("./homework1/ex1/user_average_traffic_consumption")
```


```python
#1.2 average traffic consumption of each location
location=lines.map(lambda x:(x.split('\t')[3],int(x.split('\t')[4])))#把每一行映射成 (location，流量 )的键值对：
location.take(100)
```


```python
location_average=location.reduceByKey(lambda x,y: (x+y)/2)
location_average.take(100)
location_average.saveAsTextFile("./homework1/ex1/location_average_traffic_consumption")
```


```python
# 2 user distribution in terms of locations
from operator import add
user_distribution=lines.map(lambda x:(x.split('\t')[3],x.split('\t')[0]))#把每一行映射成 (location，user )的键值对：
user_distribution.take(100)
user_distribution_result=user_distribution.countByKey()# 返回一个字典（key,count），该函数操作数据集为kv形式的数据，用于统计RDD中拥有相同key的元素个数。
#hadoop fs -rm -r ./homework1/ex1/user_distribution_of_location_result

# no # user_distribution_result2=sc.parallelize(user_distribution_result).map(lambda x:(x.split(':')[0],x.split(':')[1]))
# no #user_distribution_result2.take(10)
# no # user_distribution_result.write.csv('./homework1/ex1/user_distribution_of_location_result.csv') #保存数据

sc.parallelize(user_distribution_result).saveAsTextFile("./homework1/ex1/user_distribution_of_location_result")
```


```python
# 3 traffic consumption distribution in terms of location
traffic_consumption_distribution=lines.map(lambda x:(x.split('\t')[3],int(x.split('\t')[4])))
traffic_consumption_distribution.take(100)
traffic_consumption_distribution_result=traffic_consumption_distribution.reduceByKey(add)
traffic_consumption_distribution_result.take(100)
traffic_consumption_distribution_result.saveAsTextFile("./homework1/ex1/traffic_consumption_distribution_of_location_result")
```


```python
# for homework2 0 select the top 3 BSs(base station) with the largest traffic
#print (traffic_consumption_distribution_result.sortByKey(False).collect())#从大到小排序
traffic_consumption_distribution_result.sortBy(lambda a: a[1]).collect() #从小到大排序
traffic_consumption_distribution_result.takeOrdered(10, key=lambda x: -x[1]) 

#...(u'00309', 625502403937), (u'01077', 628462271341), (u'00332', 645735112712)]


#traffic_consumption_distribution_result.sortBy(_._2).take(10)
```


```python
# 4 traffic consumption distribution in terms of users
traffic_consumption_distribution2=lines.map(lambda x:(x.split('\t')[0],int(x.split('\t')[4])))
traffic_consumption_distribution2.take(100)
traffic_consumption_distribution2_result=traffic_consumption_distribution2.reduceByKey(add)
traffic_consumption_distribution2_result.take(100)
traffic_consumption_distribution2_result.saveAsTextFile("./homework1/ex1/traffic_consumption_distribution_of_user_result")
```
