# -*- coding: utf-8 -*-

import urllib
from flask import make_response, render_template, request,g, redirect
from flask.views import View
from werkzeug import secure_filename

from nids_file import *

import os
import sys

sys.path.append("..")
from platformcheck import platform_check
DIR, CPSSDIR = platform_check()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = DIR + 'resources'

"""
def ol_resource_http_add():
    if request.method == 'PUT' or request.method == 'POST':
        try:
            utf_filename = request.headers['Filename']
            filename = urllib.unquote(utf_filename.encode('gb2312')).decode('gb2312')
            datalen = request.headers['Datalen']
        except:
            pass

        try:
            programname = request.headers['Program']
            #print 'pre programname: ', programname
            resource_path = create_programe(programname)
        except:
            resource_path = create_programe()

        try:
            package_type = request.headers['Type']
            if package_type == 'start':
                tmp_file_name = 'tmp_' + filename
                temp_rec_file = os.path.join(resource_path, tmp_file_name)
                chuck_pos = find_end(temp_rec_file, datalen)
                return str(chuck_pos)
            else:
                return "-3"
        except:
            pass

        try:
            md5 = request.headers['Md5']
            pos = int(request.headers['Pos'])
            filelen = int(request.headers['Filelen'])
            data = request.get_data()
            programname = request.headers['Program']
        except:
            return "-2"
        #检查节目文件夹是否创建，如果已创建不做操作
        resource_path = create_programe(programname)
        if resource_path and len(data):
            w = write_file(data, filename, resource_path, pos, len(data), filelen, md5)
            r = w['error']
            return r
"""

class HttpUploadView(View):
    """
    新的Http上传类
    """
    methods = ['POST']

    def __init__(self, operation):
        self.operation = operation
        self.parameter_dict = {}
        self.data = ''
        self._getparameter()

    def dispatch_request(self):
        """
        调度函数
        """
        if self.operation == 'post':
            result = self.storeresource()
            return result

    def _getparameter(self):
        """
        获取参数
        新添加从headers获取参数
        """
        if request.method == 'POST':
            try:
                parameter_list = ['Program', 'Datalen', 'Type', 'Md5', 'Filename', 'Pos', 'Filelen']
                pre_parameter_dict = request.headers
                #print 'pre_parameter_dict', pre_parameter_dict
                pre_data = {}
                for k, v in pre_parameter_dict.iteritems():
                    if k in parameter_list:
                        pre_data[k] = v
                #print pre_data
                [self.parameter_dict.setdefault(str(key), pre_data[key].encode('utf-8')) for key in pre_data]
            except Exception:
                print 'error ', Exception
            try:
                self.data = request.get_data()
            except:
                pass
        print self.parameter_dict


    def allowed_file(self, filename):
        """
        验证文件后缀是否合法
        """
        return '.' in filename and filename.split('.')[1] in ALLOWED_EXTENSIONS

    def storeresource(self):
        """
        先实现网页http上传方式的测试用上传方式
        """
        import urllib
        try:
            utf_filename = self.parameter_dict['Filename']
            filename = urllib.unquote(utf_filename.encode('gb2312')).decode('gb2312')
            datalen = self.parameter_dict['Datalen']
        except:
            pass
        try:
            programname = self.parameter_dict['Program']
            print 'pre programname: ', programname
            resource_path = create_programe(programname)
        except:
            resource_path = create_programe()
        try:
            package_type = self.parameter_dict['Type']
            if package_type == 'start':
                tmp_file_name = 'tmp_' + filename
                temp_rec_file = os.path.join(resource_path, tmp_file_name)
                chuck_pos = find_end(temp_rec_file, datalen)
                return str(chuck_pos)
            else:
                # 传输完成之后截图，截图完成返回信号
                #
                resource_http_add(filename, 0, resource_path)
                return "-3"
        except:
            pass
        try:
            md5 = self.parameter_dict['Md5']
            pos = int(self.parameter_dict['Pos'])
            filelen = int(request.headers['Filelen'])
            programname = self.parameter_dict['Program']
            #data = request.get_data()
            data = self.data
        except:
            return "-2"
        #检查节目文件夹是否创建，如果已创建不做操作
        resource_path = create_programe(programname)
        if resource_path and len(data):
            w = write_file(data, filename, resource_path, pos, len(data), filelen, md5)
            print w
            r = w['error']
            return r




