# -*- coding: utf-8 -*-

from pymongo import MongoClient
import pymongo
import requests
import time
import random
from bson import ObjectId
import thread
from mg import mg_get_for_test
import json

mg_host = "192.168.1.123"
mg_port = 27017
mg_user = 'nids'
mg_passwd = '111111'

client = pymongo.MongoClient(mg_host)
client.admin.authenticate(mg_user, mg_passwd)
db = client.wisp

class PublishTestView():
    def moni_write():
        import random

        s = requests.session()
        s.post('http://192.168.1.123:50095/', data={'username': 'wuyi', 'password': '123456'})

        publishID_lists = []
        #clientmac_lists = []
        r = db.publish_info.find({}, {"_id": 1, "terminals": 1})
        for p in r:
            pnode = {'publish_id': p['_id'], 'terminals': []}
            for c in p['terminals']:
                pnode['terminals'].append(c['clientmac'])
            #print pnode
            publishID_lists.append(pnode)

        pub_seed = random.randint(0, len(publishID_lists)-1)
        #print pub_seed
        client_seed = random.randint(0, len(publishID_lists[pub_seed]['terminals'])-1)
        #print client_seed
        #return 'Nope'

        publish_id = publishID_lists[pub_seed]['publish_id']
        clientmac = publishID_lists[pub_seed]['terminals'][client_seed]
        schedule = random.randint(1, 12) / 100.0
        if schedule == 0.1:
            schedule = -1
        elif schedule > 0.1:
            schedule = 1

        #print "publish_id: %s, clientmac: %s, fake schedule: %s" % (publish_id, clientmac, schedule)
        r = s.post('http://192.168.1.123:50095/program/publish_status/receive', data={'publish_id': ObjectId(publish_id),
                                                                                            'clientmac': clientmac,
                                                                                            'schedule': schedule})
        print r.content

    def moni_read():
        s = requests.session()
        s.post('http://192.168.1.123:50095/', data={'username': 'wuyi', 'password': '123456'})

        r = s.post('http://192.168.1.123:50095/program/publish_status/terminal', data={'publish_id': ObjectId(publish_id),
                                                                                      'clientmac': clientmac})
        print "read result"
        print r.content

class ProgramTestView():
    def new_program_info(self, program_id):
        import json
        s = requests.session()
        s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '123456'})
        payload = {'program_id': program_id, 'content_name': json.dumps(['data_table', 'data_relational_view'])}
        #payload = {'program_id': program_id}
        r = s.post('http://192.168.1.151:5000/newprogram/get_program_content', data=payload)
        print r.content

    def new_program_update_state(self, program_id, program_state):
        import json
        s = requests.session()
        s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '123456'})

        payload = {'program_id': program_id, 'program_state': program_state}

        r = s.post('http://192.168.1.151:5000/newprogram/update_program_state', data=payload)
        print "read result"
        s.get('http://192.168.1.151:5000/logout')

    def new_program_create(self):
        import json
        s = requests.session()
        s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '123456'})

        payload = {'programname': 'createtestprogram',
                   'programresolution': '1920x1080',
                  }

        r = s.post('http://192.168.1.151:5000/newprogram/create_program', data=payload)
        print "read result"
        s.get('http://192.168.1.151:5000/logout')

    def new_program_add(self, program_id):
        import json
        s = requests.session()
        s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '123456'})
        content_data = {}.fromkeys(['data_table',
                        'resource_table',
                        'symbol_table',
                        'schedule_table',
                        'data_relational_view',
                        'resource_relational_view',
                        'struct_relation_view',
                        'symbol_relation_view',
                        'ad_relation_view',
                        'ad_schedule_relation_view'], 'cotent!!')
        print content_data
        payload = {#'programname': 'testprogram',
                   'program_id': program_id,
                   #'programresolution': '1920x1080',
                   'content': json.dumps(content_data)
                  }

        r = s.post('http://192.168.1.151:5000/newprogram/update_program', data=payload)
        print "read result"
        print r.content
        s.get('http://192.168.1.151:5000/logout')

