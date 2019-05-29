# Stub of the DAG object from Airflow custom operators
# It simulates the behavior of DataDriver's framework DDAPI
# The principal component used en rendered by the User Interface is the "output_table" attribute of each Operator

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import numpy as np
import pandas as pd

class MockOutputOperator(PythonOperator):

    def __init__(self, python_callable, output_table=None, op_args=None, op_kwargs=None, *args, **kwargs):
        super(MockOutputOperator, self).__init__(python_callable=python_callable, op_args=op_args,
                                                 op_kwargs=op_kwargs, *args, **kwargs)
        self.output_table = output_table


class MockDB:
    logistic = np.random.logistic(10, 1, 500)
    std_normal = 2.5 * np.random.randn(500)
    random = np.random.rand(500)
    poisson = np.random.poisson(100, 500)
    gamma = np.random.gamma(2, 1, 500)

    _init_set = pd.DataFrame({'logistic': logistic, 'normal': std_normal, 'random': random, 'poisson': poisson, 'gamma': gamma})

    @staticmethod
    def retrieve_table(table_name):
        return MockDB._init_set


db = MockDB
transfo_python = lambda df: df + 1
join_python = lambda df1, df2: pd.concat([df1, df2], axis=1)

with DAG(dag_id='dag_with_dataframe', start_date=airflow.utils.dates.days_ago(2), schedule_interval='@once') as dag:
    source1 = MockOutputOperator(python_callable=transfo_python, output_table='t1', task_id='Source1.click.to.see.output', op_kwargs=dict(df=None))
    source2 = MockOutputOperator(python_callable=transfo_python, output_table='t1', task_id='Source2.click.to.see.output', op_kwargs=dict(df=None))
    task1 = MockOutputOperator(python_callable=transfo_python, output_table='t2', task_id='Task1.click.to.see.output', op_kwargs=dict(df=None))
    join1 = MockOutputOperator(python_callable=transfo_python, output_table='t3', task_id='Join1.click.to.see.output', op_kwargs=dict(df=None))
    task2 = MockOutputOperator(python_callable=transfo_python, output_table='t4', task_id='Task2.click.to.see.output', op_kwargs=dict(df=None))
    join3 = MockOutputOperator(python_callable=transfo_python, output_table='t5', task_id='Join3.click.to.see.output', op_kwargs=dict(df=None))
    join2 = MockOutputOperator(python_callable=transfo_python, output_table='t6', task_id='Join2.click.to.see.output', op_kwargs=dict(df=None))
    task4 = MockOutputOperator(python_callable=transfo_python, output_table='t7', task_id='Task4.click.to.see.output', op_kwargs=dict(df=None))
    task5 = MockOutputOperator(python_callable=transfo_python, output_table='t8', task_id='Task5.click.to.see.output', op_kwargs=dict(df=None))

    source1 >> [task1, join1, join2]
    source2 >> [join2]
    task1 >> [join1, task2]
    [task2, join1, task1] >> join3
    join2 >> task4 >> task5