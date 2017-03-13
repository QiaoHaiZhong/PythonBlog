# coding=utf-8
'''
Created on 2015年11月29日
@author: Administrator
'''
from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from config.config import username,password,host,port,dbname,dbType

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@10.10.10.39:3306/pyblog'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://qhz:123456@127.0.0.1:3306/pyblog'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/pyblog'
app.config['SQLALCHEMY_DATABASE_URI'] = dbType+"://"+username+":"+password+"@"+host+":"+port+"/"+dbname
db = SQLAlchemy(app)
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    label = db.Column(db.String(200))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    type_id = db.Column(db.Integer, db.ForeignKey('arttype.id'))
    arttype = db.relationship('Arttype', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, label, body, arttype, pub_date=None):
        self.title = title
        self.label = label
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.arttype = arttype
    def __repr__(self):
        return '<Post %r>' % self.title
    
class Arttype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    add_date = db.Column(db.DateTime)  
    def __init__(self, name, add_date=None):
        self.name = name
        if add_date is None:
            add_date = datetime.utcnow()
        self.add_date = add_date
    def __repr__(self):
        return '<ArtType %r>' % self.name

class Msg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.String(db.String(50))
    email = db.Column(db.String(50))
    content = db.Column(db.Text)
    msg_date = db.Column(db.DateTime)

    def __init__(self, ip, email, content, msg_date=None):
        
        self.ip = ip
        self.email = email
        self.content = content
        if msg_date is None:
            msg_date = datetime.utcnow()
        self.msg_date = msg_date

    def __repr__(self):
        return '<Category %r>' % self.email
 
class About(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text)
    about_time=db.Column(db.DateTime)
     
    def __init__(self,content,about_time=None):
        self.content=content
        if about_time is None:
            about_time=datetime.utcnow()
        self.about_time=about_time
    
    def __repr__(self):
        return '<About %r' % self.about_time
    
class Friendlink(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    linkurl=db.Column(db.String(500))
    linkname=db.Column(db.String(500))
    add_time=db.Column(db.DateTime)
     
    def __init__(self,linkurl,linkname,add_time=None):
        self.linkurl=linkurl
        self.linkname=linkname
        if add_time is None:
            add_time=datetime.utcnow()
        self.add_time=add_time
    
    def __repr__(self):
        return '<About %r' % self.add_time
      
db.create_all()
db.session.commit()
#print Arttype.query.filter_by(id=40).all()
#print db.session.query(Arttype,Article).filter_by(Arttype.id=Article.type_id)
#print db.session.query(Arttype.id,Arttype.name,func.count(Article.id)).join(Article).filter(Arttype.id==Article.type_id).group_by(Article.type_id)

#mulu=db.session.query(Arttype.id,Arttype.name,func.count(Article.id)).join(Article).filter(Arttype.id==Article.type_id).group_by(Article.type_id).all()
#for i in mulu:
    #print i.id
    #print i.name
    #print i.keys
    #print i[2]
    #print dir(i)
    #print i.index
    #print i[2]

#print db.session.query(Arttype).filter_by(id=40)
#.where(article.type_id=Arttype.id)
#print db.session.query(Article.type_id,Arttype.name,func.count(Article.id)).filter_by(Article.type_id==Arttype.id).group_by(Arttype.id)
#print Arttype.query.filter_by(Arttype.id=40)
#a=db.session.query(Article.type_id,Arttype.name,func.count(Article.id)).filter_by(article.type_id=Arttype.id).all()
#print a
#a = Arttype('flask')
#b = Article('study flask', 'sdjfksd', 'skdjfksjfsdkfj', a)
#db.session.add(b)

