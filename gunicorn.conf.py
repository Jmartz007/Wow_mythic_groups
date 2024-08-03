bind = "0.0.0.0:443"
workers = 2
timeout = 60
certfile = '/etc/jmartzservegame/jmartz_servegame_com-chain.pem'
keyfile = '/etc/jmartzservegame/myserver.key'
accesslog = "-"
access_log_format = '%(h)s %({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'