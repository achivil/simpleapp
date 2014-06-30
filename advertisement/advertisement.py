# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, session, request, make_response, g
from jinja2 import TemplateNotFound
from advertisement_view import *



ad = Blueprint('ad', __name__, template_folder='templates/ad')

ad.add_url_rule('/store_advertisement', view_func=AdView.as_view('store_ad', operation='ReceiveInfo'))
#ad.add_url_rule('/P/get_advertisement', view_func=AdView.as_view('show_P_ad', operation='P_GetInfo'))
ad.add_url_rule('/L/get_advertisement', view_func=AdView.as_view('show_L_ad', operation='L_GetInfo'))
ad.add_url_rule('/get_advertisement', view_func=AdView.as_view('show_ad', operation='GetInfo'))
ad.add_url_rule('/get_default_statistic', view_func=SimpleAdView.as_view('default_statistic', operation='GetDefaultStatistics'))
ad.add_url_rule('/get_simple_adinfo', view_func=SimpleAdView.as_view('simple_ad_info', operation='GetSimpleInfo'))


