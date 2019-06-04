import base64,json
#定义变量
# from_addr="xiedan1999@163.com"
# to_addr="dxie@synamedia.com"
# smtp_server="smtp.163.com"

##读取json中的信息
with open('C:\\config\\flask_config.json') as config:
	config = json.load(config)


class Config:
	#使用secure token来保护cookie信息
	SECRET_KEY = config['SECRET_KEY']
	SQLALCHEMY_DATABASE_URI = config['SQLALCHEMY_DATABASE_URI']
	##SMTP 服务器的配置
	MAIL_SERVER = config['MAIL_SERVER'] 
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = config['MAIL_USERNAME'] 
	MAIL_PASSWORD = base64.decodestring(config['MAIL_PASSWORD'].encode('utf-8')).decode('utf-8')