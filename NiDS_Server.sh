#! /bin/sh

nginxpid=$(ps ax | grep  'nginx' | grep -v 'grep' | grep 'master'|awk {'split($0, b, " "); print b[1]'})
if test -z "$nginxpid"
then
    echo "No Nginx Process"
    /usr/local/nginx/nginx
else
    echo "Nginx Restart"
    echo $nginxpid
    /usr/local/nginx/nginx -s reload
    #kill $pid
    #不同机器修改nginx地址
fi

graudpid=$(ps ax | grep  'python ../host/graud' | grep -v 'grep' | awk {'split($0, b, " "); print b[1]'})
if test -z "$graudpid"
then
    echo "No graud Process"
    sleep 2
    python ../host/graud.py &
else
    echo $graudpid
    echo "Graud Restart"
    kill $graudpid
    sleep 2
    python ../host/graud.py
fi

rupid=$(ps ax | grep  'python resourceupload.py' | grep -v 'grep' | awk {'split($0, b, " "); print b[1]'})
if test -z "$rupid"
then
    echo "No resourceupload Process"
<<<<<<< HEAD
    python resourceupload.py
||||||| merged common ancestors
    sudo python resourceupload.py &
=======
    sleep2
    python resourceupload.py &
>>>>>>> e58851b5cb532967012ecfd9a175957ea9db802e
else
    echo $rupid
    echo "Resourceupload  Restart"
    kill $rupid
    sleep 2
<<<<<<< HEAD
    python resourceupload.py
||||||| merged common ancestors
    sudo python resourceupload.py &
=======
    python resourceupload.py &
>>>>>>> e58851b5cb532967012ecfd9a175957ea9db802e
fi

#python ../host/graud.py > /dev/null 2>&1 &
#python resourceupload.py > /dev/null 2>&1 &
uwsgipid=$(ps ax | grep  'uwsgi -x' | grep -v 'grep' | awk {'split($0, b, " "); print b[1]'})
if test -z "$uwsgipid"
then
    echo "No uwsgi Process"
else
    echo $uwsgipid
    echo "Uwsgi Restart"
    kill $uwsgipid
    sleep 3
fi

uwsgi -x flask.xml --ignore-sigpipe --ignore-write-errors
