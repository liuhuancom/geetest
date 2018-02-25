from flask import Flask
# from flask.ext.cache import Cache
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)



# cache = Cache(app,config={'CACHE_YPE':'simple'})
cache = SimpleCache()

app.config['cache_time'] = 3*24*60*60