class ModelTestView():
    def __init__(self):
        self.s = requests.session()
        self.s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '111111'})

    def model_info(self, model_id):
        s = self.s
        payload = {'model_id': model_id}
        r = s.post('http://192.168.1.151:5000/model/get_model', data=payload)
        print r.content

    def new_program_update_state(self, program_id, program_state):
        import json
        s = requests.session()
        s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '123456'})

        payload = {'program_id': program_id, 'program_state': program_state}

        r = s.post('http://192.168.1.151:5000/newprogram/update_program_state', data=payload)
        print "read result"
        s.get('http://192.168.1.151:5000/logout')

    def model_create(self):
        s = self.s
        payload = {'modelname': 'createtestprogram',
                   'modelresolution': '1920x1080',
                   'modelremark': 'remark',
                   }

        r = s.post('http://192.168.1.151:5000/model/create_model', data=payload)
        print r.content

    def new_program_add(self, program_id):
        import json
        s = requests.session()
        s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '123456'})
        content_data = {}.fromkeys(['data_table',
                                    'resource_table',
                                    'symbol_table',
                                    'schedule_table',
                                    'data_relational_view',
                                    'resource_relational_view',
                                    'struct_relation_view',
                                    'symbol_relation_view',
                                    'ad_relation_view',
                                    'ad_schedule_relation_view'], 'cotent!!')
        print content_data
        payload = {#'programname': 'testprogram',
                   'program_id': program_id,
                   #'programresolution': '1920x1080',
                   'content': json.dumps(content_data)
        }

        r = s.post('http://192.168.1.151:5000/newprogram/update_program', data=payload)
        print "read result"
        print r.content
        s.get('http://192.168.1.151:5000/logout')


class StatTestView():
    def __init__(self):
        self.s = requests.session()
        self.s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '111111'})

    def create_info(self):
        system_list = ['NSE', u'北理工', u'其他系统']
        program_id_list = [1, 2]
        program_name_list = [u'节目1a', u'节目2d']
        #module_list = [u'广告组件1', u'什么广告what']
        name_list = [u'广告素材1', u'饭店aa', '222']
        type_list = ['P', 'L']
        client_mac_list = []

        r = self.s.get('http://192.168.1.151:5000/client')
        result = json.loads(r.content)
        for item in result['error']:
            client_mac_list.append(str(item['clientmac']))
        #client_mac_list = ['111', '222', '333', '444', '555', '666']
        #system_list = ['NSE', 'System1', '北理工', '其他系统']
        #module_list = ['module_1', '广告组件1', '什么广告', '123']
        #name_list = ['name_1', '广告素材1', '饭店', '222']
        #client_mac_list = ['111', '222', '333', '444', '555', '666']
        info_lists = [program_id_list, system_list, name_list, client_mac_list]


        program_random_num = random.randint(0, len(program_id_list)-1)
        program_id = {'program_id': program_id_list[program_random_num]}
        program_name = {'program_name': program_name_list[program_random_num]}
        system = {'system': system_list[random.randint(0, len(system_list)-1)]}
        #module = {'module': module_list[random.randint(0, len(module_list)-1)]}
        name = {'name': name_list[random.randint(0, len(name_list)-1)]}
        client_mac = {'client_mac': client_mac_list[random.randint(0, len(client_mac_list)-1)]}
        type = {'type': type_list[random.randint(0, 1)]}
        play_time = {'play_time': random.randint(1, 600)}


        parameter_list = [program_id, program_name, system, name, client_mac, play_time, type]

        info = {}
        for parameter in parameter_list:
            k = parameter.keys()[0]
            v = parameter.values()[0]
            info.setdefault(k, v)

        #date = time.strftime('%Y-%m-%d', time.localtime())
        #print date
        date = '2014-03-' + str(random.randint(1, 31))
        #print date
        info.setdefault('date', date)
        #raw_input()

        return info


    def send_info(self):
        info = self.create_info()
        info.pop('play_time')
        #print info
        r = requests.post('http://192.168.1.151:5000/statistics/store_statistics', data=info)

    def send_length_info(self):
        info = self.create_info()
        info.pop('name')
        info.pop('type')
        #print info
        r = requests.post('http://192.168.1.151:5000/statistics/store_statistics', data=info)

    def get_simple_info(self):
        #query = {'system': 'NSE'}
        query = {'program_id': 2}
        r = requests.post('http://192.168.1.151:5000/statistics/get_simple_info', data=query)
        print r.content



    def get_info(self):
        module_list = ['广告组件1', '什么广告what']
        query = {}
        #query.setdefault('program_id', 1)
        #query.setdefault('module', module_list[random.randint(0, len(module_list)-1)])

        query = self.create_info()
        query.pop('play_time')
        query.pop('date')
        query.pop('name')
        query.pop('client_mac')
        query.pop('program_id')
        query.pop('type')

        query.setdefault('start_time', '2014-03-01')
        query.setdefault('end_time', '2014-03-20')
        query.setdefault('count', 0)
        query.setdefault('playtime', 1)
        #query.setdefault('playtime', 1)
        print query
        r = self.s.post('http://192.168.1.151:5000/statistics/get_statistics', data=query)
        print r.content





