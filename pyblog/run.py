#coding=utf-8
#!/usr/bin/env python
from flask import Flask
from admin.admin import admin
from blog.blog import blog
from flask.ext.cache import Cache 
cache = Cache(config={'CACHE_TYPE': 'simple'})
config = {
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': '10.10.10.57',
  'CACHE_REDIS_PORT': 6379,
  'CACHE_REDIS_DB': '',
  'CACHE_REDIS_PASSWORD': ''
}
pyshell=Flask(__name__,template_folder='templates',static_folder='static')

pyshell.config.from_object(config)
cache.init_app(pyshell,)
pyshell.register_blueprint(admin,url_prefix='/admin')
pyshell.register_blueprint(blog,url_prefix='/blog')

if __name__ == '__main__':
    pyshell.run()
    #pyshell.run(host='0.0.0.0', port=5000, debug=True)
