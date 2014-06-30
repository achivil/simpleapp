# -*- coding: utf-8 -*-
from time import ctime
import pymongo
import json
import os, sys, string
import time

from platformcheck import platform_check
from getconf import getconfig

DIR, CPSSDIR = platform_check()

SERVERHOST = getconfig('ip_address', 'server_address')
SERVERPORT = int(getconfig('ip_address', 'server_port'))
DBHOST = getconfig('database', 'server_address')
database = getconfig('database', 'database_name')

mg_host = DBHOST
mg_port = 27017
mg_user = 'nids'
mg_passwd = '111111'

print 'mg.py ', mg_host, database
client = pymongo.MongoClient(mg_host)
# client.admin.authenticate(mg_user, mg_passwd)
db = client[database]


def mg_finduser(username):  # 事件名称
    """
    查询单个用户
    """
    mg_dic = 0
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.user.find({"username": username}):
            mg_dic = v
    except:
        mg_dic = -3
    finally:
        return mg_dic

def mg_findusername(id):
    """
    查询单个用户
    """
    mg_dic = 0
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.user.find({"_id": id}):
            mg_dic = v
    except:
        mg_dic = -3
    finally:
        return mg_dic

def mg_changetime(username, changetime):
    """
    改变登录时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.user.update({'username':username}, {"$set":{'lastlogintime':changetime, 'thislogintime':ctime()}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_showalluser(system):
    """
    显示所有用户信息
    """
    lit = []
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        if system == 'NSE':
            for v in db.user.find({'_id': {'$gt': 0}}, {'username':1, 'naturalname':1, 'userrole':1, 'userremark':1}):
                lit.append(v)
        else:
            for v in db.user.find({'_id':{'$gt':0}, 'system': system}, {'username':1, 'naturalname':1, 'userrole':1, 'userremark':1}):
                lit.append(v)
    except:
        lit = []
    finally:
        return lit

def mg_changepassword(username, newpass):
    '''
    修改密码
    '''
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.user.update({'username':username}, {"$set":{"password":newpass}})
        return 1
    except:
        return -3
    finally:
        pass

def mg_namecheck(username):
    """
    检测新建用户名是否重复
    """
    name_exrit = 1
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.user.find({'username':username}):
            name_exrit = -2
    except:
        name_exrit = -3
    finally:
        return name_exrit

def mg_usercountfind():


    try:
        v = db.user.find_and_modify(
            {'_id':0},
            {'$inc':{'count':1}},
            new=True
        )
        return int(v["count"])
    except:
        return -3
    finally:
        pass

def mg_usercountup(upnumber):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.user.update({'_id':0}, {"$set":{'count':upnumber}})
        return 1
    except:
        return -1

def mg_useradd(userid, username, password, userrole, naturalname, userremark, system):
    '''
    添加用户
    '''
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.user.insert({'_id':userid, 'username':username, 'password':password, 'userrole':userrole, 'system': system,
                        'naturalname':naturalname, 'userremark':userremark, 'lastlogintime':"", 'thislogintime':""})
        return 1
    except:
        return -3
    finally:
        pass

def mg_resetpass(username, newpass):
    '''
    重置密码
    '''
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.user.update({'username':username}, {"$set":{'password':newpass}})
        return 1
    except:
        return -3
    finally:
        pass

def mg_resetrole(username, userrole, userremark):
    '''
    重置用户角色
    '''
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.user.update({'username':username}, {"$set":{'userrole':userrole, 'userremark':userremark}})
        return 1
    except:
        return -3
    finally:
        pass

def mg_namedel(username):
    '''
    删除用户
    '''
    import traceback
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        try:
            info = db.user.find_one({'username': username}, {'system': 1})
            if info['system'] == 'NSE':
                db.programmanage.update({}, {'$pull': {'NSEcontrolusers': username}}, multi=True)
            else:
                db.programmanage.update({}, {'$pull': {'controlusers': username}}, multi=True)
        except:
            traceback.print_exc()
            pass
        db.user.remove({'username':username})
        return 1
    except:
        return -3
    finally:
        pass
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def mg_systemmanage_findone(id):
    pass


def mg_systemmanage_show(query):
    """
    查询定制系统 搜索功能
    """
    lit = []
    try :
        for v in db.systemmanage.find(query, {"systempass":False, "_id":False}):
            client_num = db.clientmanage.find({'clientsystem': v['systemname']}).count()
            v['systemtheclientnumberhave'] = client_num
            lit.append(v)
    except:
        lit = []
    finally:
        return lit

def mg_systemmanage_show1():
    """
    查询定制系统 第一种条件搜索
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({}, {"systempass":False, "_id":False}):
            print v.systemname
            client_num = db.clientmanage.count({'clientsystem': v.systemname})
            print client_num
            v['systemtheclientnumberhave'] = client_num
            lit.append(v)
    except:
        lit = []
    finally:
        return lit

def mg_systemmanage_show2(adminorname):
    """
    查询定制系统 第二种条件搜索
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({"systemadminorname":adminorname}, {"systempass":False, "_id":False}):
            lit.append(v)
    except:
        lit = []
    finally:
        return lit


def mg_systemmanage_show3(systemname):
    """
    查询定制系统 第三种条件搜索
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({"systemname":systemname}, {"systempass":False, "_id":False}):
            lit.append(v)
    except:
        lit = []
    finally:
        return lit

