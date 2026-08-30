"""Blueprint mapping HTTP routes to appropriate controller static methods."""

from flask import Blueprint
from controller.admin_controller import AdminController
from controller.dashboard_controller import DashboardController

focuslink_bp = Blueprint('focuslink', __name__)


@focuslink_bp.route('/admin/login', methods=['GET'])
def login_view():
    return AdminController.render_login()


@focuslink_bp.route('/admin/login', methods=['POST'])
def login_action():
    return AdminController.authenticate_admin()


@focuslink_bp.route('/admin/logout', methods=['GET'])
def logout_action():
    return AdminController.logout_admin()


@focuslink_bp.route('/', methods=['GET'])
@AdminController.require_admin_cookie
def index():
    return DashboardController.render_dashboard()


@focuslink_bp.route('/device', methods=['GET'])
@AdminController.require_admin_cookie
def device_view():
    return DashboardController.render_device_details()


@focuslink_bp.route('/timeline', methods=['GET'])
@AdminController.require_admin_cookie
def timeline_view():
    return DashboardController.render_timeline()

@focuslink_bp.route('/about', methods=['GET'])
@AdminController.require_admin_cookie
def about_view():
    return DashboardController.render_about()