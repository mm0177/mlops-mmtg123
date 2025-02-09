from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import os
from components.data_ingestion import DataIngestion
from components.data_transformation import DataTransformation
from components.model_trainer import ModelTrainer
from utility.util import load_csv, save_artifact
import boto3
import zipfile

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'training_pipeline',
    default_args=default_args,
    description='Training pipeline automation using Airflow with XCom',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    artifacts_dir = './artifacts'
    raw_data_file = r'/opt/airflow/src/train.csv'
    s3_bucket_name="my-mlops-mmtg"
    s3_model_key = 'models/random_forest_model.pkl'



    # Task 1: Data Ingestion
    def data_ingestion_task(**kwargs):
        if not os.path.exists(artifacts_dir):
            os.makedirs(artifacts_dir, exist_ok=True)
        if not os.path.exists(raw_data_file):
            raise FileNotFoundError(f"Raw data file not found at {raw_data_file}. Please provide the input data.")
        DataIngestion(input_file=raw_data_file, output_dir=artifacts_dir)
        return {'train_file': os.path.join(artifacts_dir, 'train.csv'),
                'test_file': os.path.join(artifacts_dir, 'test.csv')}

    ingest_data = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion_task,
        provide_context=True,
    )

    # Task 2: Data Transformation
    def data_transformation_task(**kwargs):
        ti = kwargs['ti']
        paths = ti.xcom_pull(task_ids='data_ingestion')

        train_file_path = paths['train_file']
        test_file_path = paths['test_file']

        train_df = load_csv(train_file_path)
        test_df = load_csv(test_file_path)

        data_transformation = DataTransformation()

        # Separate the target variable
        y_train = train_df['price']
        y_valid = test_df['price']

        train_df = train_df.drop(columns=['price', 'id'], errors='ignore')
        test_df = test_df.drop(columns=['price', 'id'], errors='ignore')

        # Transform data
        train_df_transformed, test_df_transformed = data_transformation.initiate_data_transformation(train_df, test_df)

        # Save transformed columns
        transformed_columns = train_df_transformed.columns
        save_artifact(transformed_columns, os.path.join(artifacts_dir, 'transformed_columns.pkl'))

        # Push results to XCom
        return {
            'train_data': train_df_transformed.to_dict(),
            'test_data': test_df_transformed.to_dict(),
            'y_train': y_train.tolist(),
            'y_valid': y_valid.tolist(),
        }

    transform_data = PythonOperator(
        task_id='data_transformation',
        python_callable=data_transformation_task,
        provide_context=True,
    )

    # Task 3: Model Training
    def model_training_task(**kwargs):
        ti = kwargs['ti']
        transformed_data = ti.xcom_pull(task_ids='data_transformation')

        # Extract data from XCom
        train_df_transformed = pd.DataFrame(transformed_data['train_data'])
        test_df_transformed = pd.DataFrame(transformed_data['test_data'])
        y_train = pd.Series(transformed_data['y_train'])
        y_valid = pd.Series(transformed_data['y_valid'])

        # Train the model
        ModelTrainer(
            train_df_transformed,
            y_train,
            test_df_transformed,
            y_valid,
            os.path.join(artifacts_dir, 'random_forest_model.pkl'),
        )

    train_model = PythonOperator(
        task_id='model_training',
        python_callable=model_training_task,
        provide_context=True,
    )


    def compress_file(file_path,zip_path):
        with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path,os.path.basename(file_path))
        return zip_path


    def upload_fxn(**kwargs):
        model_path=os.path.join(artifacts_dir,"random_forest_model.pkl")
        zip_model_path=os.path.join(artifacts_dir,'random_forest_model.zip')

        compressed_file_path=compress_file(model_path,zip_model_path)
        if not os.path.exists(model_path):
            raise FileExistsError
        

        s3_client=boto3.client(
            's3',
            aws_access_key_id="AKIAZWLMXQ5CZWOBTC6E",
            aws_secret_access_key='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',
            region_name='ap-southeast-2'



        )
        s3_client.upload_file(compressed_file_path,s3_bucket_name,s3_model_key)

    upload_to_s3=PythonOperator(


        task_id='upload_to_s3',
        python_callable=upload_fxn,
        provide_context=True,
    )

    # Define task dependencies
    ingest_data >> transform_data >> train_model>>upload_to_s3
