# -*- coding: utf-8 -*-

from flask import make_response, render_template, request, g, redirect
from flask.views import View, MethodView
import json
from mg_advertisement import *

class AdView(View):
    methods = ['POST', 'GET']

    def __init__(self, operation):
        self.operation = operation
        self.ad_type = ''
        self.parameter_dict = {}
        self.GetParameter()

    def dispatch_request(self):
        #print 'self.operation = ', self.operation
        if self.operation == 'ReceiveInfo':
            result = self.ReceiveAdInfo()
            return make_response(json.dumps(result))
        else:
            if not session:
                return redirect('/')
            if self.operation == 'P_GetInfo':
                self.ad_type = 'P'
                result = self.GetAdInfo()
            elif self.operation == 'L_GetInfo':
                self.ad_type = 'L'
                result = self.GetAdInfoDetail()
            else:
                self.ad_type = 'A'
                result = self.GetAdInfo()
            #print result
            return make_response(json.dumps(result))

    def GetParameter(self):
        """
        获取参数
        """
        #print 'Get The Parameter'
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
                program_id = int(self.parameter_dict.pop('program_id'))
                self.parameter_dict.setdefault('program_id', program_id)

            except:
                self.error_info = {'error': 'miss parameter'}
        elif request.method == 'GET':
            #未测试是否可用
            try:
                parameter = request.args
                #print parameter
                for k, v in parameter.iteritems():
                    self.parameter_dict[k] = v
            except:
                self.error_info = {'error': 'miss parameter'}

        #print self.parameter_dict

    def GetAdInfoDetail(self):
        #print 'GetAdInfo'
        parameter_dict = self.parameter_dict

        time_list = []
        #date_info = parameter_dict['start_time']
        date_info = parameter_dict.pop('start_time')
        date_list = date_info.split('-')
        start_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        #time_list.append(str(time))
        date_info = parameter_dict.pop('end_time')
        date_list = date_info.split('-')
        #end_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])+1)
        end_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), 23, 59)
        #time_list.append(str(time))
        #print 'start time, end time: ', start_time, end_time

        query = parameter_dict
        #query = {}
        query.setdefault('date', {'$gt': start_time, '$lt': end_time})
        if self.ad_type != 'A':
            query.setdefault('type', self.ad_type)

        if session['system'] != 'NSE':
            query.setdefault('system', session['system'])

        condition = {}
        condition.setdefault('_id', 0)
        #condition.setdefault('date', 1)
        if query.has_key('playtime') and query.has_key('count'):
            try:
                play_time = query.pop('playtime')
                if play_time == 1:
                    condition.setdefault('count', 0)
            except:
                pass
            try:
                count = query.pop('count')
                if count == 1:
                    condition.setdefault('play_time', 0)
            except:
                pass

        #elif parameter_dict.has_key('count'):
        #    condition.setdefault('count', 1)

        db_connect = AdDBHandler()
        try:
            #ad_info = db_connect.FindAdInfo(query, condition)
            ad_info = db_connect.FindAdInfoDetail(query)
        except:
            ad_info = 0
            print 'get ad info error'

        return ad_info

    def GetAdInfo(self):
        #print 'GetAdInfo'
        parameter_dict = self.parameter_dict
        print parameter_dict

        time_list = []
        #date_info = parameter_dict['start_time']
        date_info = parameter_dict.pop('start_time')
        date_list = date_info.split('-')
        start_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        #time_list.append(str(time))
        date_info = parameter_dict.pop('end_time')
        date_list = date_info.split('-')
        #end_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])+1)
        end_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), 23, 59)
        #time_list.append(str(time))
        #print 'start time, end time: ', start_time, end_time

        query = parameter_dict
        #query = {}
        query.setdefault('date', {'$gt': start_time, '$lt': end_time})
        #if self.ad_type != 'A':
        #    query.setdefault('type', self.ad_type)

        if session['system'] != 'NSE':
            query.setdefault('system', session['system'])

        condition = {}
        condition.setdefault('_id', 0)
        condition.setdefault('date', 1)
        if query.has_key('playtime') and query.has_key('count'):
            if int(query['playtime']) == 1:
                condition.setdefault('play_time', 1)
            elif int(query['count']) == 1:
                condition.setdefault('count', 1)
            query.pop('count')
            query.pop('playtime')
        print 'query: '
        print query
        print 'condition: '
        print condition

        db_connect = AdDBHandler()
        try:
            #ad_info = db_connect.FindAdInfoDetail(query)
            if condition.has_key('count'):
                #print 'find count'
                ad_info = db_connect.FindAdInfo(query, condition)
            elif condition.has_key('play_time'):
                #print 'find play_time'
                ad_info = db_connect.FindAdTimeLengthInfo(query, condition)
        except:
            ad_info = 0
            print 'get ad info error'

        try:
            #返回今日数据总和
            import time
            query.pop('date')
            date_info = time.strftime('%Y-%m-%d', time.localtime())
            date_list = date_info.split('-')
            time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            query['date'] = time
            today_info = db_connect.FindTotalAdInfo(query)
        except:
            today_info = 0
        try:
            #返回历史统计综合
            query.pop('date')
            total_info = db_connect.FindTotalAdInfo(query)
        except:
            total_info = 0

        return {'ad_info': ad_info, 'today_info': today_info, 'total_info': total_info}


    def ReceiveAdInfo(self):
        parameter_dict = self.parameter_dict
        print 'receive ad info ', parameter_dict
        #新建存储广告信息
        #print 'date time is :', parameter_dict['date']
        date_info = parameter_dict.pop('date')
        #print date_info
        date_list = date_info.split('-')
        #print date_list
        date = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        #time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(date_list[3]), int(date_list[4]))
        #print date
        #print 'insert ad'
        query = parameter_dict
        query.setdefault('date', date)
        #play_time = query.pop('play_time')

        #print "ad info query: ", query

        db_connect = AdDBHandler()
        try:
            if query.has_key('play_time'):
                r = db_connect.SaveAdTimeLengthInfo(query)
                #概况统计中的时长统计
                #
            else:
                r = db_connect.SaveAdInfo(query)
                #统计信息次数、细节
                #
        except:
            print 'save ad info error'

        return 'ReceiveAdInfo'




