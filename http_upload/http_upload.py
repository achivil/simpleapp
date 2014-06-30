#-*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, session, request, make_response, g
from http_upload_view import *

resource_upload = Blueprint('http_upload', __name__, template_folder='..templates')

resource_upload.add_url_rule('/resource/http_add', view_func=HttpUploadView.as_view('http_upload', operation='post'))
