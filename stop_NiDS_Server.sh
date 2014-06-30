#! /bin/sh

nginxpid=$(ps ax | grep  'nginx' | grep -v 'grep' | grep 'master'|awk {'split($0, b, " "); print b[1]'})
if test -z "$nginxpid"
then
    echo "No Nginx Process"
else
    echo "Nginx Restart"
    echo $nginxpid
fi

graudpid=$(ps ax | grep  'python ../host/graud' | grep -v 'grep' | awk {'split($0, b, " "); print b[1]'})
if test -z "$graudpid"
then
    echo "No graud Process"
else
    echo $graudpid
    echo "Graud Restart"
    kill $graudpid
fi

rupid=$(ps ax | grep  'python resourceupload.py' | grep -v 'grep' | awk {'split($0, b, " "); print b[1]'})
if test -z "$rupid"
then
    echo "No resourceupload Process"
else
    echo $rupid
    echo "Resourceupload  Restart"
    kill $rupid
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
fi

echo "Stop NiDS Server"
