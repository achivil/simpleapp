# -*- coding: utf-8 -*-

import time
from datetime import datetime
from time import ctime
from mg import *
import json ,hashlib
from SocketServer import BaseRequestHandler
import shutil
from SocketServer import ThreadingTCPServer
import SocketServer,os
from get_thumb import *
from PIL import Image

from platformcheck import platform_check, lite_platform_check
from getconf import *

#TCPHOST, TCPPORT = "192.168.1.26", 2002
TCPHOST = getconfig('ip_address', 'server_address')
TCPPORT = int(getconfig('ip_address', 'tcp_port'))

DIR, CPSSDIR = platform_check()
OTHDIR = os.path.join(DIR, 'resources')
#print "othersth.py", OTHDIR, CPSSDIR, DIR, TCPHOST, TCPPORT
PIC_TYPE = ['jpg', 'png', 'jpeg']
VIDEO_TYPE = ['swf', 'flv', 'mp4']

def resource_http_add(resourcename, resourcesize, resourcepath):
    try:
        rrrname = resourcename
        #rrrtype = resourcename[-3:]
        rrrtype = resourcename.split('.')[1].lower()
        date_info = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        #print date_info
        date_list = date_info.split('-')
        date_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]),
                             int(date_list[3]), int(date_list[4]))
        #print date_time
        upload_time = date_time
        r_path = resourcepath
        #rrrsize = resourcesize
        rrrsize = os.path.getsize(os.path.join(r_path, resourcename))

        if rrrtype == "png":
            rrrtion = "0,0"
        else:
            rrrtion = "0,0"

        #resourceid = mg_resourcemanage_countfind()
        print 'r_path = ', r_path
        #素材文件上传后直接保存到static文件夹下
        if 'resources' in r_path:
            print 'store resources'
            print r_path
            dir_id = (r_path.split('/')[-1])[3:]

            resourceresolution = '0x0'
            #if rrrtype == "png" or rrrtype == "jpg" or rrrtype == "jpeg":
            if rrrtype in PIC_TYPE:
                print "----name-----",rrrname
                im = Image.open(os.path.join(r_path, rrrname))
                print 'Image Info'
                print im.format, im.size, im.info
                resourceresolution = im.size
                tupiansuolietu(os.path.join(r_path, rrrname))
            #elif rrrtype == "swf" or rrrtype == "mp4" or rrrtype == "flv":
            elif rrrtype in VIDEO_TYPE:
                try:
                    get_thumbnail(rrrname, r_path+os.sep, rrrtype)
                except:
                    pass
            mg_new_resourcemanage_oneadd(rrrname, rrrtype, rrrsize, resourceresolution, upload_time, str(dir_id))
        #节目组成素材上传后保存到static下的对应节目文件夹下
        #elif r_path != OTHDIR:
        else:
            print 'store program resource'
            if rrrtype in PIC_TYPE:
            #if rrrtype == "png" or rrrtype == "jpg" or rrrtype == "jpeg":
                #print r_path
                #print "----name-----", rrrname
                tupiansuolietu(os.path.join(r_path, rrrname))
            #if rrrtype == "swf" or rrrtype == "mp4" or rrrtype == "flv":
            elif rrrtype in VIDEO_TYPE:
                if lite_platform_check() == 'l':
                    get_thumbnail(rrrname, r_path + os.sep,rrrtype)
                else:
                    get_thumbnail(rrrname.decode('utf-8').encode('cp936'), r_path + os.sep,rrrtype)
                #print "................-----...--.--.----.--.--."
    except:
        pass


def tupiansuolietu(name_path):
    #size = 600,600
    size = 1920, 1920
    print size
    #nameflag = "D:\\ids\\ids_server_1.1\\static\\"+name
    nameflag = name_path
    #print nameflag
    #print "tupiansuolietu01"
    im = Image.open(nameflag)
    print "tupiansuolietu02"
    #im.thumbnail(size)
    print "tupiansuolietu03"
    quality_val = 60
    im.save(nameflag+".jpg", quality=quality_val)
    #im.save(nameflag+".jpg")
    print "tupiansuolietu04"