def mg_systemmanage_show4(systemname, adminorname):
    """
    查询定制系统 第四种条件搜索
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({"systemname":systemname, "systemadminorname":adminorname}, {"systempass":False, "_id":False}):
            lit.append(v)
    except:
        lit = []
    finally:
        return lit


def mg_systemmanage_checkname(name):
    '''
    检测定制系统管理员名是否重复
    '''
    name_exrit = 1
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({'systemadminorname':name}):
            name_exrit = -2
        for v in db.user.find({'username':name}):
            name_exrit = -2
    except:
        name_exrit = -3
    finally:
        return name_exrit

def mg_systemmanage_showone(name):
    """
    查看单一定制系统信息
    """
    dic = {}
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({"systemadminorname":name}, {"systempass":False,
                                                                  "systemtheclientnumberhave":False,
                                                                  "systemstats":False,
                                                                  "systemavlietime":False,
                                                                  "_id":False}):
            dic = v
    except:
        dic = {}
    finally:
        return dic

def mg_systemmanage_one_changeusernote(systemadminorname, realname, mail, phone, address, remark):
    '''
    添加单一系统用户信息
    '''
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.systemmanage.update({"systemadminorname":systemadminorname}, {"$set":{"realname":realname, "mail":mail,
                                                                                "phone":phone, "address":address,
                                                                                "remark":remark}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_systemmanage_oneresetpass(name, newpass):
    '''
    重置单一制定系统管理员密码
    '''
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # print name
        db.user.update({"username": name}, {"$set":{"password": newpass}})
        db.systemmanage.update({"systemadminorname":name}, {"$set":{"systempass":newpass}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_systemmanage_oneremaintime(adminorname):
    """
    查看单一定制系统授权时间
    """
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({"systemadminorname":adminorname}, {"systemavlietime":True, "_id":False}):
            return v['systemavlietime']
    except:
        return []
    finally:
        pass

def mg_systemmanage_onesetremaintime(adminorname, timelist, newtime, setremain_man):
    """
    设置单一制定系统授权时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.systemmanage.update({"systemadminorname":adminorname}, {"$push":{"systemavlietime":[timelist, newtime, setremain_man]}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_systemmanage_onecutdown(adminorname):
    """
    禁止单一指定系统使用
    """
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.systemmanage.update({"systemadminorname":adminorname}, {"$set":{"systemstats":"3"}})
        return 1
    except:
        # print "eror bokec"
        # print "error fr1st"
        return -1
    finally:
        pass

def mg_systemparty_oneipadd(adminorname, oneip):
    """
    添加定制系统ip到数据库
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # print "mg_systemparty_oneipadd: ", adminorname, oneip
        db.systemparty.find_and_modify(
                {"systemavlietime":adminorname},
                {"$set":{"systemip":oneip}},
                upsert=True)
        return 1
    except:
        return -1
    finally:
        pass

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

def mg_systemmanage_oneshowmessage(systemname):
    """
    显示单一定制系统的系统消息
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # systemadminname = db.systemmanage.find_one({'systemname': systemname}, {'_id': 0, 'systemadminorname': 1})
        # for v in db.systemmessage.find({"systemname": systemadminname['systemadminorname']},{"message":True,
        # "_id":False}):

        v = db.systemmessage.find_one({"systemname": systemname}, {"message": True, "moment": True, "_id": False})
        """
        v = db.systemmessage.find({"systemname": systemname}, {"message": True, "moment": True, "_id": False}).sort(
            'moment', 1)
        for item in v:
            lit.append(item['message'])
        print lit
        return lit
        """
        return v["message"]
    except:
        return []
    finally:
        pass

def mg_systemmanage_onesendmessage(systemname, newtime, title, text):
    """
    发送单一定制系统的系统消息
    """
    print 'system manage one send message'
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        moment = time.time()
        message_query = [newtime, title, text]
        # db.systemmessage.insert({"systemname": systemname, "message": message_query,
        #                         "moment": moment})
        db.systemmessage.update({"systemname": systemname},
                                {"$push": {"message": [newtime, title, text, moment]}},
                                upsert=True)
        return 1
    except:
        return -1
    finally:
        pass

def mg_systemmanage_getallsystemname():
    '''
    查询9s数据库里面所有定制系统的名字
    '''
    try:
        lit = []
        for v in db.systemmanage.find({}, {'systemname': 1, '_id': 0}):
            lit.append(v['systemname'])
        return lit
    except:
        return []
    finally:
        pass

def mg_systemmanage_onesendmessagallname():
    '''
    查询9s数据库里面所有定制系统的管理员名字
    '''
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # for v in db.systemmessage.find():
        for v in db.systemmanage.find():
            lit.append(v['systemadminorname'])
        return lit
    except:
        return []
    finally:
        pass

def mg_systemmanage_newone(systemname, systemadminorname, systempass, programname, rprogramname, systemavlietime, realname, mail, phone, address, remark, username, newtime):
    """
    新建定制系统
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.systemmanage.insert({"systemname":systemname, "systemadminorname":systemadminorname, "systempass":systempass,
                                "systemtheprojecthave":programname, "systemavlietime":[[systemavlietime, newtime, username]], "rprogramname":rprogramname,
                                "realname":realname, "mail":mail, "phone":phone, "address":address,
                                "remark":remark, "systemtheclientnumberhave":"", "systemstats":"1"})
        # change for test
        # print 'change the program belong to ', programname, rprogramname
        # 修改节目归属的定制系统
        #
        for p in programname:
            # if not p:
            #    continue
            # print p
            db.programmanage.update({'_id': int(p)}, {'$set': {'system': systemname}})
        # change for test
        return 1
    except:
        return -1
    finally:
        pass


def mg_mg_systemmanage_findselfname(superkey=False):
    """
    查找本系统名字 superkey:False 普通服务  True：九星服务
    """
    try:
        if superkey == False:
            # conn = pymongo.Connection(mg_host,mg_port)
            # db = conn.wisp
            for v in db.systemmanage.find({}, {"_id":False, "systemname":True}):
                return v["systemname"]
    except:
        return ""
    finally:
        pass


def mg_am_i_alive():
    """
    判断定制系统是否禁用
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find():
            return v["systemstats"]
        return "4"
    except:
        return "5"
    finally:
        pass


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def mg_clientmanage_showalls(system):
    '''
    终端管理，默认查看,返回简易信息
    '''
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        if system == 'NSE':
            for v in db.clientmanage.find({'clientsystem': system}, {"_id":False}):
                lit.append(v)
        else:
            for v in db.clientmanage.find({'clientsystem': system}, {"_id":False}):
                lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmanage_showalls_simple(system):
    '''
    终端管理，默认查看,返回简易信息 simple
    '''
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        if system == 'NSE':
            for v in db.clientmanage.find({}, {"_id":False, "clientname":True, "belongto":True, "clientstate":True, "clientmac":True}):
                lit.append(v)
        else:
            for v in db.clientmanage.find({'clientsystem': system}, {"_id":False, "clientname":True, "belongto":True, "clientstate":True, "clientmac":True}):
                lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmanage_showones(onesname):
    """
    终端管理，指定查看,返回简易信息
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmanage.find({"clientname":onesname}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmanage_showonet(onemac):
    """
    查看指定一终端消息 返回详细信息
    """
    try:
        # lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        print onemac
        for v in db.clientmanage.find({"clientmac":onemac}, {"_id":False}):
            # lit.append(v)
            return v
    except:
        return {}
    finally:
        pass
# print mg_clientmanage_showonet("5C:F9:DD:DC:B1:99")["belongto"]
def mg_clientmanage_oneremove(onemac):
    """
    移除指定终端
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.clientmanage.remove({"clientmac":onemac})
        return 1
    except:
        return -1
    finally:
        pass

def mg__clientmanage_onechangename(onemac, newname, newgroupname):
    """
    修改指定的终端名字
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.clientmanage.update({"clientmac":onemac}, {"$set":{"clientname":newname, "belongto":newgroupname}})
        return 1
    except:
        return -1
    finally:
        pass

def mg__clientmanage_onechangebelongto(onemac, newgroupname):
    """
    修改指定终端的分组
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.clientmanage.update({"clientmac":onemac}, {"$set":{"belongto":newgroupname}})
        return 1
    except:
        return -1
    finally:
        pass



def mg_clientmanage_oneshowupdowntime(onemac):
    """
    查看指定终端开关机时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmanage.find({"clientmac":onemac}, {"clientupdowntime":True}):
            return v
    except:
        return []
    finally:
        pass

def mg_clientmanage_onesetupdowntime(onemac, newtime):
    """
    修改指定终端开关机时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.clientmanage.update({"clientmac":onemac}, {"$set":{"clientupdowntime":newtime}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_clientmanage_oneplayinmita(onemac, programid, playtime):
    """
    指定终端插播节目
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # db.istpro.update({"clientmac":onemac},{"$set":{"programid":programid,"playtime":playtime}})

        # db.clientmanage.update({"clientmac":onemac},{"$set":{"insertprogram":programid,"insertprogramtime":playtime}})
        db.clientmanage.update({"clientmac":onemac}, {"$set":{"insertprogram":programid, "insertprogramtime":playtime}})
        # db.clientmanage.update({"clientmac":onemac},{"$set":{"insertprogram":programid,"insertprogramtime":playtime}})
        return 1
    except:
        return -1
    finally:
        pass


#--------------------------------------------------------------------
#--------------------------------------------------------------------

def mg_groupclientmanage_oneremove(groupname, onemac):
    '''
    从终端组移除指定终端
    '''
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.groupclientmanage.update({"groupname":groupname}, {"$pop":{"haveclient":onemac}})
        return 1
    except:
        return -1
    finally:
        pass
def mg_groupclientmanage_shoallname():
    """
    显示所有终端组名称
    """
    lit = []
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.groupclientmanage.find({}, {"groupname":True}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_groupclientmanage_oneaddhaveclient(newgroupname, onemac):
    """
    指定终端组增加终端
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.groupclientmanage.update({"groupname":newgroupname}, {"$push":{"haveclient":onemac}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_clientgroup_show(system):
    """
    终端组管理,显示全部
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.groupclientmanage.find({'groupbelongto': system}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientgroup_show_simple():
    """
    终端组管理,显示全部 simple
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.groupclientmanage.find({}, {"groupname":True, "groupbelongto":True, "haveclient": True, "_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass


def mg_clientgroup_showone(groupname):
    """
    终端组管理,显示一个
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.groupclientmanage.find({"groupname":groupname}, {'_id': 0}):
            return v

    except:
        return {}
    finally:
        pass

def mg_clientgroup_removeone(groupname):
    """
    删除指定终端组
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.groupclientmanage.remove({"groupname":groupname})
        return 1
    except:
        return -1
    finally:
        pass

def mg_clientgroup_onehaveones(groupname):
    """
    查询指定终端所组包含终端
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in  db.groupclientmanage.find({"groupname":groupname}):
            return v["haveclient"]
    except:
        return -1
    finally:
        pass


def mg_clientgroup_add(namelist, groupname, thistime, systemname):
    """
    添加终端组
    """
    lit = []
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.groupclientmanage.insert({"haveclient":namelist, "groupname":groupname, "groupupdowntime":[[], [], [], [], [], [], []],
                                     "groupinsertprogram":"", "groupinsertprogramtime":"", "groupaddtime":thistime,
                                     "groupbelongto":systemname})
        return 1
    except:
        return -1
    finally:
        pass

def mg_clientgroup_oneshowupdowntime(groupname):
    """
    查看指定终端组开关机时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.groupclientmanage.find({"groupname":groupname}, {"groupupdowntime"}):
            return v
    except:
        return []
    finally:
        pass

def mg_clientgroup_onesetupdowntime(groupname, newtime):
    """
    修改指定终端组开关机时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        lit = []
        for v in db.groupclientmanage.find({"groupname":groupname}):
            lit = v["haveclient"]
        for u in lit:
            mg_clientmanage_onesetupdowntime(u, newtime)

        db.groupclientmanage.update({"groupname":groupname}, {"$set":{"groupupdowntime":newtime}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_clientgroup__oneplayinmita(groupname, programid, playtime):
    """
    指定终端组插播节目
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        lit = []
        for v in db.groupclientmanage.find({"groupname":groupname}):
            lit = v["haveclient"]
            # print lit
        for u in lit:
            mg_clientmanage_oneplayinmita(u, programid, playtime)
            # print u
        db.groupclientmanage.update({"groupname":groupname}, {"$set":{"groupinsertprogram":programid, "groupinsertprogramtime":playtime}})
        # print 400
        return 1
    except:
        return -1
    finally:
        pass

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
def mg_programmanage_showallname(system):
    """
    显示所有节目名字
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        if system == 'NSE':
            for v in db.programmanage.find({"_id": {"$ne": 0}}, {"programname":True, "system": 1}):
                lit.append(v)
        else:
            for v in db.programmanage.find({"_id": {"$ne": 0}, 'system': system}, {"programname":True, "system": 1}):
                lit.append(v)
        return lit
    except:
        return []
    finally:
        pass







#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

def mg_status_pageshowall(starttime, endtime):
    """
    统计页面信息 0000
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1111(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "webpage":d2, "oneip":d3, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1110(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "webpage":d2, "oneip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass
def mg_status_pageshow1101(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "webpage":d2, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1100(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "webpage":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1011(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "oneip":d3, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1010(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "oneip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1001(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow1000(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "system":d1}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0111(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "webpage":d2, "oneip":d3, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0110(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "webpage":d2, "oneip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0101(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "webpage":d2, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0100(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "webpage":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0011(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "oneip":d3, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0010(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "oneip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow0001(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.statuspage.find({"inttodaytime":{"$gte":starttime, "$lte":endtime}, "onemac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_status_pageshow(starttime, endtime, d1, d2, d3, d4):
    """
     1111
    """
    try:
        lit = []
        dic = {"inttodaytime":{"$gte":starttime, "$lte":endtime}}
        if d1 != "":
            dic.setdefault("system", d1)
        if d2 != "":
            dic.setdefault("webpage", d2)
        if d3 != "":
            dic.setdefault("oneip", d3)
        if d4 != "":
            dic.setdefault("onemac", d4)

        conn = pymongo.Connection(mg_host, mg_port)
        db = conn.wisp
        for v in db.statuspage.find(dic , {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []

    finally:
        pass


def mg_status_pageshowpartget():
    """

    """
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        lit.append(db.statuspage.distinct("system"))
        lit.append(db.statuspage.distinct("webpage"))
        lit.append(db.statuspage.distinct("oneip"))
        lit.append(db.statuspage.distinct("onemac"))
        return lit
    except:
        return []

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def mg_status_showallget():
    try :
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        return db.status.distinct("almongsystem")
    except:
        return []
    finally:
        pass

def mg_status_showpart01(starttime, endtime, todaytime, yestoday, systemname):
    try:
        lit = []
        flag1 = 0
        flag2 = 0
        themax = 0
        themaxday = ""
        total = 0
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.status.find({"alonmginttoday":{"$gte":starttime, "$lte":endtime}, "almongsystem":systemname},
            {"almongtodaytime":True, "alonmgcount":True, "_id":False}):
            lit.append(v)
            if themax < v["alonmgcount"]:
                themax = v["alonmgcount"]
                themaxday = v["almongtodaytime"]
            total += v["alonmgcount"]
        for v in db.status.find({"almongtodaytime":todaytime, "almongsystem":systemname}):
            flag1 = v["alonmgcount"]
        for v in db.status.find({"almongtodaytime":yestoday, "almongsystem":systemname}):
            flag2 = v["alonmgcount"]

        return [lit, flag1, flag2, themax, themaxday, total]
    except:
        return []
    finally:
        pass

def mg_status_showpart10(starttime, endtime, todaytime, yestoday):
    try:
        lit = []
        flag1 = 0
        flag2 = 0
        themax = 0
        themaxday = ""
        total = 0
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.allstatus.find({"allinttoday":{"$gte":starttime, "$lte":endtime}},
            {"alltodaytime":True, "allcount":True, "_id":False}):
            lit.append(v)
            if themax < v["allcount"]:
                themax = v["allcount"]
                themaxday = v["alltodaytime"]
            total += v["allcount"]

        for v in db.allstatus.find({"alltodaytime":todaytime}):
            flag1 = v["allcount"]

        for v in db.allstatus.find({"alltodaytime":yestoday}):
            flag2 = v["allcount"]

        return [lit, flag1, flag2, themax, themaxday, total]
    except:
        return []
    finally:
        pass

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
def mg_homemessage(system):
    """
    首页系统消息
    """
    lit = []
    # print system
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # systemadminname = db.systemmanage.find_one({'systemname': system}, {'systemadminorname': 1})
        # for v in db.systemmessage.find({'systemname': system},{"message":True}):
        v = db.systemmessage.find_one({'systemname': system}, {"message":True})
        return v["message"]
    except:
        return []
    finally:
        pass

def mg_homeremaintime(system):
    """
    首页系统授权时间
    """
    lit = []
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find({'systemname': system}, {"systemavlietime":True}):
            # lit.append(v["systemavlietime"])
            return v["systemavlietime"]
            # print lit
        return lit
    except:
        return []
    finally:
        pass

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
def mg_clientmonitorget():

    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp

        # lit.append(db.clientmonitor.distinct("clientname"))
        # lit.append(db.clientmonitor.distinct("belongto"))
        # lit.append(db.clientmonitor.distinct("clientmac"))
        lit.append(db.clientmanage.distinct("clientname"))
        lit.append(db.clientmanage.distinct("clientsystem"))
        lit.append(db.clientmanage.distinct("clientmac"))
        return lit
    except:
        return []

def mg_clientmonitorshowpart(query):
    try:
        lit = []
        for v in db.clientmanage.find(query, {"_id":False}):
            v['belongto'] = v.pop('clientsystem')
            lit.append(v)
        return lit
    except:
        pass
    return []


def mg_clientmonitorshowpart111(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientname":d1, "belongto":d2, "clientmac":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart110(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientname":d1, "belongto":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart101(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientname":d1, "clientmac":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart100(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientname":d1}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart011(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"belongto":d2, "clientmac":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart010(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"belongto":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart001(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientmac":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitorshowpart000(d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # for v in db.clientmonitor.find({},{"_id":False}):
        for v in db.clientmanage.find({}, {"_id": False}):
            v['belongto'] = v.pop('clientsystem')
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_clientmonitor_onedetail(onemac):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientmac":onemac}):
            return v
    except:
        return {}
    finally:
        pass

def mg_clientmonitor_oneshowupdowntime(onemac):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.clientmonitor.find({"clientmac":onemac}):
            return v["clientupdowmtime"]
    except:
        return []
    finally:
        pass


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

def mg_loggingmanage_userget():
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        lit.append(db.logginguser.distinct("username"))
        lit.append(db.logginguser.distinct("usersystembelongto"))
        lit.append(db.logginguser.distinct("userip"))
        return lit
    except:
        return []



def mg_loggingmanage_usershowpart111(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "username":d1, "usersystembelongto":d2, "userip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart110(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "username":d1, "usersystembelongto":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart101(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "username":d1, "userip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart100(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "username":d1}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart011(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "usersystembelongto":d2, "userip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart010(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "usersystembelongto":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart001(starttime, endtime, d1, d2, d3):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.logginguser.find({"intusertime":{"$gte":starttime, "$lte":endtime}, "userip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_usershowpart000(starttime, endtime, d1, d2, d3):
    pass
    """
    try:
        lit = []
        #conn = pymongo.Connection(mg_host,mg_port)
        #db = conn.wisp
        ###########################
        #按照用户所属定制系统返回查询结果
        users = []
        if 1:
            for v in db.logginguser.find({"intusertime":{"$gte":starttime,"$lte":endtime}},{"_id":False}):
                lit.append(v)
        else:
            #for u in db.user.find({"system": usersystem}, {"_id": 0, "username": 1}):
                #print u
                users.append(u['username'])
        ###########################
            for v in db.logginguser.find({"intusertime":{"$gte":starttime,"$lte":endtime}},{"_id":False}):
                #print v['username']
                if v['username'] in users:
                    lit.append(v)
        return lit
    except:
        return []
    finally:
        pass
    """

def mg_loggingmanage_usershowpart(usersystem, starttime, endtime, d1, d2, d3, sort=None, start=None, end=None):
    try:
        lit = []
        count = 0
#        start = 5
#        end = 10
        dic = {"intusertime":{"$gte":starttime, "$lte":endtime}}
        if d1 != "":
            dic.setdefault("username", d1)
        if d2 != "":
            dic.setdefault("usersystembelongto", d2)
        if d3 != "":
            dic.setdefault("userip", d3)
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        users = []
        datas = []
        if usersystem == "NSE":
            datas = db.logginguser.find(dic , {"_id":False}).sort([('usertime', pymongo.DESCENDING), ])
        else:
            dic['usersystembelongto'] = usersystem
            datas = db.logginguser.find(dic , {"_id":False}).sort([('usertime', pymongo.DESCENDING), ])

        if start != None and end != None:
            count = datas.count()
            datas = datas.sort([('intusertime', pymongo.DESCENDING), ]).skip(int(start)).limit(int(end) - int(start))

        for data in datas:
            lit.append(data)

        return count, lit
    except:
        return count, []
    # for v in db.logginguser.find({"intusertime":{"$gte":starttime,"$lte":endtime},"username":d1,"usersystembelongto":d2,"userip":d3},{"_id":False}):
    #    lit.append(v)
    # dic = {"intclienttime":{"$gte":starttime,"$lte":endtime}}
    # if d1 != "":
    #    dic.setdefault("clientname",d1)

    finally:
        pass

def mg_loggingmanage_clientget():
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp

        lit.append(db.loggingclient.distinct("clientname"))
        lit.append(db.loggingclient.distinct("clientsystembelongto"))
        lit.append(db.loggingclient.distinct("clientip"))
        lit.append(db.loggingclient.distinct("clientmac"))

        return lit
    except:
        return []


def mg_loggingmanage_clientshowpart1111(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1, "clientsystembelongto":d2,
                                        "clientip":d3, "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass


def mg_loggingmanage_clientshowpart1110(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1, "clientsystembelongto":d2,
                                        "clientip":d3 }, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart1101(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1, "clientsystembelongto":d2,
                                        "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart1100(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1, "clientsystembelongto":d2}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass


def mg_loggingmanage_clientshowpart1011(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1,
                                        "clientip":d3, "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart1010(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1,
                                        "clientip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart1001(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1,
                                        "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass


def mg_loggingmanage_clientshowpart1000(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientname":d1}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart0111(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientsystembelongto":d2,
                                        "clientip":d3, "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart0110(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientsystembelongto":d2,
                                        "clientip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart0101(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientsystembelongto":d2,
                                        "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart0100(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}, "clientsystembelongto":d2
        }, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart0011(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime},
                                        "clientip":d3, "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart0010(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime},
                                        "clientip":d3}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass


def mg_loggingmanage_clientshowpart0001(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime},
                                        "clientmac":d4}, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass


def mg_loggingmanage_clientshowpart0000(starttime, endtime, d1, d2, d3, d4):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.loggingclient.find({"intclienttime":{"$gte":starttime, "$lte":endtime}
        }, {"_id":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_loggingmanage_clientshowpart(system, starttime, endtime, d1, d2, d3, d4, sort=None, start=None, end=None):
    # print 'mg_loggingmanage_clientshowpart'
    # print starttime, endtime, system
    try:
        lit = []
        dic = {"intclienttime":{"$gte":starttime, "$lte":endtime}}
        if d1 != "":
            dic.setdefault("clientname", d1)
        if d2 != "":
            dic.setdefault("clientsystembelongto", d2)
        if d3 != "":
            dic.setdefault("clientip", d3)
        if d4 != "":
            dic.setdefault("clientmac", d4)
        # print dic


        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wispdev
        users = []
        datas = []
        if system == "NSE":
            datas = db.loggingclient.find(dic, {"_id": False}).sort([('clienttime', pymongo.DESCENDING), ])
        else:
            dic['clientsystembelongto'] = system
            datas = db.loggingclient.find(dic, {"_id": False}).sort([('clienttime', pymongo.DESCENDING), ])

        if start != None and end != None:
            count = datas.count()
            datas = datas.sort([('clienttime', pymongo.ASCENDING), ]).skip(start).limit(end - start)

        for data in datas:
            lit.append(data)

        return count, lit
    except:
        return count, []
    finally:
        pass

#------------------------------------------------------------------
#------------------------------------------------------------------

def mg_programmanage_showtotal(system):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        if system == "NSE":
            for v in db.programmanage.find({'_id':{'$gt':0}}, {"_id": 1,
                                                                "programcreatetime" : 1,
                                                                # 过渡兼容用
                                                                "programmaketime" : 1,
                                                                #####################
                                                                "programmaker" : 1,
                                                                "programname" : 1,
                                                                "programpublishstate" : 1,
                                                                # 过渡兼容用
                                                                "programpublishman" : 1,
                                                                #####################
                                                                "programpublishtime" : 1,
                                                                "programresolution" : 1,
                                                                "programsize": 1,
                                                                "programupdateman": 1,
                                                                "programupdatetime": 1,
                                                                "NSEcontrolusers": 1,
                                                                "controlusers": 1,
                                                                "system" : 1}):
                # 节目权限拆分，九星用户分配节目和定制系统用户分配节目权限分离
                #
                if v.has_key('NSEcontrolusers'):
                    v['controlusers'] = v['NSEcontrolusers']
                lit.append(v)
        else:
            for v in db.programmanage.find({'_id':{'$gt':0}, 'system': system}, {"_id" : 1,
                                                                                "programcreatetime" : 1,
                                                                                # 过渡兼容用
                                                                                "programmaketime" : 1,
                                                                                #####################
                                                                                "programmaker" : 1,
                                                                                "programname" : 1,
                                                                                "programpublishstate" : 1,
                                                                                # 过渡兼容用
                                                                                "programpublishman" : 1,
                                                                                #####################
                                                                                "programpublishtime" : 1,
                                                                                "programresolution" : 1,
                                                                                "programsize" : 1,
                                                                                "programupdateman" : 1,
                                                                                "programupdatetime" : 1,
                                                                                "controlusers": 1,
                                                                                "system" : 1}):
                lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_programmanage_showtotal_simple(system):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        if system == "NSE":
            for v in db.programmanage.find({'_id':{'$gt':0}}, {"programname": True,
                                                               "programresolution": True,
                                                               "programpublishstate": True}):
                lit.append(v)
        else:
            for v in db.programmanage.find({'_id':{'$gt':0}, 'system': system}, {"programname": True,
                                                                                "programresolution": True,
                                                                                "programpublishstate": True}):
                lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_programmanage_oneshow(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.programmanage.find({"_id":id}, {"programmcontent":False}):
            return v
    except:
        return -1
    finally:
        pass

def mg_programmanage_oneedit(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.programmanage.find({"_id":id}, {"programmcontent":True, "programname":True, "programresolution":True}):
            tempv = v
            # print v
            if type(v["programmcontent"]) != dict :
                tempflag = v["programmcontent"]
                tempflag = tempflag.replace("<", "~")
                tempflag = tempflag.replace(">", "`")
                tempv["programmcontent"] = tempflag

                # print tempv
                # print tempflag
                return  tempv
            else:
                return v
    except:
        return -1
    finally:
        pass



def mg_programmanage_oneupdate(id, content, thistime, thisname):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.programmanage.update({"_id":id}, {"$set":{"programmcontent":content, "programupdatetime":thistime, "programupdateman":thisname}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_programmanage_oneremove(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.programmanage.remove({"_id":id})
        db.publish_info.remove({'program_id': id})
        return 1
    except:
        return -1
    finally:
        pass

def mg_programmanage_countfind():


    try:
        v = db.programmanage.find_and_modify(
            {'_id':0},
            {'$inc':{'count':1}},
            new=True
        )
        return int(v["count"])
    except:
        return -3
    finally:
        pass

def mg_programcountup(upnumber):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.programmanage.update({'_id':0}, {"$set":{'count':upnumber}})
        return 1
    except:
        return -1
"""
def mg_programmanage_oneadd(programname,programresolution,content,programrid,thistime,programmaker):
    try:
        #conn = pymongo.Connection(mg_host,mg_port)
        #db = conn.wisp
        db.programmanage.insert({"_id":programrid, "system": system, "programname":programname,"programresolution":programresolution,"programmcontent":content,
                                 "programmaketime":thistime,"programmaker":programmaker,"programupdatetime" : thistime,"programupdateman" : programmaker,
                                 "programsize" : "","programpublishstate" :u"未发布" ,"programpublishman" : "","programpublishtime" : ""})
        return 1
    except:
        return -1
    finally:
        pass
"""

def mg_programmanage_getonesize(id, size):
    """
    获得指定节目的大小
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.programmanage.update({'_id':id}, {"$set":{'programsize':size}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_programmanage_updateonestatus(id, username, thistime, state):
    """
    将节目的状态改为已发布
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # db.programmanage.update({'_id':id},{"$set":{'programpublishstate':u"已发布","programpublishman":username,"programpublishtime":thistime}})
        db.programmanage.update({'_id':id}, {"$set":{'programpublishstate': state, "programpublishman":username, "programpublishtime":thistime}})
        return 1
    except:
        return -1
    finally:
        pass


def mg_programmanage_oneupdatename(id, name):
    """
    修改节目名字
    """
    try:
        db.programmanage.update({'_id':id}, {'$set':{"programname":name}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_programmanage_copy(newid, id, programmaker, programname, system=None):
    """
    复制节目
    """
    try:
        v = db.programmanage.find_one({'_id': id}, {'_id': False})
        v['_id'] = newid
        v['programmaker'] = programmaker
        v['programpublishstate'] = 0
        v['NSEcontrolusers'] = []
        v['controlusers'] = []
        v['programname'] = programname
        v['system'] = 'NSE'
        db.programmanage.insert(v)
        """
        for v in db.programmanage.find({'_id':id}, {'_id':False}):
            v['_id'] = newid
            v['programmaker'] = programmaker
            # v['programupdateman'] = programmaker
            v['programpublishstate'] = 0
            v['NSEcontrolusers'] = []
            v['controlusers'] = []
            v['programname'] = programname
            if system:
                v['system'] = system
            db.programmanage.insert(v)
            break
        """
        return 1
    except:
        return -1
    finally:
        pass


def mg_programmanage_getnamelist():
    """
    获取节目名字
    """
    lit = []
    try :
        for v in db.programmanage.find({'_id':{'$gt':0}}, {'programname':1}):
            lit.append(v['programname'])
    except:
        pass
    finally:
        return lit

def mg_programmanage_getnamelist_one(id):
    """
    获取节目名字
    """
    temp_name = "thisisaprogramname"
    try :
        for v in db.programmanage.find({"_id":id}, {'programname':1}):
            temp_name = v['programname']
            break
    except:
        pass
    finally:
        return temp_name


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def mg_medalmanage_showtotal():
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.modalmanage.find({'_id':{'$gt':0}}, {"medalcontent":False}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_medalmanage_showtotal_simple():
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.modalmanage.find({'_id':{'$gt':0}}, {"medalname":True, "medalresolution":True}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_medalmanage_oneshow(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.modalmanage.find({"_id":id}, {"medalcontent":False}):
            return v
    except:
        return -1
    finally:
        pass

def mg_medalmanage_oneedit(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.modalmanage.find({"_id":id}, {"medalcontent":True, "medalname":True, "medalresolution":True}):
            tempv = v
            if type(v["medalcontent"]) != dict :
                tempflag = v["medalcontent"]
                tempflag = tempflag.replace("<", "~")
                tempflag = tempflag.replace(">", "`")
                tempv["medalcontent"] = tempflag

                # print tempv
                # print tempflag
                return  tempv
            else:
                return v
            # return  v
    except:
        return -1
    finally:
        pass

def mg_medalmanage_onesave(id, content, thistime, thisname):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.modalmanage.update({"_id":id}, {"$set":{"medalcontent":content, "medalupdatetime":thistime, "medalupdator":thisname}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_medalmanage_oneremarkupdate(id, remark):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.modalmanage.update({"_id":id}, {"$set":{"medalremark":remark}})
        return 1
    except:
        return -1
    finally:
        pass







def mg_medalmanage_oneremove(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.modalmanage.remove({"_id":id})
        return 1
    except:
        return -1
    finally:
        pass

def mg_medalmanage_countfind():

    try:
        v = db.modalmanage.find_and_modify(
            {'_id':0},
            {'$inc':{'count':1}},
            new=True
        )
        return int(v["count"])
    except:
        return -3
    finally:
        pass


def mg_medalcountup(upnumber):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.modalmanage.update({'_id':0}, {"$set":{'count':upnumber}})
        return 1
    except:
        return -1

def mg_medalmanage_oneadd(medalname, medalresolution, remark, medalid, thistime, medalbirthor):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.modalmanage.insert({"_id":medalid, "medalname":medalname, "medalresolution":medalresolution, "medalremark":remark, "medalcontent":{}
            , "medalbirthtime":thistime, "medalbirthor":medalbirthor, "medalupdatetime":"", "medalupdator":"", "medalsize":"" })
        return 1
    except:
        return -1
    finally:
        pass

def mg_medalmanage_getonesize(id, size):
    """
    获得指定模板的大小
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.modalmanage.update({'_id':id}, {"$set":{'medalsize':size}})
        return 1
    except:
        return -1
    finally:
        pass


def mg_medalmanage_oneupdatename(id, name):
    """
    修改模板名字
    """
    try:
        db.modalmanage.update({'_id':id}, {'$set':{"medalname":name}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_medalmanage_getnamelist():
    """
    获取模板名字
    """
    lit = []
    try :
        for v in db.modalmanage.find({'_id':{'$gt':0}}, {'medalname':1}):
            lit.append(v['medalname'])
    except:
        pass
    finally:
        return lit

def mg_medalmanage_getnamelist_one(id):
    """
    获取模板名字
    """
    temp_name = "thisisamodalname"
    try :
        for v in db.modalmanage.find({"_id":id}, {'medalname':1}):
            temp_name = v['medalname']
            break
    except:
        pass
    finally:
        return temp_name


def mg_medalmanage_copy(newid, id, medalbirthor, medalname):
    """
    复制模板
    """
    try :
        for v in db.modalmanage.find({'_id':id}, {'_id':False}):
            v['_id'] = newid
            v['medalbirthor'] = medalbirthor

            v['medalname'] = medalname
            db.modalmanage.insert(v)
            break
        return 1
    except:
        return -1
    finally:
        pass


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
import base64
def mg_resourcemanage_showtotal(type):
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # print db.resourcemanage.find()
        # for v in db.resourcemanage.find({"_id":0}):
        if type == "pic":
            for v in db.resourcemanage.find({"resourcetype":"jpg"}):

                if os.path.exists(DIR + v["resourcename"] + ".jpg"):
                    f = open(DIR + v["resourcename"] + ".jpg", "rb")
                    data = f.read()
                    f.close()
                    v.update({"thumbnails":base64.b64encode(data)})
                else:
                    v.update({"thumbnails":""})

                lit.append(v)

            for v in db.resourcemanage.find({"resourcetype":"png"}):

                if os.path.exists(DIR + v["resourcename"] + ".jpg"):
                    f = open(DIR + v["resourcename"] + ".jpg", "rb")
                    data = f.read()
                    f.close()
                    v.update({"thumbnails":base64.b64encode(data)})
                else:
                    v.update({"thumbnails":""})


                lit.append(v)

        else:
            for v in db.resourcemanage.find({"resourcetype":"swf"}):
                # print "resouce swf"

                if os.path.exists(DIR + v["resourcename"] + ".jpg"):
                    f = open(DIR + v["resourcename"] + ".jpg", "rb")
                    data = f.read()
                    f.close()
                    v.update({"thumbnails":base64.b64encode(data)})
                elif os.path.exists(DIR + v["resourcename"] + ".jpeg"):
                    f = open(DIR + v["resourcename"] + ".jpeg", "rb")
                    data = f.read()
                    f.close()
                    v.update({"thumbnails":base64.b64encode(data)})
                elif os.path.exists(DIR + v["resourcename"] + ".png"):
                    f = open(DIR + v["resourcename"] + ".png", "rb")
                    data = f.read()
                    f.close()
                    v.update({"thumbnails":base64.b64encode(data)})
                else:
                    v.update({"thumbnails":""})

                # v.update({"thumbnails":""})

                lit.append(v)

        return lit

        # for v in db.resourcemanage.find({"resourcetype":"jpg"}):
        # print v

        # a = open("D:\\ids\\ids_server_1.1\\static\\123.jpg",'rb')         #
        # b = open("D:\\wisp01\\123.a","w")                                   #
        #
        # base64.encode(a,b)                                                    #
        # a.close()                                                             #
        # b.close()                                                             #
        # b = open("D:\\wisp01\\123.a","r")
        #   v.update({"thumbnails":""})                                           #
        # a.close()                                                             #
        #   lit.append(v)

        # return lit

    except:

        return []
    finally:
        pass

def mg_resourcemanage_showtotal_simple():
    try:
        lit = []
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.resourcemanage.find({}, {"resourcename":True, "resourcetype":True}):
            lit.append(v)
        return lit
    except:
        return []
    finally:
        pass

def mg_resourcemanage_oneremove(id):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.resourcemanage.remove({"_id":id})
        return 1
    except:
        return -1
    finally:
        pass

def mg_resourcemanage_countfind():


    try:
        v = db.resourcemanage.find_and_modify(
            {'_id':0},
            {'$inc':{'count':1}},
            new=True
        )
        return int(v["count"])
    except:
        return -100
    finally:
        pass


def mg_resourcecountup(upnumber):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.resourcemanage.update({'_id':0}, {"$set":{'count':upnumber}})
        return 1
    except:
        return -1

def mg_resourcemanage_oneadd(resourceid, resourcename, resourcetype, resourceresolution, resourcesize, timeuoload):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.resourcemanage.insert({"_id":resourceid, "resourcename":resourcename, "resourcetype":resourcetype, "resourceresolution":resourceresolution,
                                  "resourcesize":resourcesize, "timeuoload":timeuoload})
        return 1
    except:
        return -1
    finally:
        pass


def mg_new_resourcemanage_oneadd(resourcename, resourcetype, resourcesize, resourceresolution, rrrtime, dir_id):
    """
    新的资源上传信息入库
    """
    query = {}
    query.setdefault('resourcename', resourcename)
    query.setdefault('uploadtime', rrrtime)
    query.setdefault('resourcesize', resourcesize)
    query.setdefault('resourcetype', resourcetype)
    # query.setdefault('resourceresolution', 0x0)
    query.setdefault('resourceresolution', resourceresolution)
    query.setdefault('system', 'NSE')
    query.setdefault('dir_id', dir_id)

    print query
    try:
        db.resource_files.insert(query)
        return 1
    except:
        return -1


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
def mg_icmd_status():
    """
    cmd表状态
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.update({'_id':0}, {"$set":{"status":1}})
        return 1
    except:
        return -1
    finally:
        pass
def mg_icmd_clientremoveone(mac):
    """
    移除终端
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"rmc", "cmdobject":mac})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_remove_publish(mac, publish_id):
    """
    删除发布节目 按照终端
    """
    try:
        db.icmd.insert({"cmdtype": "cpa",
                        "cmdobject": mac,
                        "publish_id": publish_id})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_publish01(onemac, programid, publish_id, playtime):
    """
    发布节目 按照终端
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"apc", "cmdobject":onemac, "cmdcontent":programid, "publish_id": publish_id, "playtime": playtime})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_publish02(grouplist, programid, publish_id, playtime):
    """
    发布节目 按照终端组
    已废弃
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"apg", "cmdobject":grouplist, "cmdcontent":programid, "publish_id": publish_id, "playtime": playtime})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_pss(mac):
    """
    终端截图
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"cps", "cmdobject":mac })
        return 1
    except:
        return -1
    finally:
        pass


def mg_icmd_setvolume(mac, volume):
    """
    终端修改音量
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"stv", "cmdobject":mac, 'value': volume })
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_groupsetvolume(groupname, volume):
    """
    终端组修改音量
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype": "stg", "cmdobject": groupname, 'value': volume })
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_clientuodowntime(mac, timelist):
    """
    终端开关机时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"cud", "cmdobject":mac, "cmdcontent":timelist})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_clientinsertplay(mac, programid, playtime):
    """
    终端插播节目
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"cip", "cmdobject":mac, "cmdcontent":programid, "cmdtime":playtime})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_groupremoveone(groupname):
    """
    删除终端组
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"rmg", "cmdobject":groupname})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_groupuodowntime(groupname, timelist):
    """
    终端组开关机时间
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"gud", "cmdobject":groupname, "cmdcontent":timelist})
        return 1
    except:
        return -1
    finally:
        pass

def mg_icmd_groupinsertplay(groupname, programid):
    """
    终端组插播节目
    """
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.icmd.insert({"cmdtype":"gip", "cmdobject":groupname, "cmdcontent":programid})
        return 1
    except:
        return -1
    finally:
        pass







def mg_badapple(mac, ip, frompage, topage, newtime, intnewtime):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        tempv = None
        for v in db.statuspage.find({"todaytime":newtime, "oneip":ip, "nextto":topage, "webpage":frompage, "onemac":mac}):
            tempv = v
        if tempv :
            db.statuspage.update({"todaytime":newtime, "oneip":ip, "nextto":topage, "webpage":frompage, "onemac":mac}, {"$set":{'count':1 + tempv["count"]}})

        else:
            db.statuspage.insert({"count":1, "todaytime":newtime, "oneip":ip, "nextto":topage, "webpage":frompage,
                                  "onemac":mac, "inttodaytime":intnewtime, "system":""})
        return 1
    except:
        return -1
    finally:
        pass

def mg_badappleall(newtime, intnewtime, newsystemname=""):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        tempv = None
        for v in db.status.find({"almongtodaytime":newtime, "almongsystem":newsystemname}):
            tempv = v
        if tempv:
            db.status.update({"almongtodaytime":newtime, "almongsystem":newsystemname}, {"$set":{"alonmgcount":1 + tempv["alonmgcount"]}})
        else:
            db.status.insert({"almongtodaytime":newtime, "almongsystem":newsystemname, "alonmginttoday":intnewtime, "alonmgcount":1})
        return 1
    except:
        return -1
    finally:
        pass

def mg_badappleallest(newtime, intnewtime):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        tempv = None
        for v in db.allstatus.find({"alltodaytime":newtime}):
            tempv = v
        if tempv:
            db.allstatus.update({"alltodaytime":newtime}, {"$set":{"allcount":1 + tempv["allcount"]}})
        else:
            db.allstatus.insert({"alltodaytime":newtime, "allinttoday":intnewtime, "allcount":1})
        return 1
    except:
        return -1
    finally:
        pass

def mg_yamasaki(mac, ip, todo, newtime, intnewtime):
    # print "mg_yamasaki start", mac
    systemname = {}
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        # print "mg_yamasaki 1"
        tempname = "resetname"
        try:
            clientname = db.clientmanage.find_one({"clientmac": mac}, {"clientname": 1})
            # print clientname["clientname"]
            tempname = clientname["clientname"]
        except:
            pass
        system_num = db.systemmanage.count()
        systemname = {'systemname': 'NSE'}
        if system_num == 1:
            systemname = db.systemmanage.find_one({}, {"systemname": 1})
        # else:
            # pass
            # if system_num > 1:
                # systemname = db.systemmanage.find_one({}, {"systemname": 1})
            #    systemname["systemname"] = "NSE"
            # else:
            #    systemname = db.systemmanage.find_one({}, {"systemname": 1})
                # print "mg_yamasaki 2"
        # print "system_name ", systemname["systemname"]
        db.loggingclient.insert({"clientmac":mac, "clientip":ip, "clienttime":newtime, "intclienttime":intnewtime, "clientwhattodo":todo,
                                 "clientsystembelongto": systemname["systemname"], "clientname": clientname['clientname']})
        return 1
    except:
        return -1

def mg_ayu(username, todosth, newtime, intnewtime, userip):
    # print "mg_ayu start"
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        system = 'NSE'

        belongto = db.user.find_one({"username": username}, {"system": 1})
        try:
            if belongto['system']:
                system = belongto['system']
        except:
            pass
        # print belongto['belongto']
        #
        # system_num = db.systemmanage.count()
        # print system_num
        """
        if system_num > 1:
            systemname = db.systemmanage.find_one({}, {"systemname": 1})
            systemname["systemname"] = "NSE"
        else:
            systemname = db.systemmanage.find_one({}, {"systemname": 1})
            #print "mg_yamasaki 2", systemname['systemname']
            #print username
            #print todosth
            #print newtime
            #print intnewtime
            #print userip
        """
        db.logginguser.insert({"username":username, "usersystembelongto": system, "userwhattodo":todosth,
                               "usertime":newtime, "intusertime":intnewtime, "userip": userip})
        print "ayu logging end"
        return 1
    except:
        print "mg logging ayu error"
        return -1
    finally:
        pass



def mg_longgingtemptemp(mac, todo):
    try:
        # print "temptemp"
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        db.clientmanage.update({"clientmac":mac}, {"$set":{"clientstate":todo}})
        return 1
    except:
        return -1
    finally:
        pass

def mg_post_fff1():
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemmanage.find():
            return v["systemadminorname"]
    except:
        return -1
    finally:
        pass

def mg_post_fff2345(name):
    try:
        # conn = pymongo.Connection(mg_host,mg_port)
        # db = conn.wisp
        for v in db.systemparty.find({"systemadminorname":name}):
            return v["systemip"]
    except:
        return -1
    finally:
        pass



def mg_get_for_test(**argv):
    list = []
    col = argv['col']
    operation = argv['opr']
    conditions = argv['conditions']
    infos = argv['infos']
    # print col, conditions, infos
    collection = db[col]
    if operation == 'find':
        for v in collection.find(conditions, infos):
            list.append(v)
    elif operation == 'find_one':
        result = collection.find_one(conditions, infos)
    elif operation == 'update':
        result = collection.update(conditions, infos)
    elif operation == 'insert':
        result = collection.insert(conditions)
    return list


if __name__ == "__main__":
    from bson import ObjectId
    publish_id = '530481e8f2ba1249c70b80d7'
    clientmac = '90:2b:34:39:16:52'
    schedule = 0.15
    # conditons = {'_id': ObjectId(publish_id), 'terminals.clientmac': clientmac}
    # infos = {'$inc': {'terminals.$.schedule': schedule}}
    conditons = {'_id': publish_id, 'terminals.clientmac': clientmac}
    infos = {}
    r = mg_get_for_test(col='publish_info', opr='find', conditions=conditons, infos=infos)
    # r = mg_get_for_test(col='publish_info', opr='update', conditions=conditons, infos=infos)
    print r


