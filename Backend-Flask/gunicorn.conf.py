bind = "0.0.0.0:5005"
workers = 2
timeout = 60
accesslog = "-"
access_log_format = '%(h)s %({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'