# Graph dash core components needs to be imported here (module level) to work fine
from dash_core_components import Graph, Dropdown
from dash_dagre import DagreD3
from dash_html_components import Div, H5
from dash_table import DataTable
from plotly.graph_objs import Histogram, Figure, Layout


def dags_dashtable(dags, html_id):

    dags_list = Dropdown(
        id=html_id,
        options=[
            {'label': dag_id, 'value': dag_id} for dag_id in dags
        ],
    )

    return dags_list


def col_histograms(df):
    """
    Generate plotly.Dash's Bar chart component. One barchart for each column of the dataframe
    :param df: pandas.DataFrame
    :return: dash_core_components.Graph
    """
    describe_bar_chart = Div(children=[])
    for col in df.columns:
        t = Histogram(x=df[col], name=col)
        l = Layout(title='Histogram for colunm {}'.format(t.name),
            autosize=False,
            width=500,
            height=500,
            margin={
                'l': 50,
                'r': 50,
                'b': 100,
                't': 100,
                'pad': 4
            })
        fig = Figure(data=[t], layout=l)
        g = Graph(figure=fig,className="col-sm-4", config={'staticPlot': True, 'responsive': True})
        describe_bar_chart.children.append(g)

    return describe_bar_chart


def describe_dashtable(df):
    """
    Generate a dash_table.DataTable component with data from dataframe.describe() function
    :param df:
    :return:
    """
    describe_dataframe = df.describe(include='all').reset_index()
    describe_datatable = Div(className="table-responsive-sm-6", children=[
        H5("Pandas' describe"),
        DataTable(
            columns=[{"name": i, "id": i} for i in describe_dataframe.columns],
            data=describe_dataframe.to_dict("rows")
        )])
    return describe_datatable


def head_and_tail_tables(df):
    head = df.head()
    tail = df.tail()
    head_and_tail = Div(children=[
        Div(className="table-responsive-sm-4", children=[
            H5("Pandas' Head"),
            DataTable(
                columns=[{"name": i, "id": i} for i in head.columns],
                data=head.to_dict("rows")
            )]),
        Div(className="table-responsive-sm-4", children=[
            H5("Pandas' Tail"),
            DataTable(
                columns=[{"name": i, "id": i} for i in tail.columns],
                data=tail.to_dict("rows")
            )])
        ,
    ])
    return head_and_tail


def dashdag(dag=None, html_id=None):
    """
    Generate a DagreD3 component, showing a Directed Acyclic Graph from Airflow's models.DagBag object
    :param dag_roots:
    :param tasks:
    :return:
    """
    if dag is None :
        return Div(DagreD3(id=html_id, nodes=[], edges=[]))

    task_id_mapping = {}
    nodes = {}
    edges = []
    for i, task in enumerate(dag.tasks):
        task_id_mapping[task.task_id] = i
        nodes[i] = {
            'parent_dag_id': dag.dag_id,
            'label': task.task_id,
            'labelStyle': "fill:{0};".format(task.ui_fgcolor),
            'style': "fill:{0};".format(task.ui_color),
            'rx': 5,
            'ry': 5,
            'output_table': getattr(task, "output_table", "")
        }

    def get_upstream(task):
        for t in task.upstream_list:
            edge = [task_id_mapping[t.task_id], task_id_mapping[task.task_id], {'curve': 'd3.curveBasis'}]

            if edge not in edges:
                edges.append(edge)
                get_upstream(t)

    for t in dag.roots:
        get_upstream(t)

    return Div(DagreD3(id=html_id, nodes=nodes, edges=edges, width='50%'), style={"background-color": " #f2f2f2"})
