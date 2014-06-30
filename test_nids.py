# -*- coding: utf-8 -*-
############################################################################
#
#
#
############################################################################

import traceback
from time import sleep
from bson import ObjectId

from flask  import Flask, request, session, g, redirect, url_for, \
    render_template, make_response, flash

from user import *
from getconf import getconfig, get_mail_config
from common.celery_app import add

from nids_file import *
from advertisement.advertisement import ad
from resource.resource_manager import new_resource_handler
from http_upload.http_upload import resource_upload
from datetime import timedelta

SECRET_KEY = 'development monkey'

app = Flask(__name__)
app.config.from_object(__name__)


# app.permanent_session_lifetime = timedelta(minutes=180)
app.register_blueprint(ad, url_prefix='/advertisement')
app.register_blueprint(new_resource_handler, url_prefix='/newresource')

DIR, CPSSDIR = platform_check()

SERVERHOST = getconfig('ip_address', 'server_address')
SERVERPORT = int(getconfig('ip_address', 'server_port'))
DBHOST = getconfig('database', 'server_address')
database = getconfig('database', 'database_name')

##############################################
# 开发 测试用数据库连接方式
mg_host = DBHOST

print 'Using Database : %s   %s' % (mg_host, database)
client = pymongo.MongoClient(mg_host)
db = client[database]
##############################################


LOGINFLAG = 0  # 判断标志，用于返回cookies        这里的全局变量是安全的

@app.before_request
def before_request():
    # g.WEBFLAG 判断标志，网页简易测试功能
    if 'AdobeAIR' in request.headers['User-Agent']:
        g.WEBFLAG = 0
    else:
        g.WEBFLAG = 1
    g.db_name = database
    g.client = client
    g.db = db

@app.after_request
def after_request(response):
    """
    只有在登录成功后触发
    在response中添加cookie
    """
    #####################################
    if g.WEBFLAG == 1:
        return response
    #####################################
    global  LOGINFLAG
    if LOGINFLAG == 1:
        LOGINFLAG = 0
        resunt = app.process_response(response)
        temp = json.dumps({"body":str(response.data) , "Cookies":resunt.headers['Set-Cookie']})
        response.data = str(temp)
    return response

@app.route('/logout', methods=['GET'])
def ol_logout():
    '''
    正常退出
    '''
    try:
        if 'username' in session:
            session.pop('username', None)
            session.pop('role', None)
            session.pop('system', None)
            session.clear()
    #************************************
            if g.WEBFLAG == 1:
                return redirect('/')
            else:
                return make_response(json.dumps({"error":1}))
    #************************************
        else:
    #************************************
            if g.WEBFLAG == 1:
                return redirect('/')
            else:
                return make_response(json.dumps({"error":-1}))
    #************************************
    except:
    #************************************
        traceback.print_exc()
        if g.WEBFLAG == 1:
            return redirect('/')
        else:
            return make_response(json.dumps({"error":-5}))
    #************************************


@app.route('/', methods=['GET', 'POST'])
def ol_login():
    '''
    登录页面
    '''
    if 'username' in session:
    #************************************
        if g.WEBFLAG == 0:
            user_information = {'error':0}
            return make_response(json.dumps(user_information))
        else:
            return render_template('users.html', user=session)
    #************************************
    elif request.method == "GET":
        # print "get method!"
        return render_template('test_nids_login.html')

    elif request.method == 'POST':
        # print request
        func1 = ids_user()
        user_information = func1.user_login(request.form['username'], request.form['password'])

        if user_information['error'] == 1:
            session['username'] = user_information['username']
            session['role'] = user_information['userrole']
            # session.permanent = True
            if not user_information['system']:
                session['system'] = 'NSE'
            else:
                session['system'] = user_information['system']
                # session['system'] = user_information['system'].encode('utf-8')
                # mongodb内存贮使用utf-8字符，有可能用到中文的地方都使用用utf-8进行编码
                # 注意发布和测试版本所以的打印信息都要去掉，防止出现中文
                # 这里的system文本信息来自于数据库查询结果，已经是utf-8编码了
            func1.user_changelastlogintime(user_information['username'], user_information['thislogintime'])

            global  LOGINFLAG
            LOGINFLAG = 1

        else:
            if g.WEBFLAG == 1:
                flash('You were failed')
                return render_template('test_nids_login.html')
            ################################################
        try:
            userip = request.environ['REMOTE_ADDR']
            # print userip
            ayu(session["username"], u"用户登录", userip)
        except:
            pass
            ###############################################
        if g.WEBFLAG == 1:
            # print user_information
            return render_template('users.html', user=session)
        else:
            return make_response(json.dumps(user_information))

@app.route('/user', methods=['GET'])
def ol_user():
    '''
    用户管理页面
    '''
    if 'username' not in session:
        user_information = {'error':0}

    else:
        func1 = ids_user()
        if func1.user_showalluser(session['system']) == -1:
            user_information = {'error':-1}
        else:
            user_information = func1.user_showalluser(session['system'])

    return make_response(json.dumps(user_information))

