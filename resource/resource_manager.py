#-*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, session, request, make_response, g
from resource_manager_view import *

new_resource_handler = Blueprint('new_resource_handler', __name__, template_folder='..templates', static_folder='../static/resources')

new_resource_handler.add_url_rule('/web_add_resource', view_func=ResourceView.as_view('web_add_resource', operation='get'))
new_resource_handler.add_url_rule('/store_resource', view_func=ResourceView.as_view('store_resource', operation='store_resource'))
new_resource_handler.add_url_rule('/remove_resource', view_func=ResourceView.as_view('remove_resource', operation='remove_resource'))
new_resource_handler.add_url_rule('/remove_tmp_resource', view_func=ResourceView.as_view('remove_tmp_resource', operation='remove_tmp_resource'))
new_resource_handler.add_url_rule('/remove_dir', view_func=ResourceView.as_view('remove_dir', operation='remove_dir'))
new_resource_handler.add_url_rule('/check_dirname', view_func=ResourceView.as_view('check_dirname', operation='check_dirname'))
new_resource_handler.add_url_rule('/create_dir', view_func=ResourceView.as_view('create_dir', operation='create_dir'))
new_resource_handler.add_url_rule('/rename_dir', view_func=ResourceView.as_view('rename_dir', operation='rename_dir'))
new_resource_handler.add_url_rule('/resource', view_func=ResourceView.as_view('show_resources', operation='show_resources'))
