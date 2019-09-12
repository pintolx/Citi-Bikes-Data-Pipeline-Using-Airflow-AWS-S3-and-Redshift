from datetime import datetime, timedelta
import os
import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import StageCsvToRedshiftOperator, PostgresOperator, StageJsonToRedshiftOperator, LoadDimensionOperator, LoadFactOperator, DataQualityOperator
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from helpers import SqlQueries
import boto3
import s3fs
import pandas as pd
#/opt/airflow/start.sh

aws_principal = ''
aws_credential = ''
def start():
    logging.info("Start of DAG")
    
def end():
    logging.info("End of DAG")

def lit_keys():
    hook = S3Hook(aws_conn_id='aws_credentials')
    bucket = Variable.get('s3_bucket')
    keys = hook.list_keys(bucket)
    for key in keys:
        logging.info(f"- Listing Keys from  s3://{key}")
        
default_args = {
    'owner': 'byronkats',
    'start_date': datetime.now(), #datetime(2019, 1, 12),
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'depends_on_past': False,
    'schedule_interval': '0 * * * *'
}
def clean_json():
    #client = boto3.client('s3') #low-level functional API
    client = boto3.client(
    service_name = 's3',
    region_name = 'us-west-2',
    aws_access_key_id = aws_principal,
    aws_secret_access_key = aws_credential)
    resource = boto3.resource('s3')
    my_bucket = resource.Bucket('udacitys3byron') #subsitute this for your s3 bucket name. 
    obj = client.get_object(Bucket='udacitys3byron', Key='cities-data/us-zip-code-latitude-and-longitude.json')
    grid_sizes = pd.read_json(obj['Body'])
    city = []
    zip_code = []
    dst = []
    geopoint = []
    longitude = []
    state = []
    latitude = []
    timezone = []
    p = grid_sizes['fields']
    for i in p:
        city.append(((i)['city']))
        zip_code.append(((i)['zip']))
        dst.append(((i)['dst']))
        geopoint.append(((i)['geopoint']))
        longitude.append(((i)['longitude']))
        state.append(((i)['state']))
        latitude.append(((i)['latitude']))
        timezone.append(((i)['timezone']))
    df = pd.DataFrame(city)
    df['city'] = city
    df['zip_code'] = zip_code
    df['dst'] = dst
    df['geopoint'] = geopoint
    df['longitude'] = longitude
    df['state'] = state
    df['latitude'] = latitude
    df['timezone'] = timezone
    df.drop(0, axis=1)
    df['city_id'] = df.index
    #writing file back to bucket
    print('Start saving the file back to the s3 Bucket')
    bytes_to_write = df.to_csv(None).encode()
    fs = s3fs.S3FileSystem(key=aws_principal, secret=aws_credential)
    with fs.open('s3://udacitys3byron/clean-cities/cleaned-latitude-and-longitude.csv', 'wb') as f:
        f.write(bytes_to_write)
    print('clean file has been saved back to the S3 bucket')


dag = DAG('etl_task_actions',
          default_args=default_args,
          description='Load and transform New York Citi bikes data in Redshift with Airflow'
        )

start_operator = PythonOperator(
    task_id='Begin_execution',
    python_callable= start, 
    dag=dag)

clean_json_operator = PythonOperator(
    task_id='clean_json_file_and_save_to_s3',
    aws_credentials_id="aws_credentials",
    python_callable= clean_json, 
    dag=dag)


#/opt/airflow/start.sh
#start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)
stage_bikes_to_redshift = StageCsvToRedshiftOperator(
    task_id='Stage_bikes',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_city_bikes_data",
    s3_bucket='udacitys3byron',
    s3_key="bikes-data/",
    extra_copy_parameters="REGION 'us-west-2'",
    dag=dag
)

stage_cities_to_redshift = StageCsvToRedshiftOperator(
    task_id='Stage_cities',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_cities",
    s3_bucket='udacitys3byron',
    s3_key="clean-cities",
    extra_copy_parameters="REGION 'us-west-2'",
    dag=dag
)

load_cities_table = LoadFactOperator(
    task_id='Load_cities_fact_table',
    redshift_conn_id="redshift",
    table="cities",
    sql_source=SqlQueries.cities_table_insert,
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    redshift_conn_id="redshift",
    table="users",
    sql_source=SqlQueries.user_table_insert,
    dag=dag
)

load_stations_dimension_table = LoadDimensionOperator(
    task_id='Load_stations_dim_table',
    redshift_conn_id="redshift",
    table="stations",
    sql_source=SqlQueries.stations_table_insert,
    dag=dag
)

load_trips_dimension_table = LoadDimensionOperator(
    task_id='Load_trips_dim_table',
    redshift_conn_id="redshift",
    table="trips",
    sql_source=SqlQueries.trips_table_insert,
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    redshift_conn_id="redshift",
    table="time",
    sql_source=SqlQueries.time_table_insert,
    dag=dag
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    redshift_conn_id="redshift",
    provide_context=True,
    dag=dag,
    table= ['cities', 'stations', 'trips', 'users', 'time']
)

end_operator = PythonOperator(
    task_id='Stop_execution', 
    python_callable= end,
    dag=dag)


start_operator >> clean_json_operator
clean_json_operator >> stage_cities_to_redshift 
stage_cities_to_redshift >> stage_bikes_to_redshift


stage_bikes_to_redshift >> load_cities_table
stage_cities_to_redshift >> load_cities_table

stage_bikes_to_redshift >> load_stations_dimension_table
stage_bikes_to_redshift >> load_trips_dimension_table
stage_bikes_to_redshift >> load_user_dimension_table
stage_bikes_to_redshift >> load_time_dimension_table

load_cities_table >> run_quality_checks
load_user_dimension_table >> run_quality_checks
load_stations_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks
load_trips_dimension_table >> run_quality_checks

run_quality_checks >> end_operator
