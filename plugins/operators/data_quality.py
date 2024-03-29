from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id='redshift',table=[],*args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        self.log.info('Start Data Quality Check ....')
        self.hook =  PostgresHook(postgres_conn_id=self.redshift_conn_id)
        for table in self.table: 
            records = self.hook.get_records(f'SELECT COUNT(*) FROM {table}')
            if len(records)<1 or len(records[0])<1 : 
                raise ValueError(f'Data quality check failed. {table} returned no result')
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError (f'Data quality check failed. {table} contained 0 rows')
            self.log.info(f'Data quality check on table {table} check passed with {records[0][0]} records')
        self.log.info('Data Quality Check Done .....')
            
        