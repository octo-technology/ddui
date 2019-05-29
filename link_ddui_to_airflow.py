import os

import click

from pkg_resources import resource_filename

@click.group()
def cli():
    pass

@cli.command()
def install():
    from airflow.configuration import get
    install_dir = os.path.dirname(resource_filename("ddui", "__init__.py"))

    root_airflow_plugin = get('core', 'plugins_folder')
    if not os.path.exists(root_airflow_plugin):
        os.mkdir(root_airflow_plugin)
        click.echo('Create Airflow plugins folder {} '.format(root_airflow_plugin))
    plugins_folder = os.path.join(root_airflow_plugin, 'ddui')

    if not os.path.exists(plugins_folder):
        os.symlink(install_dir, plugins_folder)
        click.echo('Add {} to Airflow\'s plugins folder in {}'.format(install_dir, plugins_folder))
    else:
        click.echo('''Plugin {} is already installed.
                Run `python setup.py clean` if you want to cleanup and restart the process'''.format(plugins_folder))

@cli.command()
def clean():
    from airflow.configuration import conf
    plugins_folder = os.path.join(conf.get('core', 'plugins_folder'), 'ddui')
    if os.path.exists(plugins_folder):
        os.remove(plugins_folder)
        click.echo('Remove plugins folder {} from Airflow\'s plugins'.format(plugins_folder))
    else:
        click.echo('No link to remove : {} does not exist'.format(plugins_folder))
