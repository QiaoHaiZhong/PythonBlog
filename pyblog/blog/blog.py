#coding=utf-8
#!/usr/bin/env python
from flask import Flask ,Blueprint,render_template,request,redirect
from model.createTable import db, Article, Arttype,Friendlink,About
from config.config import POSTS_PRE_PAGE
import math,logging,sys
from sqlalchemy import desc,func
from datetime import datetime
from flask.ext.cache import Cache 
reload(sys)
sys.setdefaultencoding("utf-8")
cache = Cache()
config = {
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': '10.10.10.57',
  'CACHE_REDIS_PORT': 6379,
  'CACHE_REDIS_DB': '',
  'CACHE_REDIS_PASSWORD': ''
}

blog=Blueprint('blog',__name__)
# blog.config.from_object(config)
# cache.init_app(blog)
#每个页面显示文章数量
POSTS_PRE_PAGE=POSTS_PRE_PAGE
def me():
    try:
        jinali=About.query.all()
        if len(jinali)==0:
            return redirect("/admin-index")
        else:
            for i in jinali:
                about=i.content
        return about
    except StandardError,e:
        logging.exception(e)
#博客页面首页
@blog.route('/')
def home():
    return redirect('/blog/blog')
@blog.route('/blog')
#@cache.cached(timeout=60*2)
def bloglist():
    try:
        blogL=Article.query.limit(5).all()
        blogArticle=Article.query.all()
        #about=aboutme()
        link=Friendlink.query.all()
        jinali=About.query.all()
        for i in jinali:
            about=i.content
        #print about
        guanyu=me()
        menu=Arttype.query.all()
        print menu
        print guanyu
        artstyle=db.session.query(Arttype.id,Arttype.name,func.count(Article.id)).join(Article).filter(Arttype.id==Article.type_id).group_by(Article.type_id).all()
        print artstyle
        page = int(request.args.get('page', '1'))
        #POSTS_PRE_PAGE = POSTS_PRE_PAGE
        if page < 1:
            page = 1
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
        else:
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
            object_list = paginate.items
            print type(object_list)
            total = paginate.total
            total=total/POSTS_PRE_PAGE
            total=int(math.ceil(total))
            print total
            print "总页数是 ".join(str(total))
            #return render_template('list.html',paginate=paginate,object_list=object_list,POSTS_PRE_PAGE=POSTS_PRE_PAGE,total=total)
        #return render_template('/blog/test.html')
        return render_template('/blog/blog.html',artstyle=artstyle,menu=menu,blogL=blogL,about=guanyu,link=link,paginate=paginate,object_list=object_list,POSTS_PRE_PAGE=POSTS_PRE_PAGE,total=total) 
    except StandardError,e:
        logging.exception(e)
        
        
 
@blog.route('/article')
def article():
    try:
        id=request.args.get('id',None)
        article=Article.query.get(id)
        blogL=Article.query.limit(5).all()
        blogArticle=Article.query.all()
        guanyu=me()
        menu=Arttype.query.all()
        link=Friendlink.query.all()
        page = int(request.args.get('page', '1'))
        #POSTS_PRE_PAGE = POSTS_PRE_PAGE
        artstyle=db.session.query(Arttype.id,Arttype.name,func.count(Article.id)).join(Article).filter(Arttype.id==Article.type_id).group_by(Article.type_id).all()

        if page < 1:
            page = 1
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
        else:
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
            object_list = paginate.items
            total = paginate.total
            total=total/POSTS_PRE_PAGE
            total=int(math.ceil(total))
            print "总页数是 ".join(str(total))
        return render_template('/blog/article.html',menu=menu,artstyle=artstyle,link=link,article=article,blogL=blogL,about=guanyu,paginate=paginate,object_list=object_list,POSTS_PRE_PAGE=POSTS_PRE_PAGE,total=total)  
    except StandardError,e:
        logging.exception(e)


@blog.route('/post/<int:post_id>')
def showType(post_id):
    try:
        print post_id
        #blogL=Article.query.filter_by(type_id=post_id).all()
        blogArticle=Article.query.filter_by(type_id=post_id).all()
        print blog
        guanyu=me()
        gme=About.query.all()
        blogL=Article.query.limit(5).all()
        link=Friendlink.query.all()
        menu=Arttype.query.all()
        for i in gme:
            content=i.content
            addTime=i.about_time
        artstyle=db.session.query(Arttype.id,Arttype.name,func.count(Article.id)).join(Article).filter(Arttype.id==Article.type_id).group_by(Article.type_id).all()
        page = int(request.args.get('page', '1'))
        #POSTS_PRE_PAGE = 2
        if page < 1:
            page = 1
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
        else:
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
            object_list = paginate.items
            total = paginate.total
            total=total/POSTS_PRE_PAGE
            total=int(math.ceil(total))
            print "总页数是 ".join(str(total))
        return render_template('/blog/typeBlog.html',menu=menu,blogArticle=blogArticle,artstyle=artstyle,link=link,content=content,blogL=blogL,addTime=addTime,about=guanyu,paginate=paginate,object_list=object_list,POSTS_PRE_PAGE=POSTS_PRE_PAGE,total=total)  
    except StandardError,e:
        logging.exception(e)
       

@blog.route('/me')
def showme():
    try:
        guanyu=me()
        gme=About.query.all()
        blogL=Article.query.limit(5).all()
        link=Friendlink.query.all()
        menu=Arttype.query.all()
        for i in gme:
            content=i.content
            addTime=i.about_time
        artstyle=db.session.query(Arttype.id,Arttype.name,func.count(Article.id)).join(Article).filter(Arttype.id==Article.type_id).group_by(Article.type_id).all()  
        page = int(request.args.get('page', '1'))
        #POSTS_PRE_PAGE = 2
        if page < 1:
            page = 1
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
        else:
            paginate = Article.query.order_by(desc(Article.id)).paginate(page, POSTS_PRE_PAGE, False)
            object_list = paginate.items
            total = paginate.total
            total=total/POSTS_PRE_PAGE
            total=int(math.ceil(total))
            print "总页数是 ".join(str(total))
        return render_template('/blog/me.html',menu=menu,artstyle=artstyle,link=link,content=content,blogL=blogL,addTime=addTime,about=guanyu,paginate=paginate,object_list=object_list,POSTS_PRE_PAGE=POSTS_PRE_PAGE,total=total)
    except StandardError,e:
        logging.exception(e)
        
def label():
    label=Article.query.all()
    Label={}
    for i in label:
        Label['name']=i.Label
        Label['value']=Random.random(10000)
        Label['itemStyle']='createRandomItemStyle()'
   
    print Label
    
@blog.route('/aboutme')
def aboutme():
    return  render_template('about.html')