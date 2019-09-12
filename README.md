# Citi-Bikes-Data-Pipeline-Using-Airflow-AWS-S3-and-Redshift
** New York Citi Bikes Data Pipeline
Building an end-to-end data pipeline for a bikes company based in New York City
# Section 1: Scope the Project and Gather Data
Citi Bike is a privately owned public bicycle sharing system serving the New York City boroughs of Manhattan, Queens, and Brooklyn, as well as Jersey City, New Jersey. Since it publicly shares its data here: [https://www.citibikenyc.com/system-data], many people have been curious about questions like Where do Citi Bikers ride? When do they ride? How far do they go? Which stations are most popular? What days of the week are most rides taken on? This project aims to answer some of those questions.
The scope of this project is to gather data from this open data source, load them into S3 bucket, and transform them to a well-defined schema that business analysts can use to answer business questions. Citi bikes provides data for every month of operation, I could only cover the period between 2013/07and 2014/02. The data used can be found here: [https://s3.amazonaws.com/tripdata/index.html]. This dataset was in csv format and yet the project required at least two datasets in different formats, so I went to [https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/table/] and got a json dataset about all towns in New York City. I used this to locate the citi bikes stations.
# Section 2: Explore and Assess the Data
There are two types of data in this project. One is csv, and another is json.
# Input Data Files
There are mainly two file types – the bikes dataset that was saved in csv format and locations data that is saved into the json file.
Citi Bike trips data – includes tripduration, starttime, stoptime, start station id, start station name, start station latitude, start station longitude, end station id, end station name, end station latitude, end station longitude, bikeid, usertype, birth year and gender.
Locations data - includes datasetid, fields, geometry, record_timestamp, recorded. This file is stored in an s3 bucket. The clean_josn method in the dag accesses it, preprocesses it, cleans it and saves it as a csv file in another folder. The saved csv has the following fields: city, zip_code, dst, geopoint, longitude, state, latitude and timezone
Please note that I used a different folder in my s3 bucket to store the cleaned csv file from the locations file and a different folder to store the trips data
# Output Code Files
create_table.sql - including code for creating all the tables (staging tables, dimension tables, and fact tables). It needs to be run before running the airflow dags.
- Citi_bikes_dag.py - dag file for all dag config, and task information
- sql_queries.py in plugins.helpers - including codes for ETL and deleting data if necessary
- stage_csv_to_redshift.py in plugins.operators - including codes for staging csv data from s3 bucket to redshift
- load_dimension/load_fact.py in plugins.operators - including codes for connecting to redshift, and executing codes for ETL
- data_quality.py in plugins.operators - including codes for quality checks
# Section 3: Define the Data Model
In this project, I used star schema to design the data model. Please refer to the design below -

# Section 4: Run ETL to Model the Data in Airflow
The dag is setup to run once a month because the data is updated monthly, there is a data quality check to ensure that all the tables ingest data.
DAG config is as follows -
-	The DAG does not have dependencies on past runs
-	On failure, the task are retried 3 times
-	Retries happen every 5 minutes
-	Catchup is turned off
Please refer to the graph view follows the flow shown in the image below – 

Here is the quality check results screenshot – 

# Section 5: Sample analysis queries
Here are some of the questions that can be answered using this new data warehouse -
1.	"How many unique bike stations do we have in New York City and in what zip code are they located?"
```
Sample query -
select count(distinct stationid) 
from stations

select station_name, latitude, longitude
from stations
where station_zipcode = ''
```

2.	"What is the hour of the day with the most trips on a given date?
```
Sample query -
Select start_hour, count(tripid) 
from trips
where date(start_time) = ‘2017-06-06’
group by start_hour
```
3.	"What is the longest trip on any given date?"
```
Sample query -
select max(duration) 
from trips
where date(start_time) = ‘2017-06-06’
```
# Section 6: Limitations
Because Citi Bikes provide the data, we do not have control of the data structure. The data does not have more information about the consumers and thus we cannot be able to do more analysis on user behavior. As such, the users table only has the user type and subscriber type.  
# Section 7: Difficulties of this Project
1.	Many of the difficulties that I faced were due to lack of enough experience. For example, I stored the uncleaned json file and the cleaned file in the same folder in the s3 bucket. The jobs failed because they were trying to read in both the json and the newly cleaned csv file.
2.	It was also challenging to find a second dataset that fit into the project that I was trying to set up.
3.	I also faced connectivity issues, while trying to use boto3 and sfs3 to processes the json file and save it back to the s3 bucket
