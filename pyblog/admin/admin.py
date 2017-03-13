#coding=utf-8
#!/usr/bin/env python
from flask import Blueprint,Flask, render_template, request,redirect
from model.createTable import db, Article, Arttype,Friendlink,About
import math,logging
from sqlalchemy import desc,func
from datetime import datetime

admin=Blueprint('admin',__name__)


# 管理后台首页
@admin.route('/')
def index():
    return render_template('/admin/admin-index.html')
# 跳转到添加文章页面
@admin.route('/newPost')
def newPost():
    type = Arttype.query.all()
    return render_template('/admin/newPost.html',type=type)




# 跳转到文章类型
@admin.route('/newType')
def newType():
    try:
        type = Arttype.query.all()
        
        return render_template('/admin/newType.html', type=type)
        
    except StandardError,e:
        logging.exception(e)


# 跳转到文章类型
@admin.route('/allType')
def allType():
    try:
        type = Arttype.query.all()
        
        return render_template('/admin/allType.html', type=type)
    except StandardError, e:
        logging.exception(e)
# 编辑文章类型，传id 和name 2个参数
@admin.route('/editType')
def editType():
    try:
        id = request.args.get('id', None) 
        type = Arttype.query.get(id)
        name=type.name
        id=type.id
        return render_template('/admin/editType.html', id=id ,name=name)
    except StandardError,e:
        logging.exception(e)


#修改文章类型
@admin.route('/updateType', methods=['POST', 'GET'])
def updateType():
    try:
        if request.method=='POST':
            id=request.form['type_id']
            name=request.form['type']
            p=Arttype.query.get(id)
            p.name=name        
            db.session.commit()
        type=Arttype.query.all()
        return render_template('/admin/allType.html', type=type)
    except StandardError,e:
        logging.exception(e)

# 删除文章类型
@admin.route('/delType')
def delType():
    try:
        id = request.args.get('id', None)
        print id
        deltype = Arttype.query.get(id)
        print deltype
        db.session.delete(deltype)
        type = Arttype.query.all()
        return render_template('/admin/newType.html', type=type)
    except StandardError,e:
        logging.exception(e)
        
        
# 添加文章类型
@admin.route('/addNewType', methods=['POST', 'GET'])
def addNewType():
    try:
        if request.method == 'POST':
            name = request.form['type']
            print name
        a = datetime.utcnow()
        arttype = Arttype(name)
        db.session.add(arttype)
        db.session.commit()
        type = Arttype.query.all()
        return redirect('/admin/allType')
        #return render_template('/admin/newType.html', type=type)
    except StandardError,e:
        logging.exception(e)
        
# 所有文章页面
@admin.route('/allPost')
def allPost():
    try:
        article=Article.query.all()
        
        return render_template('/admin/allPost.html',article=article)
    except StandardError,e:
        logging.exception(e)

# 编辑文章页面
@admin.route('/editPost')
def editPost():
    try:
        id=request.args.get('id',None)
        postArticle=Article.query.get(id)
        
        title=postArticle.title
        label=postArticle.label
        content=postArticle.body
        type_id=postArticle.type_id
        type=(Arttype.query.get(type_id)).name
        
        print "title is %s" %title
        print "label is %s" %label
        print "content is %s" %content
        print "type_id is %d" %type_id
        print "type is %s"  %type
        return render_template('/admin/editPost.html',id=id,type=type,type_id=type_id,title=title,label=label,content=content)
    except StandardError,e:
        logging.exception(e)
# 删除文章
@admin.route('/delPost')
def delPost():
    try:
        id=request.args.get('id',None)
        postArticle=Article.query.get(id)
        db.session.delete(postArticle)
        db.session.commit()
        return redirect("/admin/allPost")
    except StandardError,e:
        logging.exception(e)

#修改文章
@admin.route('/updateText',methods=['POST','GET'])
def updateText():
    try:
        if request.method == 'POST':
            id=request.form['id']
            title=request.form['title']
            typeID=request.form['artstyle']
            body=request.form['editor']
            desc=request.form['desc']
            article=Article.query.get(id)
            article.title=title
            article.body=body
            article.label=desc
            article.type_id=typeID
            db.session.commit()
            blog=Article.query.all()
            guanyu=me()
            link=Friendlink.query.all()
            article=Article.query.get(id)
            return redirect('/blog')
            #return render_template('/blog/article.html',link=link,article=article,blog=blog,about=guanyu)
    except StandardError,e:
        logging.exception(e)
    #print id,title,label,typeID,body
        

        
