import os
import sys
from importlib import import_module


bind               = 'unix:%s' % os.path.join(os.environ['DJANGOPROJECT_DATA_DIR'], 'run', 'gunicorn.sock')
pidfile            = os.path.join(os.environ['DJANGOPROJECT_DATA_DIR'], 'run', 'gunicorn.pid')
worker_tmp_dir     = os.path.join(os.environ['DJANGOPROJECT_DATA_DIR'], 'tmp', 'gunicorn')
errorlog           = os.path.join(os.environ['DJANGOPROJECT_DATA_DIR'], 'log', 'gunicorn', 'error.log')
accesslog          = os.path.join(os.environ['DJANGOPROJECT_DATA_DIR'], 'log', 'gunicorn', 'access.log')
working_dir        = os.path.join(os.path.expanduser('~django'), 'site', 'site')
chdir              = working_dir
user               = None
group              = None
capture_output     = True
backlog            = 2048
worker_connections = 1000
timeout            = 30
keepalive          = 2
umask              = 0
spew               = False
daemon             = False
proc_name          = None
tmp_upload_dir     = None

try:
    from multiprocessing import cpu_count
    workers = 2 * cpu_count() + 1
except NotImplementedError:
    workers = 3

if working_dir not in sys.path:
    sys.path.insert(0, working_dir)

debug = getattr(import_module(os.environ['DJANGO_SETTINGS_MODULE']), 'DEBUG', False)
loglevel = 'debug' if debug else 'info'


def on_starting(server):
    global worker_tmp_dir

    try:
        os.access(worker_tmp_dir, os.F_OK) or (
            os.mkdir(worker_tmp_dir)
        )
        os.stat(worker_tmp_dir).st_mode == 0o46775 or (
            os.chmod(worker_tmp_dir, 0o46775)
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