class AdTestView():
    def __init__(self):
        self.s = requests.session()
        self.s.post('http://192.168.1.123:50085/', data={'username': 'wuyi', 'password': '111111'})

    def create_ad_info(self):
        system_list = ['NSE', u'北理工', u'其他系统']
        program_id_list = [1, 2]
        program_name_list = [u'节目1a', u'节目2d']
        ad_module_list = [u'广告组件1', u'什么广告what']
        ad_name_list = [u'广告素材1', u'饭店aa', '222']
        message_list = ['message1', u'消息2']
        message_type_list = ['P', 'L']
        client_mac_list = []

        r = self.s.get('http://192.168.1.123:50085/client')
        result = json.loads(r.content)
        for item in result['error']:
            client_mac_list.append(str(item['clientmac']))
        #client_mac_list = ['111', '222', '333', '444', '555', '666']
        #system_list = ['NSE', 'System1', '北理工', '其他系统']
        #ad_module_list = ['ad_module_1', '广告组件1', '什么广告', '123']
        #ad_name_list = ['ad_name_1', '广告素材1', '饭店', '222']
        #client_mac_list = ['111', '222', '333', '444', '555', '666']
        info_lists = [program_id_list, system_list, ad_module_list, ad_name_list, client_mac_list]


        program_random_num = random.randint(0, len(program_id_list)-1)
        program_id = {'program_id': program_id_list[program_random_num]}
        program_name = {'program_name': program_name_list[program_random_num]}
        system = {'system': system_list[random.randint(0, len(system_list)-1)]}
        ad_module = {'ad_module': ad_module_list[random.randint(0, len(ad_module_list)-1)]}
        ad_name = {'ad_name': ad_name_list[random.randint(0, len(ad_name_list)-1)]}
        message = {'message': message_list[random.randint(0, len(message_list)-1)]}
        client_mac = {'client_mac': client_mac_list[random.randint(0, len(client_mac_list)-1)]}
        type = {'type': message_type_list[random.randint(0, 1)]}
        play_time = {'play_time': random.randint(1, 600)}


        parameter_list = [program_id, program_name, system, ad_module, ad_name, message, client_mac, play_time, type]

        ad_info = {}
        for parameter in parameter_list:
            k = parameter.keys()[0]
            v = parameter.values()[0]
            ad_info.setdefault(k, v)

        #date = time.strftime('%Y-%m-%d', time.localtime())
        #print date
        date = '2014-03-' + str(random.randint(1, 31))
        #print date
        ad_info.setdefault('date', date)

        return ad_info


    def send_ad_info(self):
        ad_info = self.create_ad_info()
        ad_info.pop('play_time')
        #print ad_info
        r = requests.post('http://192.168.1.27:50095/advertisement/store_advertisement', data=ad_info)

    def send_ad_length_info(self):
        ad_info = self.create_ad_info()
        ad_info.pop('message')
        ad_info.pop('type')
        #print ad_info
        r = requests.post('http://192.168.1.151:5000/advertisement/store_advertisement', data=ad_info)


    def get_simple_ad_info(self):
        #query = {'system': 'NSE'}
        query = {'program_id': 2}
        r = requests.post('http://192.168.1.151:5000/advertisement/get_simple_adinfo', data=query)
        print r.content



    def get_ad_info(self):
        ad_module_list = ['广告组件1', '什么广告what']
        query = {}
        #query.setdefault('program_id', 1)
        #query.setdefault('ad_module', ad_module_list[random.randint(0, len(ad_module_list)-1)])

        query = self.create_ad_info()
        query.pop('play_time')
        query.pop('date')
        query.pop('ad_name')
        #query.pop('client_mac')
        query.pop('ad_module')
        #query.pop('program_id')
        query.pop('program_name')
        query.pop('system')
        query.pop('type')
        query.pop('message')

        query.setdefault('start_time', '2014-03-01')
        query.setdefault('end_time', '2014-03-20')
        query.setdefault('count', 0)
        query.setdefault('playtime', 1)
        r = self.s.post('http://192.168.1.151:5000/advertisement/get_advertisement', data=query)
        #r = self.s.post('http://192.168.1.151:5000/advertisement/get_simple_adinfo', data=query)
        print r.content

