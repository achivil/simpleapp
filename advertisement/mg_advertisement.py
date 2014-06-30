# -*- coding: utf-8 -*-

from flask import make_response, render_template, request, g, session

import traceback
import json
import time
from datetime import datetime

import sys
sys.path.append("..")
from clientmanage import ids_clientmanage

#数据库操作部分

class AdDBHandler():
    def __init__(self):
        dbname = g.db_name
        self.dbconnect = g.client[dbname]
        #self.dbconnect = g.client['wispdev']
        self.db = self.dbconnect['advertisement']

    def SaveAdTimeLengthInfo(self, query):
        """
        存储、更新广告信息
        """
        #print 'save ads time length'
        db = self.dbconnect['advertisement_timelength']
        #print query['play_time']
        play_time = query.pop('play_time')
        condition = query
        #print condition
        #print play_time
        mg_request = (g.client).start_request()
        try:
            result = db.update(condition, {'$inc': {'play_time': int(play_time)}}, upsert=True)
        except Exception:
            traceback.print_exc()
            result = -1
            print 'save ad info failed ', Exception
        finally:
            mg_request.end()
        return result

    def SaveAdInfo(self, query):
        """
        存储、更新广告信息
        """
        #print 'save ads'
        db = self.dbconnect['advertisement']
        #print query['play_time']
        #play_time = query.pop('play_time')
        condition = query
        #print condition
        mg_request = (g.client).start_request()
        try:
            result = db.update(condition, {'$inc': {'count': 1}}, upsert=True)
            #result = self.db.update(condition, {'$inc': {'count': 1, 'play_time': int(play_time)}}, upsert=True)
        except:
            traceback.print_exc()
            result = -1
            print 'save ad info failed.'
        finally:
            mg_request.end()
        return result

    def FindAdInfoDetail(self, query):
        #print 'Find Ad Info query: ', query
        mg_request = (g.client).start_request()
        try:
            r = self.db.find(query, {'play_time': 0, '_id': 0})
        finally:
            mg_request.end()
        result = []
        client_handler = ids_clientmanage()
        client_info = client_handler.clientmanage_showalls(session['system'])
        client_list = {}
        for c in client_info:
            client_list[c['clientmac']] = {'name': c['clientname'], 'ip': c['clientip']}
        #print 'client_info :', client_list

        for item in r:
            new_item = item
            new_date = str(item['date'])
            if client_list.has_key(str(item['client_mac'])):
                new_mac_node = {str(item['client_mac']): client_list[str(item['client_mac'])]}
            else:
                continue

            new_item['client_mac'] = new_mac_node
            #
            new_item['date'] = new_date
            result.append(new_item)
        return result


    def FindAdInfo(self, query, condition):
        #print 'Find Ad Info query: ', query, condition
        record = {}
        db = self.dbconnect['advertisement']
        mg_request = (g.client).start_request()
        try:
            r = db.find(query, condition)
            #r = db.find(query)
        finally:
            mg_request.end()
        for item in r:
            if item['date'] not in record:
                #if item.has_key('count'):
                record.setdefault(str(item['date']), {'count': 0})
                record[str(item['date'])]['count'] += int(item['count'])
                #elif item.has_key('play_time'):
                #    record.setdefault(str(item['date']), {'play_time': 0})
                #    record[str(item['date'])]['play_time'] += int(item['play_time'])
        #print record
        return record

    def FindAdTimeLengthInfo(self, query, condition):
        print 'Find Ad Info query: ', query, condition
        record = {}
        db = self.dbconnect['advertisement_timelength']
        mg_request = (g.client).start_request()
        try:
            r = db.find(query, condition)
        finally:
            mg_request.end()
        for item in r:
            if item['date'] not in record:
                record.setdefault(str(item['date']), {'count': 0})
                record[str(item['date'])]['count'] += int(item['play_time'])
                #record.setdefault(str(item['date']), {'play_time': 0})
                #record[str(item['date'])]['play_time'] += int(item['play_time'])
        #print record
        return record


    def FindTotalAdInfo(self, query):
        """
        查找返回条件内的全部时长、次数信息
        """
        record = {}
        total_length = self.FindTotalAdLength(query)
        total_count = self.FindTotalAdCount(query)

        record.setdefault('total_length', total_length)
        record.setdefault('total_count', total_count)
        #print record
        return record



    def FindTotalAdCount(self, query):
        """
        查找返回条件内的全部次数信息
        """
        condition = {'_id': 0}

        db = self.dbconnect['advertisement']
        condition.setdefault('count', 1)

        #print 'Find Total Count query: ', query
        mg_request = (g.client).start_request()
        try:
            r = db.find(query, condition)
        finally:
            mg_request.end()
        total_count = 0
        for item in r:
            #record[total_count]是查询条件内的全部流量计数
            total_count += int(item['count'])
            #total_length是查询条件内的全部播放时长计数
        #record.setdefault('total_count', total_count)
        #print record
        return total_count


    def FindTotalAdLength(self, query):
        """
        查找返回条件内的全部时长信息
        """
        condition = {'_id': 0}

        db = self.dbconnect['advertisement_timelength']
        condition.setdefault('play_time', 1)

        #print 'Find Total Length Info query: ', query
        mg_request = (g.client).start_request()
        try:
            r = db.find(query, condition)
        finally:
            mg_request.end()
        total_length = 0
        for item in r:
            #total_length是查询条件内的全部播放时长计数
            total_length += int(item['play_time'])
        #record.setdefault('total_length', total_length)
        #print record
        return total_length


    def FindSimpleAdInfo(self, query):
        """
        返回系统、节目、终端相应的名字和id数据
        """
        import traceback
        #print 'Find Simple Ad Info'
        p_info_dic = {}

        db = self.dbconnect['advertisement_timelength']
        mg_request = (g.client).start_request()
        try:
            system = db.find({}, {'system': 1}).distinct('system')
            program = db.find({}, {'program_id': 1}).distinct('program_id')
            for p_info in db.find({}, {'program_id': 1, 'program_name': 1, '_id': 0}):
                p_info_dic.setdefault(p_info['program_id'], p_info['program_name'])
            program_names = db.find({}, {'program_name': 1}).distinct('program_name')
            ad_module = db.find({}, {'ad_module': 1}).distinct('ad_module')
            ad_name = db.find({}, {'ad_name': 1}).distinct('ad_name')
            client_mac = db.find({}, {'client_mac': 1}).distinct('client_mac')
            message = db.find({}, {'message': 1}).distinct('message')
            #program_info_list = []
            #for i in list(program):
            #    program_name = db.find_one({'program_id': i}, {'program_name'})
                #print program_name
            #    program_info_list.append({i: program_name['program_name']})

            #print list(program)
        finally:
            mg_request.end()

        db = self.dbconnect['advertisement']
        mg_request = (g.client).start_request()
        try:
            system_1 = db.find({}, {'system': 1}).distinct('system')
            program_1 = db.find({}, {'program_id': 1}).distinct('program_id')
            for p_info in db.find({}, {'program_id': 1, 'program_name': 1, '_id': 0}):
                p_info_dic.setdefault(p_info['program_id'], p_info['program_name'])
            program_names_1 = db.find({}, {'program_name': 1}).distinct('program_name')
            ad_module_1 = db.find({}, {'ad_module': 1}).distinct('ad_module')
            ad_name_1 = db.find({}, {'ad_name': 1}).distinct('ad_name')
            client_mac_1 = db.find({}, {'client_mac': 1}).distinct('client_mac')
            message_1 = db.find({}, {'message': 1}).distinct('message')
        finally:
            mg_request.end()

        #program_list = list(set(list(program_names)+list(program_names_1)))
        program_list = list(set(list(program)+list(program_1)))
        program_info_list = []
        for item in program_list:
            #print item, p_info_dic[int(item)]
            program_info_list.append({item: p_info_dic[int(item)]})

        try:
            system_info = {'system': list(set(list(system)+list(system_1)))}
            program_info = {'program': program_info_list}
            ad_module_info = {'ad_module': list(set(list(ad_module)+list(ad_module_1)))}
            ad_name_info = {'name': list(set(list(ad_name)+list(ad_name_1)))}
            message_info = {'message': list(set(list(message)+list(message_1)))}
            client_mac_info = {'client_mac': list(set(list(client_mac)+list(client_mac_1)))}
        except:
            traceback.print_exc()
            pass
        #program_info = {'program': program_info_list}
        #system_info = {'system': list(system)}
        #ad_module_info = {'ad_module': list(ad_module)}
        #ad_name_info = {'ad_name': list(ad_name)}
        #message_info = {'message': list(message)}
        #client_mac_info = {'client_mac': list(client_mac)}

        result = {}
        result.setdefault('system_info', system_info)
        result.setdefault('program_info', program_info)
        result.setdefault('ad_module_info', ad_module_info)
        result.setdefault('ad_name_info', ad_name_info)
        result.setdefault('message_info', message_info)

        client_handler = ids_clientmanage()
        client_info = client_handler.clientmanage_showalls(session['system'])
        client_list = {}
        for c in client_info:
            client_list[c['clientmac']] = {'name': c['clientname'], 'ip': c['clientip']}
        #print 'client_list : ', client_list

        new_client_mac_info = {'client_mac': []}
        for item in client_mac_info['client_mac']:
            if client_list.has_key(str(item)):
                new_item = {str(item): client_list[str(item)]}
                new_client_mac_info['client_mac'].append(new_item)
            #print new_item

        result.setdefault('client_mac_info', new_client_mac_info)
        return result

