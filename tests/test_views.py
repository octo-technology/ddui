from airflow.www.app import csrf

from ddui.views import DashAdminView


def test_init_DashAdminView_should_add_the_url_to_init_of_dash_too():
    # Given
    url = '/my/url'

    # When
    result = DashAdminView(url=url)

    # Then
    assert result.url_base_pathname == '/my/url/'


def test_add_url_should_truncat_dash_prefix_to_let_airflow_expose_the_endpoint():
    # Given
    app = DashAdminView(url='/dash')
    name = '/dash/dash-component'
    methods = ('GET')

    def func(x):
        return x

    # When
    app._add_url(name, func, methods)

    # Then
    assert ('/dash-component', func.__name__, ('GET')) in app._urls
    assert  name in app.routes

def test_add_url_should_add_the_url_to_csrf_exempt_list():
    # Given
    app = DashAdminView(url='/dash')
    name = '/dash/dash-component'
    methods = ('GET')

    def func(x):
        return x

    # When
    app._add_url(name, func, methods)

    # Then
    assert 'tests.test_views.func' in csrf._exempt_views
