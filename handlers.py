# coding: utf-8
import sys
import tornado.web
import tornado.auth
from jinja2 import Template, Environment, FileSystemLoader
from pymongo.objectid import ObjectId

import filter, utils, session
from models import *

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.session = session.TornadoSession(application.session_manager, self)

    def render(self,template,**args):
        env = Environment(loader=FileSystemLoader(self.settings['template_path']))
        env.filters['markdown'] = filter.markdown
        env.filters['md_body'] = filter.md_body
        env.filters['tags_name_tag'] = filter.tags_name_tag
        env.filters['user_name_tag'] = filter.user_name_tag
        env.filters['strftime'] = filter.strftime
        env.filters['strfdate'] = filter.strfdate
        env.filters['truncate_lines'] = utils.truncate_lines
        template = env.get_template(template)
        self.finish(template.render(settings=self.settings,
                        notice_message=self.notice_message,
                        current_user=self.current_user,
                        static_url=self.static_url,
                        modules=self.ui['modules'],
                        xsrf_form_html=self.xsrf_form_html,
                        **args))

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id: return None
        try:
          return User.objects(id = user_id).first()
        except:
          return None

    def notice(self,msg,type = "success"):
        type = type.lower()
        if ['error','success','warring'].count(type) == 0:
            type = "success"
        self.session["notice_%s" % type] = msg 
        self.session.save()

    @property
    def notice_message(self):
        try:
          msg = self.session['notice_error']
          self.session['notice_error'] = None
          self.session['notice_success'] = None
          self.session['notice_warring'] = None
          self.session.save()
          if not msg:
            return ""
          else:
            return msg
        except:
          return ""

    def render_404(self):
        raise tornado.web.HTTPError(404)

class HomeHandler(BaseHandler):
    def get(self):
        last_id = self.get_argument("last", None)
        if not last_id:
          asks = Ask.objects.order_by("-replied_at").limit(10)
        else:
          asks = Ask.order_by("-replied_at").objects(id_lt = last_id).limit(10)
        if not asks:
            self.redirect("/ask")
        else:
            self.render("home.html", asks=asks)


class AskHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        ask = Ask()
        self.render("ask.html",ask=ask)

    @tornado.web.authenticated
    def post(self):
        ask = Ask(title=self.get_argument("title",None),
            body = self.get_argument("body",''),
            summary = utils.truncate_lines(self.get_argument("body",''),3,500),
            user = self.current_user,
            tags = utils.format_tags(self.get_argument("tags",'')))
        try:
          ask.save()
          self.redirect("/ask/%s" % ask.id)
        except Exception,exc:
          self.notice(exc,"error")
          self.render("ask.html",ask=ask)


        
class AskShowHandler(BaseHandler):
    def get(self,id):
        ask = Ask.objects(id=id).first()
        answers = Answer.objects(ask=ask)
        if not ask:
            render_404
        self.render("ask_show.html",ask=ask, answers=answers)


class AnswerHandler(BaseHandler):
    def get(self,ask_id):
        self.redirect("/ask/%s" % ask_id)

    @tornado.web.authenticated
    def post(self,ask_id):
        ask = Ask.objects(id=ask_id).first()
        answer = Answer(ask=ask,
                        body=self.get_argument("body",None),
                        user=self.current_user)
        try:
            answer.save()
            Ask.objects(id=ask_id).update_one(inc__answers_count=1)
            self.redirect("/ask/%s" % ask_id)
        except Exception,exc:
            self.notice(exc,"error")
            self.render("ask_show.html",ask=ask)

class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user_id","")
        self.redirect("/login")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        email = self.get_argument("email",None)
        password = utils.md5(self.get_argument("password",""))
        user = User.objects(email=email,password=password).first()
        if not user:
            self.notice("Email or Password error.",'error')
            self.render("login.html")
        else:
            self.set_secure_cookie("user_id", str(user.id))
            self.redirect(self.get_argument("next","/"))

class RegisterHandler(BaseHandler):
    def get(self):
        user = User()
        self.render("register.html", user=user)

    def post(self):
        user = User(name=self.get_argument("name",None),
            email=self.get_argument("email",None),
            password=utils.md5(self.get_argument("password","")))
        try:
          user.save()
          self.set_secure_cookie("user_id",str(user.id))
          self.redirect("/")
        except Exception,exc:
          self.notice(exc,"error")
          self.render("register.html",user=user)

class FeedHandler(BaseHandler):
    def get(self):
        self.render("feed.html")


class CommentHandler(BaseHandler):
    def post(self, commentable_type, commentable_id):
        commentable_type = commentable_type.lower()
        if ["ask","answer"].count(commentable_type) == 0: return ""
        comment = Comment(id=utils.sid(),
                          body=self.get_argument("body",None),
                          user=self.current_user)
        if commentable_type == "ask":
            Ask.objects(id=commentable_id).update_one(push__comments=comment)            
        elif commentable_type == "answer":
            Answer.objects(id=commentable_id).update_one(push__comments=comment) 
        comment_hash = { "success":1,
                "user_id":str(self.current_user.id),
                "name":self.current_user.name }
        self.write(tornado.escape.json_encode(comment_hash))