class DBtestView():
    def pymongo_test(self):
        mg_host = "192.168.1.123"
        mg_user = 'nids'
        mg_passwd = '111111'

        client = pymongo.MongoClient(mg_host)
        #client.admin.authenticate(mg_user, mg_passwd)
        db = client.wispdev

        mg_request = client.start_request()
        try:
            #r = list(db.publish_info.find({"_id": ObjectId(publish_id),  "$or": [{"terminals.clientmac":"94:de:80:ab:c0:a7"}, {"terminals.clientmac": "5c:f9:dd:dc:b1:17"}]}))
            #r = list(db.publish_info.find({"_id": ObjectId(publish_id), "terminals.clientmac": {"$in": ["94:de:80:ab:c0:a7", "5c:f9:dd:dc:b1:17"]}}))
            #r = db.user.find_one({'username': 'dingzhixitong2'})
            #system = r['system']
            #print type(system)
            #print system
            """
            """
            system_info = []
            program_id_list = []
            ad_module_list = []
            system_list = list(db.advertisement.distinct('system'))
            print system_list
            for system in system_list:
                program_list = list(db.advertisement.find({'system': system}).distinct('program_id'))
                print 'system ' + system + '\'s program'
                print program_list
                for program_id in program_list:
                    module_list = list(db.advertisement.find({'program_id': program_id}).distinct('ad_module'))
                    print '    program ' + str(program_id) + '\'s module'
                    print module_list
                    for module in module_list:
                        ad_list = list(db.advertisement.find({'ad_module': module}).distinct('ad_name'))
                        print '         module ' + module + '\'s ad'
                        print ad_list
                        ad_name_list = {'ad_name': ad_list}
                    ad_module_list.append({module: ad_name_list})
                program_id_list.append({program_id: ad_module_list})
            system_info.append({system: program_id_list})
        finally:
            mg_request.end()
            print system_info
            #db = client.NIDSdev
            #mg_request = client.start_request()
            #try:
            #    r = db.user.insert({'system': system})
            #    print r
            #finally:
            #    mg_request.end()

class PlayListView():
    def __init__(self):
        self.s = requests.session()
        self.s.post('http://192.168.1.151:5000/', data={'username': 'wuyi', 'password': '111111'})

    def store_play_lsit(self):
        info = {}
        tasklist = [u'1---00:00,19:38---533e983cf556d4737c31c5eb---175---04-01', u'1---19:38,19:41---533e9908f556d4737c31c5ef---175---04-01', u'1---19:41,19:44---533e9a08f556d4737c31c5f7---175---04-01', u'1---19:44,19:58---533e9ab6f556d4737c31c5fb---175---04-01', u'1---19:58,20:15---533e9d8bf556d4737c31c607---158---\u7ad6\u5c4f1', u'1---20:15,20:34---533ea19cf556d473a331c5d8---158---\u7ad6\u5c4f1', u'1---20:34,22:00---533e9d8bf556d4737c31c607---158---\u7ad6\u5c4f1', u'1---22:00,23:59---533e983cf556d4737c31c5eb---175---04-01', u'2---00:00,19:38---533e983cf556d4737c31c5eb---177---04-02', u'2---19:38,19:41---533e9908f556d4737c31c5ef---177---04-02', u'2---19:41,19:44---533e9a08f556d4737c31c5f7---177---04-02', u'2---19:44,19:58---533e9ab6f556d4737c31c5fb---177---04-02', u'2---19:58,20:15---533e9d8bf556d4737c31c607---160---\u7ad6\u5c4f2', u'2---20:15,20:34---533ea19cf556d473a331c5d8---160---\u7ad6\u5c4f2', u'2---20:34,22:00---533e9d8bf556d4737c31c607---160---\u7ad6\u5c4f2', u'2---22:00,23:59---533e983cf556d4737c31c5eb---177---04-02']

        r = self.s.get('http://192.168.1.151:5000/client')
        result = json.loads(r.content)
        client_mac_list = []
        for item in result['error']:
            client_mac_list.append(str(item['clientmac']))
        client_mac = {'client_mac': client_mac_list[random.randint(0, len(client_mac_list)-1)]}
        info.setdefault('clientmac', client_mac['client_mac'])
        info.setdefault('tasklist', json.dumps(tasklist))
        #print info
        r = requests.post('http://192.168.1.151:5000/newclient/store_playlist', data=info)
        print r.content

    def get_play_list(self, mac):
        info = {}
        info.setdefault('clientmac', mac)
        r = self.s.post('http://192.168.1.151:5000/newclient/get_playlist', data=info)
        print r.content

if __name__ == "__main__":
    #test = PlayListView()
    #test.store_play_lsit()
    #test.get_play_list('94:de:80:ab:c0:a7')
    #"""
    test = AdTestView()
    for i in xrange(1):
       test.send_ad_info()
       #test.send_ad_length_info()
    #test.get_ad_info()
    #test.get_simple_ad_info()
    #"""

    #"""
    #test = StatTestView()
    #for i in xrange(10000):
       #test.send_info()
       #test.send_length_info()
    #test.get_info()
    #test.get_simple_info()
    #"""
    #test = DBtestView()
    #test.pymongo_test()
    #new_program_info(1)
    #new_program_update_state(2, -1)
    #new_program_add(1)
    #new_program_create()
    #test = ModelTestView()
    #test.model_info(10)
    #test.model_create()
