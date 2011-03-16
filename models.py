# coding: utf-8
from mongoengine import *
import datetime

class User(Document):
    email = EmailField(required=True,unique=True)
    name = StringField(required=True,min_length=2)
    password = StringField(required=True)
    blog = URLField()
    created_at = DateTimeField(default=datetime.datetime.now)

class Comment(EmbeddedDocument):
    id = StringField(required=True)
    body = StringField(required=True,min_length=4, max_length=2000)
    user = ReferenceField(User)
    created_at = DateTimeField(default=datetime.datetime.now)
    
class Ask(Document):
    title = StringField(required=True,min_length=5,max_length=255)
    body = StringField()
    summary = StringField()
    user = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    answers_count = IntField(required=True,default=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    replied_at = DateTimeField(default=datetime.datetime.now)

class Answer(Document):
    ask = ReferenceField(Ask)
    body = StringField()
    user = ReferenceField(User)
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.datetime.now)

