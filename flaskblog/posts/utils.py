from flask import current_app
from flaskblog.models import Post
import os,secrets
from PIL import Image



##公告路径中的图片存储功能
def save_post_pic(picture_file,old_image=None):
	##传入的是图片对象的数据
	##如果只在意返回的一个值，而返回两个值，可以把其中的一个值用_表示。
	_,ext = os.path.splitext(picture_file.filename)
	##新的文件名由 8字节的随机数和上传图片名称的后缀构成
	new_file_name = secrets.token_hex(8) + ext
	##确认文件名在数据库中不重复
	while True:
		if not Post.query.filter_by(image_file=new_file_name).first():
			break
		new_file_name = secrets.token_hex(8) + ext		
	##app.root_path 是程序package目录在操作系统上的路径
	file_location = os.path.join(current_app.root_path,'static/post_pics',new_file_name)
	## 用pillow来改变图片的大小并保存文件
	im = Image.open(picture_file)
	im.thumbnail((1200,1200))
	## 将图片文件存入本地指定目录
	im.save(file_location)
	##删除操作系统中的原有图片
	if old_image:
		old_file_location = os.path.join(current_app.root_path,'static/post_pics',old_image)
		if os.path.exists(old_file_location):
			os.remove(old_file_location)
	return new_file_name