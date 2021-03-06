# coding:utf-8

workers = 4

threads = 4

bind = '0.0.0.0:5000'

worker_class = 'eventlet'  # 'gevent'

worker_connections = 2000

pidfile = 'gunicorn.pid'

accesslog = './logs/gunicorn_acess.log'
errorlog = './logs/gunicorn_error.log'

loglevel = 'info'

reload = True
