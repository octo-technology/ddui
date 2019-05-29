import os
import shutil

from click.testing import CliRunner

from link_ddui_to_airflow import install, clean
from tests.conftest import airflow_home

airflow_plugins = os.environ['AIRFLOW__CORE__PLUGINS_FOLDER']


def setup_function(function):
    shutil.rmtree(airflow_plugins, ignore_errors=True)


def teardown_function(function):
    shutil.rmtree(airflow_plugins, ignore_errors=True)
    shutil.rmtree(f'{airflow_home}/logs', ignore_errors=True)


def test_install_should_add_ddui_symlink_into_airflow_plugins_folder():
    # Given
    runner = CliRunner()

    # When
    with runner.isolated_filesystem():
        result = runner.invoke(install)

        # Then
        assert "Add" in result.stdout
        assert f"to Airflow's plugins folder in {airflow_plugins}/ddui" in result.stdout
        assert os.path.exists(f'{airflow_plugins}/ddui')


def test_install_should_create_folder_when_airflow_plugins_folder_does_not_exist():
    # Given
    runner = CliRunner()

    # When
    with runner.isolated_filesystem():
        result = runner.invoke(install)

        # Then
        assert f"Create Airflow plugins folder {airflow_plugins}" in result.stdout
        assert os.path.exists(f'{airflow_plugins}')


def test_install_should_fallback_when_ddui_already_exists():
    # Given
    runner = CliRunner()

    # When
    with runner.isolated_filesystem():
        os.mkdir(f'{airflow_plugins}')
        os.symlink('.', f'{airflow_plugins}/ddui')
        result = runner.invoke(install)

        # Then
        assert "Run `python setup.py clean` if you want to cleanup and restart the process" in result.stdout


def test_clean_should_remove_ddui_symlink_from_airflow_plugins_folder():
    # Given
    runner = CliRunner()

    # When
    with runner.isolated_filesystem():
        os.mkdir(f'{airflow_plugins}')
        os.symlink('.', f'{airflow_plugins}/ddui')
        result = runner.invoke(clean)

        # Then
        assert f"Remove plugins folder {airflow_plugins}/ddui from Airflow's plugins" in result.stdout
        assert not os.path.exists(f'{airflow_plugins}/ddui')


def test_clean_should_exit_with_error_when_no_link_to_remove():
    # Given
    runner = CliRunner()

    # When
    with runner.isolated_filesystem():
        result = runner.invoke(clean)

        # Then
        assert f"No link to remove : {airflow_plugins}/ddui does not exist" in result.stdout
