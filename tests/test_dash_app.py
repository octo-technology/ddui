from unittest.mock import mock_open, patch

from mock import Mock

from ddui.dash_app import _get_db_from_datadriver_dag, show_columns


def test_get_db_from_datadriver_dag_should_return_db_object_when_DAGfile_contains_an_object_named_db():
    # Given
    dag_filepath = "/my/datadriver_dag.py"
    dag_python_src = "from mock import Mock \n" \
                     "db = Mock()"

    # When
    with patch("builtins.open", mock_open(read_data=dag_python_src)) as f_mock:
        result = _get_db_from_datadriver_dag(dag_filepath)

        # Then
        f_mock.assert_called_once_with(dag_filepath)


def test_get_db_from_datadriver_dag_should_return_db_object_when_DAGfile_contains_an_object_with_retrieve_table_method():
    # Given
    dag_filepath = "/my/datadriver_dag.py"
    dag_python_src = "from mock import Mock \n" \
                     "object_with_retrieve_table = Mock()"

    # When
    with patch("builtins.open", mock_open(read_data=dag_python_src)) as f_mock:
        result = _get_db_from_datadriver_dag(dag_filepath)

        # Then
        assert hasattr(result, "retrieve_table")

def test_show_columns_should_return_Error_when_db_retrieve_table_raise_an_exception():
    # Given
    selectedId = 1
    selectedNodeProps = {'output_table': 'no_such_file_or_directory'}
    db_mock = Mock()
    def retrieve_table_with_error(table):
        raise FileNotFoundError(f"No such file or directory {table}")
    db_mock.retrieve_table.side_effect = retrieve_table_with_error

    # When
    with patch("airflow.models.DagBag", Mock()):
        with patch("ddui.dash_app._get_db_from_datadriver_dag", return_value=db_mock):
            result = show_columns(selectedId, selectedNodeProps)

    # Then
    assert result
    assert b'Error' in result.data