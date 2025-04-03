from airflow import DAG
from airflow.operators.python import PythonOperator
import yaml
import subprocess
from datetime import datetime, timedelta

# Load config
config_path = "C:\Users\aastha\Desktop\Crypto_Dashboard\Crypto_Dashboard\SRC_BAKND\airflow\config\airflow_config.yaml"

def load_config():
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

# Execute shell commands from config
def run_command(command):
    subprocess.run(command, shell=True, check=True)

def execute_backend():
    config = load_config()

    # Start Zookeeper and Kafka
    run_command(config["commands"]["start_zookeeper"])
    run_command(config["commands"]["start_kafka"])

    # Run backend scripts
    run_command(config["commands"]["run_script_1"])
    run_command(config["commands"]["run_script_2"])
    run_command(config["commands"]["run_script_3"])

# Airflow DAG configuration
default_args = {
"owner": "airflow",
"depends_on_past": False,
"start_date": datetime(2024, 4, 1),
"retries": 1,
"retry_delay": timedelta(minutes=5),
}

dag = DAG(
"crypto_data_pipeline",
default_args=default_args,
description="Triggers Kafka, Zookeeper, and backend scripts",
schedule_interval="*/2 * * * *", # Every 2 minutes
catchup=False,
)

# Define Airflow task
run_pipeline_task = PythonOperator(
task_id="run_crypto_pipeline",
python_callable=execute_backend,
dag=dag,
)

run_pipeline_task