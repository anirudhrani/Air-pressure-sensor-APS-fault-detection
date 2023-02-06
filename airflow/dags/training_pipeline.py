from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

# Retries -> If the pipeline fails for the first time then it can retry trainng speified no. of times.
# schedule_interval -> A fixed interval after which the process will get executed again. Ex: @weekly-> Weekly basis.
with DAG(
        "sensor_training",
        default_args= {'retries'}: 2,
        description= "Air pressure sensor fault detection",
        schedule_interval= "@weekly",
        start_date= pendulum.datetime(2023, 2, 2, tz= "UTC"),
        catchup= False,
        tags= ['example']
        ) as dag:

        def training(**kwargs):
            """Starts training pipeline."""
            # To start the training pipeline in the container.
            from sensor.pipeline.training_pipeline import start_training_pipeline
            start_training_pipeline()

        def sync_artifact_to_s3_bucket(**kwargs):
            bucket_name= os.getenv("BUCKET_NAME")
            os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
            os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")

        # Airflow provides python operrator to call the function.
        training_pipeline=  PythonOperator(task_id= "training_pipeline",
                                           python_callable= training)

        sync_data_to_s3= PythonOperator(task_id= "sync_data_to_s3",
                                        python_callable= sync_artifact_to_s3_bucket)

