from dash_html_components import Div, Button, Span, Strong


def Panel(head, body, idHtml=None, className=None):
    return Div(id=idHtml, className=f"panel panel-default {className}", children=[
        Div(head, className="panel-heading"),
        Div(body, className="panel-body")
    ])


def Alert(message):
    return Div(id="alert-div",
               className="alert alert-warning alert-dismissible",
               children=[
                   Button(className="close", type='button',
                          children=[Span("x")], **{"data-dismiss": "alert", "aria-label": "Close"}),
                   Strong("Warning!"),
                   f" {message}",
               ]
               )


def Error(message):
    return Div(id="alert-div",
               className="alert alert-danger alert-dismissible",
               children=[
                   Strong("Error!"),
                   f" {message}",
               ]
               )