def ayu(username, todosth, userip):
#dic1 = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07",
#"Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    d = datetime.now()
    newtime = d.strftime("%Y/%m/%d/%H/%M/%S")
    ctime = time.ctime()
    intnewtime = int(newtime[0:4])*600 + int(newtime[5:7])*40 + int(newtime[8:10])
    #print intnewtime
    return mg_ayu(username,todosth,ctime,intnewtime, userip)


class ids_othersth():
    """
    """
    def homemessage(self, system):
        """
        首页系统消息
        """

        dic = mg_homemessage(system)

        return dic

    def homeremaintime(self, system):
        """
        首页系统授权时间
        """

        dic =mg_homeremaintime(system)
        return dic


    def ids_resource_move(self, resourcepath, name, id, idtype):
        print 'ids_resource_move :  ', resourcepath
        des_path = DIR+ idtype + str(id)
        print des_path
        if not os.path.isdir(des_path):
            os.makedirs(des_path)
        try:
            if idtype == "program":
                #print 'remove to program'
                #print os.path.join(DIR, resourcepath)
                #print DIR+"program"+str(id)+os.sep+name
                shutil.copy(os.path.join(DIR, resourcepath), DIR+"program"+str(id)+os.sep+name)
                shutil.copy(os.path.join(DIR, resourcepath+'.jpg'), DIR+"program"+str(id)+os.sep+name+'.jpg')
                return 1
            elif idtype == "model":
                shutil.copy(os.path.join(DIR, resourcepath), DIR+"model"+str(id)+os.sep+name)
                shutil.copy(os.path.join(DIR, resourcepath+'.jpg'), DIR+"model"+str(id)+os.sep+name+'.jpg')
                return 1
            else:
                return -1
        except:
            return -1


    def badapple(self,mac,ip,frompage,topage):
        dic1 = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07",
                "Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
        timetemp = ctime()
        newtime = timetemp[20:]+'/'+dic1[timetemp[4:7]]+'/'+timetemp[8:10]
        intnewtime = int(newtime[0:4])*600 + int(newtime[5:7])*40 + int(newtime[8:])

        mg_badapple(mac,ip,frompage,topage,newtime,intnewtime)
        mg_badappleall(newtime,intnewtime)
        mg_badappleallest(newtime,intnewtime)


    def yamasaki(self,mac,ip,todo):
        d = datetime.now()
        #newtime = d.strftime("%Y/%m/%d/%H/%M/%S")
        ctime = time.ctime()
        #print ctime
        #intnewtime = int(time.time())
        newtime = d.strftime("%Y/%m/%d/%H/%M/%S")
        intnewtime = int(newtime[0:4])*600 + int(newtime[5:7])*40 + int(newtime[8:10])
        #print intnewtime
        mg_yamasaki(mac,ip,todo,ctime,intnewtime)


    def longgingtemptemp(self,mac,ip,todo):

        mg_longgingtemptemp(mac,todo)
    #a = ids_othersth()
#a.ids_resource_move("1.jpg",23,"modal")


