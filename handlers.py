# coding: utf-8
import tornado.web
import tornado.auth
from jinja2 import Template, Environment, FileSystemLoader
import filter
import utils
import session

class BaseHandler(tornado.web.RequestHandler):

    def render(self,template,**args):
        env = Environment(loader=FileSystemLoader(self.settings['template_path']))
        env.filters['markdown'] = filter.markdown
        env.filters['truncate_lines'] = utils.truncate_lines
        template = env.get_template(template)
        self.finish(template.render(settings=self.settings,
                        notice_message=self.notice_message,
                        current_user=self.current_user,
                        xsrf_form_html=self.xsrf_form_html,
                        **args))

    @property
    def db(self):
        return self.application.db

    @property
    def session(self):
        return session.TornadoSession(self.application.session_manager, self)

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id: return None
        return self.db.get("SELECT * FROM users WHERE id = %s", int(user_id))

    def notice(self,msg,type = "success"):
        if ['error','success','warring'].count(type) == 0:
            type = "success"
        self.session["notice_%s" % type] = msg 
        self.session.save

    def notice_message():
        msg = self.session['notice_error']
        if not msg:
            return ""
        else:
            return msg

    def render_404(self):
        raise tornado.web.HTTPError(404)

class HomeHandler(BaseHandler):
    def get(self):
        asks = self.db.query("select * from asks order by id desc limit 10")
        if not asks:
            self.redirect("/ask")
        else:
            self.render("home.html", asks=asks)


class AskHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("ask.html")

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title",None)
        body = self.get_argument("body",'')
        summary = utils.truncate_lines(body,3,500)
        id = self.db.execute("INSERT INTO asks (title,body,summary,user_id,created_at)  values(%s,%s,%s,%s,UTC_TIMESTAMP())",
                        title,body,summary,self.current_user.id)
        self.redirect("/ask/%s" % id)


        
class AskShowHandler(BaseHandler):
    def get(self,id):
        ask = self.db.get("select * from asks where id = %d" % int(id))
        if not ask:
            render_404
        self.render("ask_show.html",ask=ask)



class LogoutHandler(BaseHandler):
    def get(self):
        self.render("login.html")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        email = self.get_argument("email",None)
        password = self.get_argument("password",None)
        user = self.db.get("select * from users where email = %s and password = %s", email, password)
        if not user:
            self.notice("Email or Password error.",'error')
            self.render("login.html")
        else:
            self.set_secure_cookie("user_id", str(user.id))
            self.redirect(self.get_argument("next","/"))

class FeedHandler(BaseHandler):
    def get(self):
        self.render("feed.html")