#显示友情链接页面      
@admin.route('/newFreLink')
def newFreLink():
    try:
        type=Friendlink.query.all()
        
        return render_template('/admin/newFreLink.html',type=type)
    
    except StandardError,e:
        logging.exception(e)
    #return render_template('newFreLink.html') 
#添加友情链接
@admin.route('/addFreLink',methods=['POST','GET'])
def addFreLink():
    try:
        if request.method=='POST':
            url=request.form['linkAddr']
            name=request.form['linkName']
            addLink=Friendlink(url,name)
            db.session.add(addLink)
            db.session.commit()
        type=Friendlink.query.all()
        return render_template('/admin/newFreLink.html',type=type) 
    except StandardError,e:
        logging.exception(e)
#删除链接
@admin.route('/delLink')
def delLink():
    try:
        id = request.args.get('id', None)
        print id
        delLink = Friendlink.query.get(id)
        #print deltype
        db.session.delete(delLink)
        type = Friendlink.query.all()
        return render_template('/admin/newFreLink.html', type=type)
    except StandardError,e:
        logging.exception(e)
#显示所有链接
@admin.route('/allLink')
def allLink():
    try:
        type = Friendlink.query.all()
        
        return render_template('/admin/allLink.html', type=type)
        
    except StandardError,e:
        logging.exception(e)
#编辑链接
@admin.route('/editLink')
def editLink():
    try:
        id=request.args.get('id',None)
        link=Friendlink.query.get(id)
        url=link.linkurl
        name=link.linkname
        return render_template('/admin/editLink.html',id=id,url=url,name=name)
    except StandardError,e:
        logging.exception(e)
#更新链接
@admin.route('/updateLink',methods=['POST','GET'])
def updateLink():
    try:
        if request.method == 'POST':
            id=request.form['id']
            url=request.form['url']
            name=request.form['name']
            link=Friendlink.query.get(id)
            link.linkurl=url
            link.linkname=name
            db.session.commit()
        listlink=Friendlink.query.all()
        return render_template('/admin/allLink.html',type=listlink)
    except StandardError,e:
        logging.exception(e)
        
        
@admin.route('/updateme',methods=['POST','GET'])
def updateme():
    try:
        if request.method=='POST':
            id=request.form['id']
            content=request.form['aboutme']
            
            Content=About.query.get(id)
            Content.content=content
            db.session.commit()
            
        return redirect('/blog/me')
    except StandardError,e:
        logging.exception(e)
        
@admin.route('/addabout',methods=['POST','GET'])
def addAbout():
    try:
        if request.method=='POST':
            content=request.form['aboutme']
            addAbout=About(content)
            db.session.add(addAbout)
            db.session.commit()  
        return  redirect('/admin/')
    except StandardError,e:
        logging.exception(e)

@admin.route('/editme')
def editme():
    try:
        about=About.query.all()
        if len(about) >0:
        #id=about.id
            for obj in about:
                id=obj.id
                content=obj.content
            return render_template('/admin/editme.html',id=id,content=content)
        else:
            return redirect('/admin/aboutme')
    except StandardError,e:
        logging.exception(e)


@admin.route('/tianjia', methods=['POST', 'GET'])
def articletianjia():
    try:
        if request.method == 'POST':
            content = request.form['editor']
            title=request.form['title']
            desc=request.form['desc']
            typestyle=request.form['artstyle']
            #title, label, body, arttype,
            postType=Arttype.query.get(typestyle)
            print content
            print title
            print desc
            print typestyle
            addPost=Article(title,desc,content,postType)
            db.session.add(addPost)
            db.session.commit()
            return redirect('/admin/newPost')
    except StandardError,e:
        logging.exception(e)
  
@admin.route('/aboutme')
def aboutme():
    return  render_template('/admin/about.html')
  
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




@admin.route('/uedit')
def uedit():
    return render_template('/admin/b.html')
