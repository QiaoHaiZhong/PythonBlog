from flask import Flask
from flask.ext.cache import Cache 
cache = Cache(config={'CACHE_TYPE': 'simple'})
config = {
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': '10.10.10.57',
  'CACHE_REDIS_PORT': 6379,
  'CACHE_REDIS_DB': '',
  'CACHE_REDIS_PASSWORD': ''
}
  
app = Flask(__name__)
app.config.from_object(config)
cache.init_app(app)
  
@app.route('/')
@cache.cached(timeout=60*2)
def index():
  name = 'mink'
  return name
  
if __name__ == '__main__':
  app.run()