class CollectServer(BaseRequestHandler):
    def handle(self):
        #print 2
        data = self.request.recv(1024)
        #print data
        name = data[4:]
        #print "list1",data
        #print "$$$$$$$$$$$$$$$    5"
        data = self.request.recv(1024)

        size = int(data[4:])
        smin = 0
        realsize = 0
        #print "list2",data
        #print size

        self.request.send(str(0))

        global DIR
        #print DIR,"1st"

        if lite_platform_check() == 'l':
            newdir = DIR +os.sep + name
        else:
            newdir = DIR +os.sep + name.decode('utf-8').encode('cp936')
        ##newdir = DIR +os.sep + name
        #print newdir,"2nd"
        f = open(newdir,'wb')

        try:
            #print 4
            while size > 0:
                #print 5

                data = self.request.recv(1024)
                #self.request.send(str(smax-size))
                f.write(data)
                size -= len(data)
                smin += len(data)
                realsize += len(data)

                #print 'size ',size
                #print 'realsize ',realsize
                #realsize += len(data)
                if size > 0:
                    if smin% 10485760 == 0 :

                        self.request.sendall("size" +str(realsize))
                        #print smin



                    pass
                else:
                    pass
                    #print 8
                    #print realsize
                    #self.request.sendall(str(realsize))

            #############################
            f.close()
            #############################
            try :
                #print 33333333333333333333333333333333
                if True:#realsize == size:
                    #print 100
                    rrrname = name
                    rrrtype = name[-3:]
                    rrrsize = realsize
                    rrrtime = ctime()
                    #print 200
                    if rrrtype == "png":
                        #rrrf = Image.open("newdir")
                        #rrrtion = rrrf.size
                        rrrtion = "0,0"
                    else:
                        rrrtion ="0,0"
                        #print 300
                    resourceid = mg_resourcemanage_countfind()
                    #print 5000
                    #global DIR
                    if resourceid > 0  and DIR == OTHDIR:
                        mg_resourcecountup(resourceid+1)
                        #print 600
                        mg_resourcemanage_oneadd(resourceid,rrrname,rrrtype,rrrtion,rrrsize,rrrtime)

                        if rrrtype == "png" or rrrtype == "jpg":
                            #print "----name-----",rrrname
                            tupiansuolietu(rrrname)
                            #print "-----namehoushizaideweizhiitisafinctic---------"
                        elif rrrtype == "swf":
                            try:
                                get_thumbnail(rrrname,DIR,rrrtype)
                            except:
                                pass

                        else:
                            pass
                    elif resourceid > 0 and DIR != OTHDIR:
                        if rrrtype == "swf" or rrrtype == "mp4" or rrrtype == "flv":
                            try:
                                get_thumbnail(rrrname, DIR + os.sep,rrrtype)
                            except:
                                try:
                                    get_thumbnail(rrrname.decode('utf-8').encode('cp936'),DIR + os.sep,rrrtype)
                                except:
                                    pass
                                    #print "................-----...--.--.----.--.--."

                                    #print 700
            except:
                #print 400
                pass
                #self.request.sendall(str(realsize))
        except:
            pass
            #print 11

        finally:
            self.request.sendall(str(realsize))
            #print "$$$$$$$$$$$$$$$    6"
            #print 7
            #global SHOTDOWNFLAG
            #SHOTDOWNFLAG = 1
            #DIR = "D:\\ids\\ids_server_1.1\\static\\"
            ##DIR = "/ids/ids_server_1.1/static/"
            #print SHOTDOWNFLAG,"3th"
            #f.close()
            return 0

class othersth_overship_Server(BaseRequestHandler):
    def handle(self):
        #print 2
        data = self.request.recv(1024)
        #print data
        id = data.split('-')[1]
        idtype = data.split('-')[2]
        #print "get the resource info ", id, idtype
        self.request.send('ok')

        global DIR
        #print "4th",DIR
        if id == "" and idtype == "":
            DIR = OTHDIR
            #print "260", DIR, OTHDIR
        else:
            DIR = OTHDIR
            #print "264", DIR, OTHDIR

            DIR = DIR + str(idtype) + str(id)
            #print "267", DIR
            #print "5th",DIR

"""
def resourceHTTPServer():
    print "before aging"
    server = SocketServer.TCPServer((TCPHOST, TCPPORT), CollectServer)
    print "aging"
    server.serve_forever()

def othersth_overship():
    print "before ordering"
    server = SocketServer.TCPServer((TCPHOST, 2003), othersth_overship_Server)
    print "odering"
    server.serve_forever()
"""





#------------------------------------------------------------------------
#临时解决方案
#
#------------------------------------------------------------------------




















#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------






def stringtolist_maclist(oldstringlist):
    """
    类型转化，将str转化为mac列表
    """
    ledgh = len(oldstringlist)
    lit = []
    v = 2
    while v < ledgh :
        print oldstringlist[v:v+16]
        lit.append(oldstringlist[v:v+16])
        v += 20

    return lit


def stringtolist_updowntime(oldstringlist):
    """
    类型转化，将str转化为time列表
    """
    ledgh = len(oldstringlist)
    #print ledgh
    lit = []
    v = 3
    while v < ledgh:
        lit.append(oldstringlist[v:v+11])
        v += 16

    return lit








import base64
def zhongduanjtu(picname):



    a = open(CPSSDIR + picname,"rb")
    data = a.read()
    a.close()
    os.remove(CPSSDIR + picname)


    return {"data":base64.b64encode(data)}



if __name__ == '__main__':
    resourcename = 'pic.JPG'
    resourcesize = 123
    resourcepath = '/hh/a'
    resource_http_add(resourcename, resourcesize, resourcepath)


