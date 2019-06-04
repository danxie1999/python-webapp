from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.Config import Config

SERVER_NAME = 'Custom Flask Web Server v0.1.0'

#override Flask中的 Flask.process_response() method以修改响应首部字段
class localFlask(Flask):
	def process_response(self, response):
	#Every response will be processed here first
		response.headers['server'] = SERVER_NAME
		##继承父类的method
		super().process_response(response)
		return(response)

##初始化 SQLAlchemy
db = SQLAlchemy()
##初始化 bcrypt
bcrypt = Bcrypt()
##初始化 LoginManager 
login_manager = LoginManager()
##使用login_required是跳转的页面
login_manager.login_view = 'users.login'
## 跳转时的提示语（以flash形式存在）
login_manager.login_message = '访问该页面，需要认证！'
## 提示语的形式
login_manager.login_message_category = 'info'

#初始化Mail
mail = Mail()




def create_app(config_class=Config):
	app = localFlask(__name__)
	##从文件中导入app配置
	app.config.from_object(config_class)
	##把cookie的保护关了，默认是开的
	app.config['SESSION_COOKIE_HTTPONLY'] = False

	#使用secure token来保护cookie信息
	# app.config['SECRET_KEY'] = '629ed7150113f8f5ee9a219433c7d6ab'
	## 为了避免循环导入，routes模块需要放在app初始化之后。

	##初始化所有的子程序，将子程序和主程序隔离，不同的主程序可以使用相同的子程序
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	## 注册蓝本
	#导入蓝本实例
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.error_handler import errors
	##注册蓝本实例
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	return app
