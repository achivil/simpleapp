# -*- coding: utf-8 -*-
################################
#
#用户管理函数
#
###############################
from time import ctime
from mg import *
import json,hashlib
import pymongo

role_to_digs = {"ninestars":1,
               "admin":2,
               "publisher":4,
               "maker":8,
               "editor":16,
               "soduadmin":32,
               "adser":64,
               "checker":128
                }

class ids_role():
    '''
    '''
    def __init__(self):
        '''
        '''
        #属性值两种 True False
        self.ns_administrator = False
        self.administrator = False
        self.publisher = False
        self.maker = False
        self.editor = False

        self.role_to_digs = {"ninestars":1,
               "admin":2,
               "publisher":4,
               "maker":8,
               "editor":16,
               "soduadmin":32,
               "adser":64,
               "checker":128
                }

    def update(self,rule_number):
        '''
        更改user的role属性
        '''
        lit = []
        while rule_number != 0:
            if rule_number%2 == 1:
                lit.append(True)
            else:
                lit.append(False)
            rule_number /= 2

        self.ns_administrator, self.administrator,self.publisher,self.maker,self.editor = lit

    def info(self):
        '''
        返回user的role属性
        '''
        rule_number = 0
        if self.ns_administrator:
            rule_number +=1
        if self.administrator:
            rule_number +=2
        if self.publisher:
            rule_number +=4
        if self.maker:
            rule_number +=8
        if self.editor:
            rule_number +=16

        return rule_number



class ids_user():
    """
    """

    def __init__(self):
        """
        现在没用，只是作为数据库中表的备份记录
        """
        self.username = ""
        self.naturalname = ""
        self.password = ""
        self.userremark = ""
        self.userrole = ids_role
        self.lastlogintime = ""
        self.thislogintime = ""

        self.role_to_digs = {"ninestars":1,
               "admin":2,
               "publisher":4,
               "maker":8,
               "editor":16,
               "soduadmin":32,
               "adser":64,
               "checker":128
                }

    @staticmethod
    def user_role(userrole):
        """
        将用户的权限分解为相应的权限值
        """
        lit = []
        v = 0
        while userrole > 0:
            if userrole%2 ==1:
                lit.append(2 ** v)
            userrole /= 2
            v +=1
        return  lit

    def user_role_checker(self, role, user_info):
        result = 1
        role_list = self.user_role(user_info)
        if user_info == 2 or user_info == 3 or user_info == 33:
            # 如果用户角色是管理员（3）或超级管理员（33）立即返回正值
            #
            return result
        #print role_list
        for r in role:
            #print self.role_to_digs[r]
            #print r, role_list
            if self.role_to_digs[r] not in role_list:
                print 'user role error'
                result = -1
                return result
        return result


    def user_login(self,username,password):
        """
        """
        dic =mg_finduser(username)
        if dic == -1:
            return {'error':-3}
        elif type(dic) != dict:
            return {'error':-1}
        elif type(dic) == dict and dic["password"] !=  hashlib.md5(password).hexdigest():
            return {'error':-2}
        elif type(dic) == dict and dic["password"] ==  hashlib.md5(password).hexdigest():
            return {'error':1,'_id':dic['_id'],'username':dic['username'],'userrole':dic['userrole'],'thislogintime':dic['thislogintime'], 'system': dic['system']}
        else:
            return {'error':-5}

    def user_changelastlogintime(self,username,thislogintime):
        """
        """
        dic = mg_changetime(username,thislogintime)
        if dic == 1:
            pass
            #修改时间成功
        else:
            #失败
            pass

    def user_showalluser(self, system):
        dic = mg_showalluser(system)
        if dic != []:
            return dic
        else:
            #查询失败
            return -1

    def user_name(self, id):
        dic = mg_findusername(id)
        if dic != []:
            return dic
        else:
            #查询失败
            return -1


    def user_changepassword(self,username,oldpass,newpass ):
        '''
        修改用户本身密码
        '''
        dic = mg_finduser(username)

        if type(dic) == dict:
            if hashlib.md5(oldpass).hexdigest() == dic['password']:
                return mg_changepassword(username, hashlib.md5(newpass).hexdigest())
            else:
                return -2
        else:
            return  -1

    def user_namecheck(self,username):
        '''
        检测新建用户名是否重复
        '''
        dic = mg_namecheck(username)
        return dic

    def user_nameadd(self,username,password,userrole,naturalname,userremark, system):
        """
        添加用户
        """
        userid = mg_usercountfind()
        if userid > 0:
            dic = mg_useradd(userid,username,hashlib.md5(password).hexdigest(),int(userrole),naturalname,userremark, system)
            if dic ==1 :
                return 1
            else:
                return -3
        else:
            return -2

    def user_resetpass(self,username,newpass):
        '''
        重置密码
        '''
        dic = mg_resetpass(username,hashlib.md5(newpass).hexdigest())
        return dic

    def user_resetrole(self,username,userrole,userremark):
        """
        重置用户角色
        """
        dic = mg_resetrole(username,int(userrole),userremark)
        return dic

    def user_namedel(self,username):
        '''
        删除用户
        '''
        dic = mg_namedel(username)
        return dic


