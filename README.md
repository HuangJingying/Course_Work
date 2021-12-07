# homework1 
## homwork1 experiment #1
code : homework1_ex1.md
spark data output : /user/huangjingying/homework1/ex1
explanation for code : 
1)	average traffic consumption of each user and each location:
map and reduceByKey (key is user/location, do (x+y)/2 for traffic consumption)
2)	user distribution in terms of locations :
	map and countByKey(key is location, count number of users)
3)	traffic consumption distribution in terms of location :
	map and reduceByKey (key is location, add traffic consumption)
4)	traffic consumption distribution in terms of users : 
map and reduceByKey (key is user , add traffic consumption)

## homwork1 experiment #2
spark code : hw1_ex2_sum_traffic_volumns_per_hour_of_one_bs-*.md
python code : hw1_ex2_plot_traffic_volums_eachhour.py
spark data output : /user/huangjingying/homework1/ex2 AND homwork1/ex2
python output : homework/ex2
1)	select the top 3 BSs(base station) with the largest traffic: 
	sortBy for the result of traffic consumption distribution in terms of location and get top 3 locations with the largest traffic : (u'00309', 625502403937), (u'01077', 628462271341), (u'00332', 645735112712)
this code is in homework1_ex1 annotated by “for homework2 0 select the top 3 BSs(base station) with the largest traffic”
2)	get the traffic volume of the BSs in time_bins(1hour) : 
	filter by location , map and reduceByKey (key is start time/3600)
3)	trend component , periodical component ,residual componnent :
do by seasonal_decompose
4)	plot : title is location ID



# homework3
•Data processing code

train.py ; trace_handler.py ; embed.py

•Collaborative filtering code

recommender_sysytem_CF.py

•Other analysis code

DimReduce.py ; classify.py ; visualizing.py

