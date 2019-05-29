from airflow.www.app import csrf
from dash import Dash
from flask_admin import expose, AdminIndexView
from flask import Markup
from flask import request



class DashAdminView(AdminIndexView, Dash):

    def __init__(self, external_stylesheets=None, **kwargs):
        AdminIndexView.__init__(self, **kwargs)
        url_base_of_dash = kwargs.get('url') + '/'
        Dash.__init__(self, url_base_pathname=url_base_of_dash, external_stylesheets=external_stylesheets, **kwargs)


    @expose('/')
    def index(self):
        """
        AdminView
        """

        return Dash.index(self)


    def _add_url(self, name, view_func, methods=('GET',)):
        """
        From Dash
        """
        csrf.exempt(view_func)
        self._urls.append((name.replace('/dash/', '/'), view_func.__name__, methods))
        self.routes.append(name)

    def interpolate_index(self,
                          metas='', title='', css='', config='',
                          scripts='', app_entry='', favicon='', renderer=''):
        """
        From Dash : interpolate_index
        """
        content = self.render('brian/dash.html',
                              app_entry=app_entry,
                              dash_config=config,
                              scripts=scripts)
        return '{}'.format(content)



    @expose('/version')
    def version(self):
        content = "Plugin's Version : {}"
        import pkg_resources
        version = pkg_resources.get_distribution("ddui").version

        return self.render('brian/dash.html', app_entry=content.format(version), title="Datadriver - Version")