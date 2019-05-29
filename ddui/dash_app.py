import logging
from copy import copy

from dash.dependencies import Output, Input
from dash_core_components import Tab, Tabs
from dash_html_components import Div
from flask_admin.consts import ICON_TYPE_IMAGE

from ddui import orm
# Graph dash core components needs to be imported here (because it will be included as a dash's javascript component)
from ddui import plot
from ddui.dash_components import Panel, Alert, Error
from ddui.views import DashAdminView

TABLE_OF_DAGS_HTML_ID = 'table-dags'
DAG_VIEW_HTML_ID = 'div-dag'
DAGRE_HTML_ID = 'dagre-component'
PLOT_DESCRIPTION_HTML_ID = 'describe-div'

app = DashAdminView(category='DataDriver',
                    name='Datascience UI',
                    endpoint='dash',
                    url='/dash',
                    menu_icon_type=ICON_TYPE_IMAGE,
                    menu_icon_value='brian/sigle.png',
                    external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"])

app.scripts.config.serve_locally = False
app.css.config.serve_locally = False
app.config['suppress_callback_exceptions'] = True

dags_df = orm.airflow_dags()

app.layout = Div(className='container', id='ds-ui', children=[
    Div(className="row", children=[
        Panel(head="Select a DAG", body=plot.dags_dashtable(dags_df, TABLE_OF_DAGS_HTML_ID), idHtml="div-select-dag",
              className="col-md-3"),
        Panel(head="", body="", className="col-md-12", idHtml=DAG_VIEW_HTML_ID),
    ]),
    Div(className="row", id=PLOT_DESCRIPTION_HTML_ID),
])


@app.callback(Output(DAG_VIEW_HTML_ID, 'children'),
              [Input(TABLE_OF_DAGS_HTML_ID, "value")])
def show_dag(selected_dag):
    from airflow import models, settings

    dagbag = models.DagBag(settings.DAGS_FOLDER)

    dag = dagbag.get_dag(selected_dag)

    return [Div('Click on a task to see its output', className="panel-heading"),
            Div(plot.dashdag(dag, html_id=DAGRE_HTML_ID), className="panel-body")]


@app.callback(Output(PLOT_DESCRIPTION_HTML_ID, 'children'),
              [Input(DAGRE_HTML_ID, "selectedId"),
               Input(DAGRE_HTML_ID, "selectedNodeProps")])
def show_columns(selectedId, selectedNodeProps):
    if not selectedId or not selectedNodeProps:
        return Alert('Select a task to watch the output !')

    output_table = selectedNodeProps.get('output_table', '')
    if not output_table:
        return Alert('This operator has no output_table property. Is it a DataDriver workflow ?')
    dag_id = selectedNodeProps.get('parent_dag_id', '')

    from airflow import models, settings

    dagbag = models.DagBag(settings.DAGS_FOLDER)
    fileloc = dagbag.get_dag(dag_id).fileloc
    db = _get_db_from_datadriver_dag(fileloc)
    if db is None:
        return Alert("Object named 'db' not found in {}".format(fileloc))

    logging.info("DB type is {} \t\t {}".format(type(db), db))
    try:
        df = db.retrieve_table(output_table)
    except Exception as e:
        return Error(f"An exception occured when reading output_table {output_table} : {e}")

    describe_datatable = plot.describe_dashtable(df)
    describe_bar_chart = plot.col_histograms(df)
    head_and_tail_tables = plot.head_and_tail_tables(df)
    tab_head_tail = Tab(label='Head and tail', children=[head_and_tail_tables    ])
    tab_bar_chart = Tab(label='Bar-chart by column', children=[describe_bar_chart])
    tab_describe = Tab(label='Describe frame', children=[describe_datatable])

    return Panel(
        head="Select a Tab to see the statistics on the task's output",
        body=Tabs([
            tab_describe,
            tab_bar_chart,
            tab_head_tail
        ], colors={"border": "white", "primary": "#00a9c5", "background": "#e0e0e0"})
    )


def _get_db_from_datadriver_dag(filepath):
    with open(filepath) as f:
        logging.info("Trying to get DB object from {}".format(filepath))
        local_dict = {}
        exec(f.read(), local_dict)

        if 'db' in local_dict:
            return local_dict.get('db')
        else:
            objects = copy(local_dict)
            for obj in objects.values():
                if hasattr(obj, 'retrieve_table'):
                    return obj
