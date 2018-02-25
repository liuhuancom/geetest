from flask import Flask
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)

cache = SimpleCache()

app.config['cache_time'] = 3*24*60*60

