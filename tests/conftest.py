
import os
airflow_home = os.path.dirname(os.path.realpath(__file__))
os.environ['AIRFLOW_HOME'] = airflow_home
os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = f'{airflow_home}/dags'
os.environ['AIRFLOW__CORE__PLUGINS_FOLDER'] = f'{airflow_home}/plugins'
os.environ['AIRFLOW__CORE__UNIT_TEST_MODE'] = 'True'

import airflow
airflow.configuration.load_test_config()