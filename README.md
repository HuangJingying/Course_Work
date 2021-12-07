According to the user requirements, the project team designed the project architecture as shown in Figure X, including seven modules of data acquisition and integration, descriptive data analysis, data cleaning, data pre-processing, neural network model, model evaluation, and establishment of credit scoring system.

# Data source acquisition and integration 
The historical data of China Railway Multi-Link integrated business system is exported and filtered, and data crawlers are used to complement the current data of the enterprise, and finally useless data are deleted and the required data are integrated
# Descriptive data analysis 
The purpose of this step is to conduct an initial exploration of the distribution of each variable, to obtain the general situation of the sample, and to assess whether the data have diversity and completeness. Exploratory data analysis methods include: histogram, scatter plot and box plot.
# Data cleaning 
Including data missing value processing, outlier processing, filtering out the most significant impact on the results by statistical methods, and transforming the acquired raw data into exploitable formatted data.
# Integrated decision tree classification model 
The extraction of labels and quantification of features are performed first, and then an integrated learning-based decision tree classification model is established to accurately predict the next repayment time and repayment willingness of some enterprises as loan indicators
# Model evaluation 
Analyze the reasonableness and business relevance of the model, evaluate the differentiation ability, prediction ability, and stability of the model, and conclude whether the model can be used.
# Comprehensive credit scoring system 
Calculate indicators such as business penetration rate, average order amount, and number of days overdue for each customer, and convert the model into a form of standard score according to the 5-3-2 indicator system of the financial industry to establish an automatic credit scoring system.
# Establish a whitelist 
Based on the comprehensive scoring system, take the customers who are in the top of all indicators as whitelist customers, and agree with the companies on the score line of specific indicators
# Post-lending management and feedback 
Introduce a post-lending management evaluation system. For loan customers, calculate their credit limits and capital risks every day, show reminders for customers with high risks, recommend phone calls, talks, other emergency measures, etc.

