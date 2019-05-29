import os
import sys


os.environ['AIRFLOW_HOME'] = './'
os.environ['AIRFLOW__CORE__PLUGINS_FOLDER'] = '../../ddui'
os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = '../dags'
os.environ['AIRFLOW__CORE__UNIT_TEST_MODE'] = 'True'
os.environ['AIRFLOW__CORE__LOAD_EXAMPLES'] = 'False'
import airflow
airflow.configuration.load_test_config()

from airflow import configuration
from airflow.bin.cli import CLIFactory
from airflow.utils.db import initdb

initdb()
sys.argv.append("webserver")
sys.argv.append("-w 1")
parser = CLIFactory.get_parser()
args = parser.parse_args()
args.func(args)