# coding -*- utf-8 -*-
"""
"""
import os
import re
import shutil
from subprocess import Popen, PIPE

from platformcheck import platform_check

DIR, CPSSDIR = platform_check()

def count_time():
    pass

def get_thumbnail_MP4(path, inputfile, thumbnailname, time):
    """
    Get a thumbnail of MP4 file by call ffmpeg.
    """
    inputfile = str(path)  + inputfile
    thumbnailname = str(path)  + thumbnailname
    cmd = 'ffmpeg -i %s -ss %02d:%02d:%02d -f image2 -vframes 1 %s -loglevel quiet -y' % (inputfile, time[0], time[1], time[2], thumbnailname)
    #print cmd
    output  = Popen(cmd, shell=True)
    output.wait()
    if os.path.isfile(thumbnailname):
        #print "Created thumbnail"
        return thumbnailname
    else:
        #shutil.copyfile(DIR + "jpg.jpg",thumbnailname)
        shutil.copyfile(DIR + "video.jpg",thumbnailname)
        return thumbnailname


def get_thumbnail_swf(path, inputfile, thumbnailname, time):
    """
    Get a thumbnail of swf file by call swftools.
    """
    inputfile = str(path)  + inputfile
    thumbnailname = str(path)  + thumbnailname

    try:
        cmd_res = {}
        cmd = "swfextract %s" % inputfile
        res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        cmd_res['out'] = res.stdout.readlines()
        cmd_res['err'] = res.stderr.readlines()
        res.wait()
        jnum = 0
        pnum = 0

        for r in cmd_res['out']:
            if "[-j]" in r:
                #print r
                jnum = int((r.split(',')[0].split(':'))[1][7:])
                #print "jnum ", jnum
                #jnum = int(r.split(':')[1][7])
                if "JPEG" in r or "JPEGs" in r:
                    jinfo = {'type': 'jpeg', 'value': jnum}
                else:
                    jinfo = {'type': 'j', 'value': jnum}
            elif "[-p]" in r:
                #print r
                pnum = int((r.split(',')[0].split(':'))[1][7:])
                #print "pnum ", pnum
                #pnum = int(r.split(':')[1][7])
                pinfo = {'type': 'p', 'value': pnum}

        if jnum > 0 and pnum > 0:
            #print "jnumber and pnumber", jnum, pnum
            if jnum < pnum:
                swfinfo = jinfo
            else:
                swfinfo = pinfo
        elif jnum == 0 and pnum == 0:
            #print "f"
            swfinfo = {'type': 'f', 'value': 0}
        elif jnum == 0:
            #print "pinfo"
            swfinfo = pinfo
        elif pnum == 0:
            #print "jinfo"
            swfinfo = jinfo

        #print swfinfo
        #print "swfinfo['type']  ", swfinfo['type']
        #print "swfinfo['value']  ", swfinfo['value']
    except:
        pass
    try:
        if swfinfo['type'] == 'jpeg':
            cmd = "swfextract %s -j %d -o %s.jpeg" % (inputfile, swfinfo['value'], inputfile)
            #print cmd
            res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
            res.wait()
            cmd = "ffmpeg -i %s.jpeg %s -loglevel quiet -y" % (inputfile, thumbnailname)
            #print cmd
            newres = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
            res.wait()
        elif swfinfo['type'] == 'j':
            cmd = "swfextract %s -j %d -o %s.jpg" % (inputfile, swfinfo['value'], thumbnailname)
            #print cmd
            res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
            res.wait()
        elif swfinfo['type'] == 'p':
            cmd = "swfextract %s -p %d -o %s.png" % (inputfile, swfinfo['value'], inputfile)
            #print cmd
            res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
            res.wait()
            cmd = "ffmpeg -i %s.png %s -loglevel quiet -y" % (inputfile, thumbnailname)
            #print cmd
            newres = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
            res.wait()
        elif swfinfo['type'] == 'f':
            cmd = 'ffmpeg -i %s -ss %02d:%02d:%02d -f image2 -vframes 1 %s -loglevel quiet -y' % (inputfile, time[0], time[1], time[2], thumbnailname)
            #print cmd
            output = Popen(cmd, shell=True)
            output.wait()
        else:
            pass
    except:
        print 'creat thumbnail error'

    if os.path.isfile(thumbnailname):
        #print "Created thumbnail"
        return thumbnailname
    else:
        #shutil.copyfile(DIR + "jpg.jpg", thumbnailname)
        shutil.copyfile(DIR + "swf.jpg", thumbnailname)
        return thumbnailname



def get_thumbnail(filename,newdir,newtype):
    """
    Process the files' name and paths. Check the files' format.
    Now get_thumbnail_swf and get_thumbnail_MP4 are same function.
    Maybe get_thumbnail_swf will be change for reasons.
    """

    try:
        size = os.stat(newdir+filename).st_size
    except:
        size = 0
        #return error_file

    if size > 100000000:
        time = [0, 0, 5]
    elif size < 5000:
        time = [0, 0, 2]
    else:
        time = [0, 0, 3]

    if newtype == 'mp4':
        #print "This is a mp4 file."
        pic = get_thumbnail_MP4(newdir, filename, filename+".jpg", time)
    elif newtype == 'swf':
        #print "This is a swf file."
        pic = get_thumbnail_swf(newdir, filename, filename+".jpg", time)
    elif newtype == 'flv':
        pic = get_thumbnail_MP4(newdir, filename, filename+".jpg", time)
    else:
        #print "This format is not support now."
        #pic = get_thumbnail_swf(newdir, filename, filename+".jpg", time)
        pass
    if pic == 'NULL':
        #return error_file
        pass
    return pic


