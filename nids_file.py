#-*-coding: utf-8 -*-
#按块读写文件，提供给传输模块使用
#实现断点续传等功能

import os
import hashlib
import shutil

from othersth import *

#temp_rec_file = os.path.join(os.getcwd(), 'tmpfile.tmp')
filepath = os.path.join(os.getcwd(), 'static')
#temp_rec_file = os.path.join(filepath, 'tmpfile.tmp')

#建立节目文件夹
def create_programe(programname=None):
    if programname != '""':
        if 'program' in programname:
            #print 'create program: ', programname
            pro_path = os.path.join(filepath, programname)
        elif 'modal' in programname:
            #print 'create modal: ', programname
            pro_path = os.path.join(filepath, programname)

        #pro_path = os.path.join(filepath, 'program' + programname)
        if not os.path.isdir(pro_path):
            os.makedirs(pro_path)
    else:
        pro_path = filepath + '/'
        #素材文件夹要和DIR保持一致，加上尾部的斜杠
    return pro_path

def check_file_right(tmp=0, f_md5=0):
    if not os.path.isfile(tmp):
        return 1
    with open(tmp, 'rb') as f:
        data = f.read()
        temp_md5 = (hashlib.md5(data)).hexdigest()
    #print temp_md5, "__++++++++++++__", f_md5
    if str(temp_md5) == str(f_md5):
        return 1
    else:
        return 1

def find_end(filename, chuck_len):
    #查找文件结尾
    #print "find file end start"
    if os.path.isfile(filename):
        chucks = int(os.path.getsize(filename)) // int(chuck_len)
        chuck_pos = chucks
    else:
        chuck_pos = -1
    return int(chuck_pos)

#按接收到的分块信息写文件
def write_file(data, filename, resource_path, pos, datalen, filelen, md5):
    mess = {'error': "0"}
    tmp_file_name = 'tmp_' + filename
    temp_rec_file = os.path.join(resource_path, tmp_file_name)
    #print 'temp_rec_file: ', temp_rec_file
    #print 'resource_path', resource_path
    start = pos
    #开始位置是参数指定的文件结尾
    #当开始位置加上data长度小于文件大小时，继续写文件
    if  (start + datalen) < int(filelen):
        if not check_file_right(temp_rec_file, md5):
            mess = {'error': "-2"}
            return mess
        if int(start) == 0:
            #创建新文件
            #
            with open(temp_rec_file, 'wb') as f:
                f.write(data)
        else:
            #追加文件
            #
            with open(temp_rec_file, 'ab') as f:
                f.seek(int(start))
                f.write(data)
        mess = {'error': "-1"}
        print "!!!###^^^^^^^^^^^^^^^^^^   save chucks done"
    else:
        with open(temp_rec_file, 'ab') as f:
            f.seek(int(start))
            f.write(data)
        #os.remove(programpath)
        if not check_file_right(temp_rec_file, md5):
            mess = {'error': "-2"}
            return mess
        print 'start save'
        #修改为移动文件
        #print temp_rec_file
        #print os.path.join(resource_path, filename)
        shutil.move(temp_rec_file, os.path.join(resource_path, filename))
        print "save done"
        mess = {'error': "-3"}
        resource_http_add(filename, filelen, resource_path)
        #os.remove(tmp_rec_file)
    return mess

def read_file(filename, start):
    """
    #目前server暂时没有使用
    #读文件时需要文件名和开始读取的位置
    pos = int(start)
    filelength = int(os.path.getsize(os.path.join(filepath, filename)))
    #print 'pos = ', pos
    #print 'filelength = ', filelength
    if pos >= find_end(filename):
        return "position is not valid"
    if pos == 0:
        #print "start read at:", pos
        with open(os.path.join(filepath, filename), 'rb') as f:
            data = f.read(data_len)
    else:
        #print "start read at:", pos
        with open(os.path.join(filepath, filename), 'rb') as f:
            f.seek(pos)
            data = f.read(data_len)
    pos = int(pos)
    #print pos, 'send over.'
    return data
    """

if __name__ == "__main__":
    find_end('/Users/achivil/work/NiDS/idsmanage/src/server/static/jpg.jpg', 1024)
