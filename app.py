# coding: UTF-8
import os
import re
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import unicodedata
from tornado.options import define, options
from jinja2 import Template, Environment, FileSystemLoader
from handlers import *
import filter
import session

def markdown_tag(str):
    return markdown.markdown(str)

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="wenda", help="blog database name")
define("mysql_user", default="monster", help="blog database user")
define("mysql_password", default="123123", help="blog database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/feed", FeedHandler),
            (r"/ask/([^/]+)", AskShowHandler),
            (r"/ask/([^/]+)/answer", AnswerHandler),
            (r"/ask", AskHandler),
            (r"/login", LoginHandler),
            (r"/register", RegisterHandler),
            (r"/logout", LogoutHandler),
        ]
        settings = dict(
            app_name=u"Quora",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="81o0TzKaPpGaYdkL5gEmGepeuuYi7EPnp2XdTP1o/Vo=",
            login_url="/login",
            session_secret='08091287&^(01',
            session_dir=os.path.join(os.path.dirname(__file__), "tmp/session"),
        )
        self.session_manager = session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == "__main__":
    main()
