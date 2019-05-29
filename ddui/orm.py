

def airflow_dags():
    """
    Read the list of dags from Airflow's metastore DB and return the list as a pandas.DataFrame
    :return: pandas.DataFrame
    """
    from airflow import models, settings

    dagbag = models.DagBag(settings.DAGS_FOLDER)

    return list(dagbag.dags)