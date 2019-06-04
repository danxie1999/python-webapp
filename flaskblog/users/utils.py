from flaskblog import mail
from flaskblog.models import User
from flask_login import current_user
from flask_mail import Message
import os,secrets
from PIL import Image
from flask import current_app,url_for


## 账号路径中的头像存储函数
def save_pic(picture_file):
	##传入的是图片对象的数据
	##如果只在意返回的一个值，而返回两个值，可以把其中的一个值用_表示。
	_,ext = os.path.splitext(picture_file.filename)
	##新的文件名由 8字节的随机数和上传图片名称的后缀构成
	new_file_name = secrets.token_hex(8) + ext
	##确认文件名在数据库中不重复
	while True:
		if not User.query.filter_by(image_file=new_file_name).first():
			break
		new_file_name = secrets.token_hex(8) + ext		
	##app.root_path 是程序package目录在操作系统上的路径
	file_location = os.path.join(current_app.root_path,'static/profile_pics',new_file_name)
	## 用pillow来改变图片的大小并保存文件
	im = Image.open(picture_file)
	im.thumbnail((125,125))
	## 将图片文件存入本地指定目录
	im.save(file_location)
	##删除操作系统中的原有图片
	if current_user.image_file != 'default.jpg':
		old_file_location = os.path.join(current_app.root_path,'static/profile_pics',current_user.image_file)
		if os.path.exists(old_file_location):
			os.remove(old_file_location)
	return new_file_name


##发送邮件的函数
def send_reset_email(user):
	token = user.reset_request_token()
	##创建邮件msg实例
	msg = Message(subject="Password reset Request!",
				sender=("DTH HE WEB Admin",current_app.config['MAIL_USERNAME']),
				recipients=[user.email])
	##添加正文内容
	msg.body = '''To reset your password, please visit following link:
{}

If you did not make a request, please ignore this email, no change will make.
	'''.format(url_for('users.password_reset',token=token,_external=True))
	##发送邮件
	mail.send(msg)