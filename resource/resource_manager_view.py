# -*- coding: utf-8 -*-

from flask import make_response, render_template, request,g, redirect, url_for
from flask.views import View
from werkzeug import secure_filename

import os
import sys
import shutil
from bson import ObjectId

from mg_resource import *

sys.path.append("..")
from platformcheck import platform_check
DIR, CPSSDIR = platform_check()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = DIR + 'resources'

class ResourceView(View):
    """
    新的素材资源管理类
    """
    methods = ['GET', 'POST']

    def __init__(self, operation):
        #print url_for('new_resource_handler.static')
        self.operation = operation
        self.parameter_dict = {}
        self._getparameter()

    def dispatch_request(self):
        """
        调度函数
        """
        print self.operation
        if self.operation == 'get':
            #
            #
            return render_template('upload_resource.html')
        elif self.operation == 'store_resource':
            #
            #
            self.test_storeresource()
            #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            return redirect(url_for('new_resource_handler.show_resources'))
        elif self.operation == 'remove_resource':
            #
            #
            self.removeresource()
            #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            return redirect(url_for('new_resource_handler.show_resources'))
        elif self.operation == 'remove_tmp_resource':
            #
            #
            dir_id = self.parameter_dict['dir_id']
            resourcename = self.parameter_dict['resourcename']
            self.remove_tmp_resource(dir_id, resourcename)
            #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            return redirect(url_for('new_resource_handler.show_resources'))
        elif self.operation == 'remove_dir':
            #
            #
            pre_dir_id = self.removedir()
            print pre_dir_id
            self.parameter_dict['dir_id'] = pre_dir_id
            return redirect(url_for('new_resource_handler.show_resources'))
        elif self.operation == 'check_dirname':
            #
            #
            r = self.check_dirname()
            #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            return make_response(json.dumps(r))
        elif self.operation == 'create_dir':
            #
            #
            print 'create dir'
            r = self.create_child_dir()
            if not r:
                # 如果创建文件夹名字重复 不进行创建 返回当前文件夹信息
                #
                print 'dir has created'
                return make_response(json.dumps({'error': 'name repeat'}))
                #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            return redirect(url_for('new_resource_handler.show_resources'))
        elif self.operation == 'rename_dir':
            #
            #
            print 'rename dir'
            r = self.rename_dir()
            #self.parameter_dict['dir_id'] = self.parameter_dict['pre_dir']
            return redirect(url_for('new_resource_handler.show_resources'))
        elif self.operation == 'show_resources':
            #展示素材
            #
            print 'show resources'
            info = self.show_dir()
            #child_dirs = self.findchilddirs()
            #files = self.findfiles()
            #info = {'dir_info': r, 'child_dirs': child_dirs, 'files_info': files}
            if g.WEBFLAG == 1:
                #return make_response(json.dumps(info))
                return render_template('upload_resource.html', info=info)
                #return render_template('upload_resource.html', dir_info=r, child_dirs=child_dirs)
            else:
                #info = {'dir_info': r, 'child_dirs': child_dirs, 'files_info': files}
                return make_response(json.dumps(info))
        else:
            pass

    def _getparameter(self):
        """
        获取参数
        """
        if request.method == 'POST':
            try:
                pre_data = {}
                parameter = request.form
                #print parameter
                for k, v in parameter.iteritems():
                    pre_data[k] = v
                #[self.parameter_dict.setdefault(str(key), pre_data[key]) for key in pre_data]
                #中文编码问题。转换utf-8
                [self.parameter_dict.setdefault(str(key), pre_data[key].encode('utf-8')) for key in pre_data]
                #program_id = int(self.parameter_dict.pop('program_id'))
                #self.parameter_dict.setdefault('program_id', program_id)
                #print self.parameter_dict
            except:
                self.error_info = {'error': 'miss parameter'}
        elif request.method == 'GET':
            #未测试是否可用
            try:
                parameter = request.args
                for k, v in parameter.iteritems():
                    self.parameter_dict[k] = v
            except:
                self.error_info = {'error': 'miss parameter'}

    def test_storeresource(self):
        """
        先实现网页http上传方式的测试用上传方式
        """
        #文件存储部分
        #
        if self.parameter_dict.has_key('dir_name'):
            dir_name = self.parameter_dict['dir_name']

        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            resourcesize = os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
        #
        #

        from nids_file import create_programe as create_resource_dir
        filepath = 'res' + str(self.parameter_dict['dir_id'])
        resource_path = create_resource_dir(filepath)
        #print 'resource_path', resource_path
        shutil.move(os.path.join(UPLOAD_FOLDER, filename), os.path.join(resource_path, filename))
        #
        #数据库入库存储
        #
        import time
        from datetime import datetime
        #生成时间 使用datetime格式 mongodb中会处理成ISOdate
        #
        date_info = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        #print date_info
        date_list = date_info.split('-')
        date_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]),
                             int(date_list[3]), int(date_list[4]))
        #print date_time
        #
        #
        query = {}
        query.setdefault('resourcename', filename)
        query.setdefault('uploadtime', date_time)
        query.setdefault('resourcesize', resourcesize)
        query.setdefault('resourcetype', self.parameter_dict['type'])
        query.setdefault('resourceresolution', 0x0)
        query.setdefault('system', session['system'])
        query.setdefault('dir_id', self.parameter_dict['dir_id'])

        #print query

        db_connect = ResourceDBHandler()
        result = db_connect.storeresource(query)
        return result


    def get_dir_tree(self, dir_name):
        db_connect = ResourceDBHandler()
        try:
            dirs_path = db_connect.getdirtree(dir_name)
        except Exception:
            print Exception
        #print 'dirs_path: ', dirs_path
        return dirs_path


    def allowed_file(self, filename):
        return '.' in filename and filename.split('.')[1] in ALLOWED_EXTENSIONS


    def show_dir(self):
        if self.parameter_dict.has_key('resourcetype'):
            type = self.parameter_dict['resourcetype']
            if type == 'folder':
                type = 'all'
        else:
            type = 'all'
        dir_info = self.show_resourcesdir_info()

        """
        if type == 'all':
            child_dirs_info = self.findchilddirs()
        else:
            child_dirs_info = []
        """
        child_dirs_info = self.findchilddirs()

        for info in child_dirs_info:
            dir_name = info.pop('dir_name')
            info.setdefault('resourcename', dir_name)
            dir_id = info.pop('dir_id')
            info.setdefault('f_id', dir_id)

        pre_files_info = self.findfiles()
        #print pre_files_info
        #print child_dirs_info

        #files_info = pre_files_info
        #files_info.extend(child_dirs_info)
        files_info = child_dirs_info
        files_info.extend(pre_files_info)

        info = {'dir_info': dir_info, 'files_info': files_info}
        #info = {'dir_info': r, 'child_dirs': child_dirs, 'files_info': files}

        return info

    def show_resourcesdir_info(self):
        """
        查找返回资源文件夹信息
        """
        if (self.parameter_dict).has_key('dir_id'):
            #如果携带文件夹信息，查找并进行返回
            #
            pre_dir_id = self.parameter_dict['dir_id']
            dir_id = ObjectId(pre_dir_id)
            #print dir_id
        else:
            #如果不携带文件夹信息，返回根文件夹信息
            #
            dir_id = 'None'
        db_connect = ResourceDBHandler()
        try:
            result = db_connect.findresourcedir(dir_id)
        except Exception, data:
            print Exception, data
        #print result
        if result:
            return result
        else:
            print "create root dir"
            result = self.create_new_dir('root', 'None', 'nothing more')
            return result

    def create_child_dir(self):
        """
        创建子文件夹
        """
        print 'Create child dir'
        try:
            pre_dir_id = self.parameter_dict['dir_id']
            #print pre_dir_id
            dir_name = self.parameter_dict['new_dir_name']
            #print dir_name
        except Exception:
            print 'Get parameter failed'
            return 'error'

        if self.parameter_dict.has_key('otherinfo'):
            otherinfo = self.parameter_dict['otherinfo']
        else:
            otherinfo = ''
        try:
            r = self.check_dirname(dir_name)
            print 'new dir name check result', r
            if r:
                r = self.create_new_dir(dir_name, pre_dir_id, otherinfo)
        except Exception:
            print 'Find resource dirs error', Exception
        return r

    def check_dirname(self, dir_name):
        db_connect = ResourceDBHandler()
        try:
            r = db_connect.find_resource_dir_id(dir_name)
        except Exception:
            print Exception
        #print r
        if not r:
            return True
        else:
            return False



    def create_new_dir(self, dir_name, pre_dir_id, otherinfo):
        """
        创建新并返回的资源文件夹信息
        """
        if pre_dir_id == 'None':
            #创建根目录文件夹
            #
            query = {'pre_dir_id': pre_dir_id}
        #在pre_dir下创建子文件夹
        #
        else:
            query = {'pre_dir_id': ObjectId(pre_dir_id)}
        #query.setdefault('dir_path', [''])
        query.setdefault('dir_name', dir_name)
        query.setdefault('other_info', otherinfo)

        db_connect = ResourceDBHandler()
        try:
            r = db_connect.find_resource_dir_id(dir_name)
        except Exception:
            print Exception
        if r:
            # 如果文件夹重名则返回-1 文件夹唯一标识是_id
            #
            print 'this file name is already used.'
            result = -1
        else:
            #没有文件夹没有重名，可以创建
            #
            try:
                r = db_connect.createresoucedir(query)
            except Exception:
                print Exception
            result = db_connect.findresourcedir(ObjectId(r))
        print result
        return result

    def rename_dir(self):
        """
        重命名素材文件夹名字
        """
        try:
            dir_id = self.parameter_dict['old_dir_id']
            new_name = self.parameter_dict['newname']
            show_id = self.parameter_dict['dir_id']
        except Exception:
            print 'get parameters failed'
            return -1
        query = {}
        query.setdefault('_id', ObjectId(dir_id))
        condition = {}
        condition.setdefault('dir_name', new_name)

        db_connect = ResourceDBHandler()
        try:
            r = db_connect.renamedir(query, condition)
        except Exception:
            print Exception
        result = db_connect.findresourcedir(ObjectId(show_id))
        #print result
        return 1

    def findchilddirs(self):
        if self.parameter_dict.has_key('dir_id'):
            dir_id = self.parameter_dict['dir_id']
        else:
            dir_id = 'None'

        db_connect = ResourceDBHandler()
        try:
            r = db_connect.findchilddirs(dir_id)
        except Exception:
            #print Exception
            r = ''
        #finally:
        #    result = db_connect.findresourcedir(dir_name)
        #print r
        return r

    def findfiles(self):
        if self.parameter_dict.has_key('dir_id'):
            dir_id = self.parameter_dict['dir_id']
        else:
            dir_id = 'None'
        if self.parameter_dict.has_key('resourcetype'):
            type = self.parameter_dict['resourcetype']
            if type == 'folder':
                type = 'all'
            #if type != 'swf':
            #    type = 'pic'
        else:
            type = 'all'

        #query = {'_id': dir_id}
        #print query
        db_connect = ResourceDBHandler()
        try:
            r = db_connect.findfiles(dir_id, type)
        except Exception:
            print Exception
            r = '-1'
        #finally:
        #    result = db_connect.findresourcedir(dir_name)
        #print r
        return r





    def storeresource(self, r_filename, filesize, r_type, r_resolution, dir_id):
        """
        资源信息数据库入库
        """
        #
        #数据库入库存储, 暂时没有使用，入库调用函数在othersth里，上传完毕就处理完了
        #
        import time
        from datetime import datetime
        #生成时间 使用datetime格式 mongodb中会处理成ISOdate
        #
        date_info = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        #print date_info
        date_list = date_info.split('-')
        date_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]),
                             int(date_list[3]), int(date_list[4]))
        #print date_time
        #
        #
        query = {}
        query.setdefault('resourcename', r_filename)
        query.setdefault('uploadtime', date_time)
        query.setdefault('resourcesize', filesize)
        query.setdefault('resourcetype', r_type)
        query.setdefault('resourceresolution', r_resolution)
        query.setdefault('system', session['system'])
        query.setdefault('dir_id', ObjectId(dir_id))
        #query.setdefault('dir_id', dir_id)

        #print query

        db_connect = ResourceDBHandler()
        result = db_connect.storeresource(query)


    def removedir(self):
        """
        删除素材文件夹
        """
        pre_dir_id = self.parameter_dict['dir_id']

        dir_id = ObjectId(pre_dir_id)
        db_connect = ResourceDBHandler()
        result = db_connect.removedir(dir_id)

        dir_path = os.path.join(UPLOAD_FOLDER, 'res'+str(pre_dir_id))
        try:
            shutil.rmtree(dir_path)
        except:
            #print 'remove dir failed'
            pass
        return result

    def removeresource(self):
        """
        删除素材资源
        """
        resource_id = self.parameter_dict['resource_id']
        db_connect = ResourceDBHandler()

        r_info = db_connect.get_file_info(resource_id)
        r_path = os.path.join(UPLOAD_FOLDER, os.path.join('res'+str(r_info['dir_id']), r_info['resourcename']))
        try:
            os.remove(r_path)
        except:
            print 'remove file failed'
        result = db_connect.removeresource(resource_id)
        return result

    def remove_tmp_resource(self, dir_id, resourcename):
        """
        删除上传中的素材资源
        """
        print 'remove tmp resource'
        r_path = os.path.join(UPLOAD_FOLDER, os.path.join('res'+str(dir_id), resourcename))
        if os.path.isfile(r_path):
            pass
        else:
            r_path = os.path.join(UPLOAD_FOLDER, os.path.join('res'+str(dir_id), 'tmp_'+resourcename))
        print r_path
        try:
            os.remove(r_path)
            result = True
        except:
            print 'remove file failed'
            result = False
            pass
        return result


