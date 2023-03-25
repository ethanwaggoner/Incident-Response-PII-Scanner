from flask import Blueprint

blueprint = Blueprint(
    'dashboard_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/dashboard'
)
