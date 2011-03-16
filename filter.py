# coding: utf-8
import re
import markdown as Markdown
from jinja2.utils import urlize, escape

def markdown(value):
    return Markdown.markdown(value)

def md_body(value):
    value = urlize(value,32,True)
    return markdown(value)
    
def tags_name_tag(tags,limit = 0):
    html = []
    if not tags: return ""
    if limit > 0:
      tags = tags[0:limit]
    for tag in tags:
        html.append('<a class="tag" href="/tag/%s">%s</a>' % (tag,tag))
    return ",".join(html)

def user_name_tag(user):
    return '<a href="/user/%s" class="user">%s</a>' % (user.id,user.name)
        
def strftime(value, type='normal'):
    if type == 'normal':
        format="%Y-%m-%d %H:%M"
    elif type == 'long':
        format="%Y-%m-%d %H:%M:%S"
    else:
        format="%m-%d %H:%M"
    return value.strftime(format)

def strfdate(value,type='normal'):
    if type == 'normal':
        format="%Y-%m-%d"
    elif type == "long":
        format="%Y-%m-%d"
    else:
        format="%m-%d"
    return value.strftime(format)
    
