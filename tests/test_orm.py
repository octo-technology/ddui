from mock import patch

from ddui.orm import airflow_dags


def test_airflow_dags_should_return_the_dag_id_list_from_the_AIRFLOW_DAGS_FOLDER():
    # Given


    # When
    result = airflow_dags()

    # Then
    assert 'dag_with_dataframe' in result