@app.route('/password', methods=['GET', 'POST'])
def ol_password():
    '''
    用户修改密码
    '''

    if request.method == 'POST':
        if 'username' not in session:
            user_information = {'error':0}
        elif request.method == 'POST':
            func1 = ids_user()
            user_information = {'error':func1.user_changepassword(request.form['username'],
                request.form['oldpass'], request.form['newpass'])}
        else:
            user_information = {'error':-5}
            ################################################
        return make_response(json.dumps(user_information))


@app.route('/user/add/checkname', methods=['GET', 'POST'])
def ol_user_checkname():
    '''
    检测新建用户名是否重复
    '''
    if request.method == 'POST':
        func1 = ids_user()
        user_information = { 'error':func1.user_namecheck(request.form['username']) }
    else:
        user_information = {'error':-5}
    return make_response(json.dumps(user_information))

@app.route('/user/add', methods=['GET', 'POST'])
def ol_user_add():
    '''
    添加用户
    '''

    if request.method == 'POST':
        if 'role' not in session:
            user_information = { 'error':-5}

        else:
            if int(session['role']) / 2 % 2 == 1 or int(session['role']) % 2 == 1 or int(session['role'] / 32) % 2 == 1:
                func1 = ids_user()
                errornote = func1.user_nameadd(request.form['username'], request.form['password'],
                    request.form['userrole'], request.form['naturalname'], request.form['userremark'], session['system'])
                user_information = {'error':errornote}
            else:
                user_information = {'error':-1}
                ################################################
        return make_response(json.dumps(user_information))

@app.route('/user/<id>/password', methods=['GET', 'POST'])
def ol_user_resetpass(id):
    '''
    重置密码
    '''
    if request.method == 'POST':
        if 'role' not in session:
            user_information = { 'error':-5}
        else:
            if int(session['role']) / 2 % 2 == 1 or int(session['role']) % 2 == 1 or int(session['role'] / 32) % 2 == 1:
                func2 = ids_user()
                op = func2.user_name(int(id))
                func1 = ids_user()
                user_information = {'error':func1.user_resetpass(request.form['username'], request.form['newpass'])}
            else:
                user_information = {'error':-1}
                ################################################
        return make_response(json.dumps(user_information))

@app.route('/user/<id>/role', methods=['GET', 'POST'])
def ol_user_resetrole(id):
    '''
    重置用户角色
    '''
    if request.method == 'POST':
        if 'role' not in session:
            user_information = { 'error':-5}
        else:
            if int(session['role']) / 2 % 2 == 1 or int(session['role']) % 2 == 1 or int(session['role'] / 32) % 2 == 1:
                func2 = ids_user()
                op = func2.user_name(int(id))
                func1 = ids_user()
                user_information = {'error':func1.user_resetrole(request.form['username'], request.form['userrole'],
                    request.form['userremark'])}
            else:
                user_information = {'error':-1}
            ###############################################
        return make_response(json.dumps(user_information))

@app.route('/user/<id>/del', methods=['GET', 'POST'])
def ol_user_del(id):
    '''
    删除用户
    '''
    if request.method == 'POST':
        if 'role' not in session:
            user_information = { 'error':-5}
        else:
            if int(session['role']) / 2 % 2 == 1or int(session['role']) % 2 == 1  or int(session['role'] / 32) % 2 == 1:
                from program.mg_program import ProgramDB

                func2 = ids_user()
                op = func2.user_name(int(id))
                func1 = ids_user()
                user_information = {'error': func1.user_namedel(request.form['username'])}
            else:
                user_information = {'error':-1}
            ###############################################
        return make_response(json.dumps(user_information))
#--------------------------------------------------------------------------------------------
#########################################################################
# send mail with photographs
#########################################################################
from send_mail import sendmail, create_attachment

@app.route('/new_send_mail', methods=['GET', 'POST', 'PUT'])
def send_mail():
    from common.celery_app import send_comment_mail
    error_info = 'error init'
    if request.method == 'GET':
        try:
            # print receivers
            # print "info ready"
            para_dic = {}
            # para_dic.setdefault('data', request.form['uploadFile'])
            # para_dic.setdefault('receivers', request.form['address'])
            receivers = TEST_ADDRESS
            data = base64.b64encode("000")
            para_dic.setdefault('data', data)
            para_dic.setdefault('receivers', receivers)
            para_dic.setdefault('sender', get_mail_config('email_info', 'sender'))
            para_dic.setdefault('smtpaddr', get_mail_config('email_info', 'smtpserver'))
            para_dic.setdefault('username', get_mail_config('email_info', 'username'))
            para_dic.setdefault('passwd', get_mail_config('email_info', 'passwd'))
            para_dic.setdefault('subject', get_mail_config('email_info', 'subject'))
            para_dic.setdefault('text', get_mail_config('email_info', 'text'))
            para_dic.setdefault('photoname', get_mail_config('email_info', 'photoname'))
        except:
            print 'parameters are wrong.'
            return make_response("1")

        try:
            print "before send photo."
            # 后台执行邮件发送操作 使用celery+Redis
            send_comment_mail.delay(para_dic)
            return make_response("0")
        except:
            errorinfo = 1
            print "send photo failed."
            return make_response("1")
    else:
        error_info = 'request methods wrong'
    return error_info

#############################
#
# 服务启动
#
#############################

def start():
    app.run(host=SERVERHOST, port=SERVERPORT, debug=False)

if __name__ == '__main__':
    start()
