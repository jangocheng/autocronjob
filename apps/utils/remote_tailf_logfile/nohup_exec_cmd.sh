#!/bin/bash
# exec tailf_logfile.py


cd /tmp
argv7=echo $7|sed s/[[:space:]]//g

pids=`ps axu | grep  tailf_logfile.py|grep $5 | grep -v grep |awk '{print $2}'`

if [ "$pids" == "" ];
then
   if [ -z "$argv7" ];
   then
      nohup python /opt/autocronjob/apps/utils/remote_tailf_logfile/tailf_logfile.py $1 $2 $3 $4 $5 $6 "" &
   else
      nohup python /opt/autocronjob/apps/utils/remote_tailf_logfile/tailf_logfile.py $1 $2 $3 $4 $5 $6 $7 &
   fi
else
   echo "tailf_logfile.py is running"
fi
