from flask import Blueprint
from flask_admin.base import MenuLink
from flask_admin.consts import ICON_TYPE_IMAGE

from ddui.dash_app import app as dash_view
from airflow.plugins_manager import AirflowPlugin


ml_repo_website = MenuLink(
    category='DataDriver',
    name='Git repository',
    url='https://gitlab.octo.com/dd/ddui.git',
    icon_type=ICON_TYPE_IMAGE,
    icon_value='brian/git.png'
)

ml_doc = MenuLink(
    category='DataDriver',
    name='DataDriver API documentation',
    url='http://datadriver-doc-ddapi.s3-website-eu-west-1.amazonaws.com/',
    icon_type=ICON_TYPE_IMAGE,
    icon_value='brian/sigle.png'
)

ml_version = MenuLink(
    category='DataDriver',
    name='Version',
    url='/dash/version',
    icon_type=ICON_TYPE_IMAGE,
    icon_value='brian/sigle.png'
)


brian_bp = Blueprint(
    "brian_web", __name__,
    template_folder='templates',
    static_folder='static/brian',
    static_url_path='/static/brian',
)

class DataDriverUIPlugin(AirflowPlugin):
    name = 'DataDriver UI Plugin'
    operators = []
    hooks = []
    executors = []
    macros = []
    admin_views = [dash_view]
    flask_blueprints = [brian_bp]
    menu_links = [ml_doc, ml_repo_website, ml_version]