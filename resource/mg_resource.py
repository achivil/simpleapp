# -*- coding: utf-8 -*-

from flask import make_response, render_template, request, g, session

from bson import ObjectId
import json
import time
from datetime import datetime

import sys
sys.path.append("..")
#数据库操作部分

class ResourceDBHandler():
    def __init__(self):
        dbname = g.db_name
        self.dbconnect = g.client[dbname]
        #self.dbconnect = g.client['wispdev']
        self.db = self.dbconnect['resources_lib_info']

    def createresoucedir(self, query):
        print 'create new resources dir', query
        pre_dir_id = query['pre_dir_id']
        #print pre_dir_id
        mg_request = (g.client).start_request()
        try:
            if pre_dir_id == 'None':
                dir_path = []
            else:
                pre_dir_info = self.db.find_one({'_id': pre_dir_id}, {'dir_path': 1, 'dir_name': 1})
                dir_path = pre_dir_info['dir_path']
                dir_path.append(pre_dir_info['dir_name'])
            query.setdefault('dir_path', dir_path)
            #print 'query', query
            r = self.db.insert(query)
            #print 'mg_resource createresource dir r = ', r
        except Exception:
            print Exception
        finally:
            mg_request.end()
        return r

    def renamedir(self, query, pre_condition):
        condition = {'$set': pre_condition}
        print 'rename dir ', query, condition
        mg_request = (g.client).start_request()
        try:
            r = self.db.update(query, condition)
        except Exception:
            print Exception
        finally:
            mg_request.end()
        #print r
        return r

    def find_resource_dir_id(self, dir_name):
        print 'find resources dir by name', dir_name
        mg_request = (g.client).start_request()
        try:
            r = self.db.find_one({'dir_name': dir_name}, {'_id': 1})
        except Exception:
            print Exception
        finally:
            mg_request.end()
        #print r
        #if r:
        #    print 'r is true'
        #else:
        #    print 'r is false'
        return r


    def findresourcedir(self, dir_id):
        print 'find resource dir', dir_id
        if dir_id == 'None':
            mg_request = (g.client).start_request()
            try:
                r = self.db.find_one({'dir_name': 'root'})
            except Exception:
                print Exception
            finally:
                mg_request.end()
        else:
            mg_request = (g.client).start_request()
            try:
                r = self.db.find_one({'_id': dir_id})
            except Exception:
                print Exception
            finally:
                mg_request.end()
        try:
            dir_id = r.pop('_id')
            r.setdefault('dir_id', str(dir_id))
            pre_dir_id = r.pop('pre_dir_id')
            r.setdefault('pre_dir_id', str(pre_dir_id))
        except Exception:
            r = 0
        #print "r value: ", r
        return r



    def findchilddirs(self, dir_id):
        print 'find child dirs', dir_id
        if dir_id == 'None':
            mg_request = (g.client).start_request()
            try:
                pre_dir_id = self.db.find_one({'dir_name': 'root'})
                #print 'find child dirs pre_dir_id: ', pre_dir_id['_id']
                dir_id = str(pre_dir_id['_id'])
            except Exception:
                print Exception
            finally:
                mg_request.end()
        mg_request = (g.client).start_request()
        try:
            r = self.db.find({'pre_dir_id': ObjectId(dir_id)})
        except Exception:
            print Exception
        finally:
            mg_request.end()
        #print r
        result = list(r)
        try:
            for item in result:
                item.setdefault('r_type', 'dir')
                dir_id = item.pop('_id')
                #print str(dir_id)
                item.setdefault('dir_id', str(dir_id))
                pre_dir_id = item.pop('pre_dir_id')
                #print str(pre_dir_id)
                item.setdefault('pre_dir_id', str(pre_dir_id))
        except:
            result = 0
        #print "result value: ", result
        return list(result)


    def findfiles(self, dir_id, type='all'):
        print 'find files', dir_id
        print 'find files TYPE : ', type
        if dir_id == 'None':
            mg_request = (g.client).start_request()
            try:
                pre_dir_id = self.db.find_one({'dir_name': 'root'})
                #print 'find child dirs pre_dir_id: ', pre_dir_id['_id']
                dir_id = str(pre_dir_id['_id'])
            except Exception:
                print Exception
            finally:
                mg_request.end()

        db = self.dbconnect['resource_files']
        mg_request = (g.client).start_request()
        try:
            if type == 'all':
                #r = db.find({'dir_id': dir_id}, {'resourcename': 1, 'resourcetype': 1})
                r = db.find({'dir_id': dir_id})
            elif type == 'swf':
                #r = db.find({'dir_id': dir_id, 'resourcetype': 'swf'}, {'resourcename': 1, 'resourcetype': 1})
                r = db.find({'dir_id': dir_id, 'resourcetype': 'swf'})
            elif type == 'video':
                r = db.find({'dir_id': dir_id, 'resourcetype': {'$nin': ['swf', 'jpg', 'jpeg', 'peg', 'png']}})
            else:
                #r = db.find({'dir_id': dir_id, 'resourcetype': {'$ne': 'swf'}}, {'resourcename': 1, 'resourcetype': 1})
                r = db.find({'dir_id': dir_id, 'resourcetype': {'$ne': 'swf'}})
        except Exception:
            print Exception
        finally:
            mg_request.end()
        result = list(r)
        try:
            for item in result:
                item.setdefault('r_type', 'file')
                f_id = item.pop('_id')
                #print str(f_id)
                item.setdefault('f_id', str(f_id))
                uploadtime = item.pop('uploadtime')
                #print str(uploadtime)
                item.setdefault('uploadtime', str(uploadtime))
                #[item.setdefault(str(key), item[key].encode('utf-8')) for key in item]
        except:
            result = 0
        #print "result value: ", result
        return list(result)

    def get_file_info(self, resource_id):
        """
        通过素材id获取素材信息
        """
        print 'get resource file info'
        db = self.dbconnect['resource_files']
        mg_request = (g.client).start_request()
        try:
            r = db.find_one({'_id': ObjectId(resource_id)})
        except Exception:
            print Exception
        finally:
            mg_request.end()
        return r



    def storeresource(self, query):
        """
        素材信息存入数据库
        """
        print 'store resource info'
        #self.db = self.dbconnect['resources_lib_info']
        db = self.dbconnect['resource_files']
        resourcename = query['resourcename']
        #info = 'aha'
        mg_request = (g.client).start_request()
        try:
            #info = db.insert(query)
            info = db.update({'resourcename': resourcename}, query, upsert=True)
        except Exception:
            pass
        finally:
            mg_request.end()

        return info

    def removedir(self, dir_id):
        """
        数据库操作 删除 资源文件夹
        """
        print 'remove dir: ', dir_id
        db = self.dbconnect['resource_files']
        mg_request = (g.client).start_request()
        try:
            #print 'remove resources in dir'
            r = db.remove({'dir_id': ObjectId(dir_id)})
        except Exception:
            print Exception
        finally:
            mg_request.end()

        mg_request = (g.client).start_request()
        try:
            print 'remove dir'
            r = self.db.find_one({'_id': ObjectId(dir_id)}, {'pre_dir_id': 1})
            #print r
            if r['pre_dir_id'] == 'None':
                result = 'None'
            else:
                result = str(r['pre_dir_id'])
            r = self.db.remove({'_id': dir_id})
        except Exception:
            print Exception
        finally:
            mg_request.end()
        return result

    def removeresource(self, resource_id):
        """
        数据库操作 删除 资源
        """
        print 'remove resource: ', resource_id
        db = self.dbconnect['resource_files']
        mg_request = (g.client).start_request()
        try:
            #print 'remove resources'
            r = db.remove({'_id': ObjectId(resource_id)})
        except Exception:
            print Exception
        finally:
            mg_request.end()
        return r

