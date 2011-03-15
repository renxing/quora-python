# coding: utf-8
from mongoengine import *
import datetime

class User(Document):
    email = EmailField(required=True,unique=True)
    name = StringField(required=True,min_length=2)
    password = StringField(required=True)
    blog = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
class Answer(EmbeddedDocument):
    body = StringField()
    user = ReferenceField(User)
    created_at = DateTimeField(default=datetime.datetime.now)

class Ask(Document):
    title = StringField(required=True,min_length=5,max_length=255)
    body = StringField()
    summary = StringField()
    user = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    answers = ListField(EmbeddedDocumentField(Answer))
    created_at = DateTimeField(default=datetime.datetime.now)
    replied_at = DateTimeField(default=datetime.datetime.now)



