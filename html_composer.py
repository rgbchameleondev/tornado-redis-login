import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import config
import random
from tornado.options import define, options, parse_command_line
from datetime import datetime, timedelta

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


def check_auth(session):
    if session is not None and config.redis_con.get(session) is not None:
        return True
    else:
        return False


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/login")


class LoginHandler(tornado.web.RequestHandler):

    def get(self):

        session = self.get_cookie("SSID")
        if check_auth(session):
            self.redirect("/dashboard")
        else:
            self.render("pages/login.html")

    def post(self):
        username = (self.get_argument("uname"))
        password = (self.get_argument("psw"))

        if username == config.username and password == config.password:

            session = str(random.getrandbits(256))
            config.redis_con.set(session, "admin")
            self.set_cookie("SSID", session)
            self.redirect("/dashboard")

        else:
            self.redirect("/login")


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        session = self.get_cookie("SSID")
        if check_auth(session):
            config.redis_con.delete(session)
            self.redirect("/login")
        else:
            self.redirect("/login")


class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        session = self.get_cookie("SSID")
        if check_auth(session):
            # stat_obj = list(config.mongo_con.statistics.find({}, {"_id": 0}))
            # print(stat_obj)
            # data = {
            #     "statistics": stat_obj
            # }
            data = {}

            content = {
                "page": "dashboard",
                "content_block": "blocks/dashboard.html",
                "data": data
            }

            self.render("pages/content.html", content=content)
        else:
            self.redirect("/login")


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", RootHandler),
            (r'/favicon.ico', tornado.web.StaticFileHandler,
             dict(url=os.path.join(os.path.dirname(__file__), '/static/favicon.ico'), permanent=False)),

            (r"/logout", LogoutHandler),
            (r"/login", LoginHandler),
            (r"/dashboard", DashboardHandler),

        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
