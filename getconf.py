import os
import ConfigParser
import codecs

def getconfig(section, item):
    path = os.path.abspath(os.path.pardir)
    if os.path.isfile(os.path.join(path, "server/config.conf")):
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.join(path, "server/config.conf"))
        conf_item = cf.get(section, item)
        return conf_item
    else:
        print "config file error"
        return 0

def get_mail_config(section, item):
    path = os.getcwd()
    if os.path.isfile("mail_config.conf"):
        cf = ConfigParser.ConfigParser()
        cf.read("mail_config.conf")
        #cf.read(codecs.open("mail_config.conf", "r", "utf-8"))
        conf_item = cf.get(section, item)
        return conf_item
    else:
        print "mail config file error"
        return 0

if __name__ == "__main__":
    print getconfig('ip_address', 'server_address')
