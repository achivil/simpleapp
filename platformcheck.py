import platform
import os

from getconf import *

def platform_check():
    system_check = platform.architecture()

    if 'windowspe' in system_check[1].lower():
        DIR = getconfig('dir', 'win_dir')
        CPSSDIR = DIR + 'temp' + r'\\'
        #DIR = "D:\\ids\\server\\static\\"
        #CPSSDIR = "D:\\ids\\server\\static\\temp\\"
    else:
        DIR = getconfig('dir', 'linux_dir')
        if DIR == 'None':
            DIR = os.path.join(os.getcwd(), "static/")
        CPSSDIR =  DIR + "temp/"
    return DIR, CPSSDIR
    #SERVERHOST = "192.168.1.26"

def lite_platform_check():
    system_check = platform.architecture()

    if 'windowspe' in system_check[1].lower():
        return "w"
    else:
        return "l"

if __name__ == "__main__":
    DIR, CPSSDIR = platform_check()
    print DIR, CPSSDIR
    r = lite_platform_check()
    print r

