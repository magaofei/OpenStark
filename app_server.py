#!/usr/bin/env python3
# coding=utf8
"""
Author: 归根落叶
Blog: https://www.bstester.com
"""

from tornado import httpserver, ioloop
from tornado.options import options, define
from tornado.web import Application
from functions.scheduler import job_monitor
from settings import *
import urls


class AppServer(Application):
    """应用启动入口"""
    def __init__(self):
        handlers = urls.handlers
        settings = {'template_path': template_path,
                    'static_path': static_path,
                    'cookie_secret': cookie_secret,
                    'xsrf_cookie': xsrf_cookie,
                    'login_url': login_url,
                    'ui_modules': ui_modules,
                    'debug': debug}
        Application.__init__(self, handlers, **settings)


def main():
    define('port', default=9090, help='run on the given port', type=int)
    define('monitor', default='on', help='open jobs monitor', type=str)

    options.parse_command_line()
    http_server = httpserver.HTTPServer(AppServer(), xheaders=True)
    http_server.listen(options.port)
    if options.monitor.lower() == 'on':
        ioloop.PeriodicCallback(job_monitor, cycle_time * 1000).start()
    ioloop.IOLoop.instance().run_sync(init_db)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
