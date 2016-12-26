#uwsgi --http job.icybee.cn:8000 --chdir /alidata/workspace/icyjob/icyjob --module django_wsgi
uwsgi --xml icyjob_socket.xml 
