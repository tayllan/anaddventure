from flask import Flask, Blueprint
from flask_mail import Mail
from flask_cache import Cache

# BEGIN app configuration
app = Flask(__name__)
app.config.update(
	# FLASK SETTINGS
	SECRET_KEY = '\xe1{\xb3\x96\xbac\x1ds\xad\x04\x92@\x0e\x8d\xaf`|\x95P\x84;\xa7\x0b\x98\xbcX\x9d\xeaV\x7f',
	MAX_CONTENT_LENGTH = 1024 * 1024,
	#DEBUG = True, SERVER_NAME = 'anaddventure.com.dev:5000', CONF_PRODUCTION = False,
	DEBUG = False, SERVER_NAME = 'anaddventure.com', CONF_PRODUCTION = True,

	# PERSONAL SETTINGS
	SITE_NAME = 'An Addventure',
	SITE_URL = 'https://www.anaddventure.com',

	# EMAIL SETTINGS
	MAIL_SERVER = 'smtp-mail.outlook.com',
	MAIL_PORT = 587,
	MAIL_USE_TLS = True,
	MAIL_DEFAULT_SENDER = 'anaddventure@outlook.com',
	MAIL_USERNAME = 'anaddventure@outlook.com',
	MAIL_PASSWORD = 'autoescola19',
)
www = Blueprint('www', __name__, 	subdomain = 'www', 	static_folder = 'static', 	static_url_path = '/static')
pt = Blueprint('pt', __name__, subdomain = 'pt', static_folder = 'static', static_url_path = '/static')
cache = Cache(app, config = {
	'CACHE_DEFAULT_TIMEOUT': 300,
	'CACHE_TYPE': 'redis',
	'CACHE_KEY_PREFIX': 'fcache',
	'CACHE_REDIS_HOST': 'localhost',
	'CACHE_REDIS_PORT': '6379',
	'CACHE_REDIS_URL': 'redis://localhost:6379',
})
mail = Mail(app)
# END app configuration

import controllers

app.register_blueprint(www)
app.register_blueprint(pt)