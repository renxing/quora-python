# coding: utf-8
import re
import markdown as Markdown
from jinja2.utils import urlize, escape
def markdown(value):
    return Markdown.markdown(value)

def md_body(value):
    value = urlize(value,32,True)
    return markdown(value)
    

