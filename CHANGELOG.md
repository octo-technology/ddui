3.0.5 (unreleased)
------------------

- Nothing changed yet.


3.0.4 (2019-03-17)
------------------

- Fix : breaking change with dash 0.38.* and later. back to 0.37


3.0.3 (2019-03-06)
------------------

- DD-200 : display error message when exception occures in db.retrieve_table


3.0.2 (2019-02-19)
------------------

- fix twine upload
- LICENSE Apache 2

3.0.1 (2019-02-15)
------------------

- fix the missing link_ddui_to_airflow script in the package distribution
- add coverage and unit test reports to jenkins
- make testing with the webserver easier
- fix bug : update of the task's output not working at first, when there is no user action to force reload a dag
- serve dash js libs remotely
- fix Datadriver's UI CSS to remove != alignment


3.0.0 (2019-02-08)
------------------

- Support Python 3.6
- Support Airflow 1.10.*
- Integration of plotly.Dash
- New UI with rich visualisations of output tables
- Support of any datadriver's DB like object

2.3.4 (2018-09-05)
------------------