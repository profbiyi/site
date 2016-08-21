user               = None
group              = None
bind               = 'unix:/var/local/agcs/run/gunicorn.sock'
errorlog           = '/var/local/agcs/log/gunicorn/error.log'
accesslog          = '/var/local/agcs/log/gunicorn/access.log'
pidfile            = '/var/local/agcs/run/gunicorn.pid'
worker_tmp_dir     = '/var/local/agcs/tmp/gunicorn'
working_dir        = '/home/django/site/site'
chdir              = working_dir
loglevel           = 'info'
backlog            = 2048
worker_connections = 1000
timeout            = 30
keepalive          = 2
umask              = 0
debug              = False
spew               = False
daemon             = False
proc_name          = None
tmp_upload_dir     = None


try:
    from multiprocessing import cpu_count
    workers = 2 * cpu_count() + 1
    del(cpu_count)
except NotImplementedError:
    workers = 3

try:
    import sys
    sys.path.index(working_dir)
except ValueError:
    sys.path.insert(0, working_dir)
finally:
    del(sys)

try:
    from importlib import import_module
    from os import getenv
    debug = import_module(getenv('DJANGO_SETTINGS_MODULE')).DEBUG
except AttributeError:
    debug = debug
finally:
    del(getenv, import_module)

loglevel = debug and 'debug' or 'info'


def on_starting(server):
    from os import (
        mkdir, chmod, stat,
        access, F_OK
    )

    global worker_tmp_dir

    try:
        access(worker_tmp_dir, F_OK) or (
            mkdir(worker_tmp_dir)
        )
        stat(worker_tmp_dir).st_mode == 0o46775 or (
            chmod(worker_tmp_dir, 0o46775)
        )
    except:
        worker_tmp_dir = None
        server.log.info("Failed to create %s. "
            "Using fallback." % worker_tmp_dir
        )

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    import threading, sys, traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def post_fork(server, worker):
    pass
def pre_fork(server, worker):
    pass
def pre_exec(server):
    server.log.info("Forked child, re-executing.")
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")
def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")

