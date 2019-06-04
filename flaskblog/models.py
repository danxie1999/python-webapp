from datetime import datetime
from flaskblog import db,login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

#从用户的Session里的用户ID来获得用户对象
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

## UserMixin 是让User 类继承一些Method,例如 is_authenticated
class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True,nullable=False)
	email = db.Column(db.String(120),unique=True,nullable=False)	
	image_file = db.Column(db.String(60),nullable=False,default='default.jpg')
	password = db.Column(db.Unicode,nullable=False)
	#创建一个DB的一对多关系，Post对应子Model Post, backref对应在子Model中的隐藏属性
	#隐藏属性的值是和主Model的实例相关联。 而posts这个属性又和隐藏属性相对应（一对多）	
	posts = db.relationship('Post',backref='author',lazy=True)
	##加载用户ID,生成安全令牌，
	def reset_request_token(self,exp_time=300):
		s = Serializer(current_app.config['SECRET_KEY'],exp_time)
		token = s.dumps({'user_id': self.id}).decode('utf-8')
		return token
	##验证安全令牌的有效性，如果有效则返回用户对象
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return 'User <{},{},{}>'.format(self.username,self.email,self.image_file)

class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content = db.Column(db.Unicode,nullable=False)
	image_file = db.Column(db.String(60))	
	## owner_id是User的外键
	owner_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return  'Post <{},{}>'.format(self.title,self.date_posted)