class SimpleAdView(AdView):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if not session:
            return redirect('/')
        if self.operation == 'GetSimpleInfo':
            result = self.FindSimpleAdInfo()
            return make_response(json.dumps(result))
        elif self.operation == 'GetDefaultStatistics':
            result = self.FindDefaultStatistics()
            return make_response(json.dumps(result))

    def FindSimpleAdInfo(self):
        """
        返回系统、节目、广告组件、广告、终端的表数据
        """
        print 'the parameter_dict', self.parameter_dict
        if not self.parameter_dict:
            #print 'method get'
            query = {}
        else:
            query = self.parameter_dict

        if session['system'] != 'NSE':
            query.setdefault('system', session['system'])
        db_connect = AdDBHandler()
        try:
            result = db_connect.FindSimpleAdInfo(query)
        except:
            result = None
        #print 'Find simple ad info', result
        return result




    def FindDefaultStatistics(self):
        """
        废弃
        返回默认的统计信息 默认系统的全部广告统计信息
        """
        query = {}
        date = time.strftime('%Y-%m-%d', time.localtime())
        date_info = date
        date_list = date_info.split('-')
        date = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])-7)
        start_time = date
        date = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        end_time = date

        #query.setdefault('date', date)
        query.setdefault('date', {'$gt': start_time, '$lt': end_time})
        if session['system'] != 'NSE':
            query.setdefault('system', session['system'])

        db_connect = AdDBHandler()
        try:
            play_time = db_connect.FindAdInfo(query)
        except:
            play_time = 0
        result = play_time
        return result

