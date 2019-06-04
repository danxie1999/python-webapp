from flask import render_template,url_for,flash,redirect,request,Blueprint
from flaskblog import db,bcrypt
from flaskblog.users.forms import (RegistrationForm,LoginForm,AccountUpdateForm,
							ResetRequestForm,PasswordResetForm)
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from flaskblog.users.utils import save_pic,send_reset_email

##创建一个蓝本实例
users = Blueprint('users',__name__)

##点击主页用户名后查询该用户的所有公告
@users.route("/home/<string:username>")
def user_posts(username):
	##定义一个page的变量，默认值为1，类型为整数，从URL的查询参数
	##page中获得
	page = request.args.get('page',1,type=int)
	##通过URL中的命名参数在数据库查出用户的对象，若不存在，返回HTTP 404
	user = User.query.filter_by(username=username).first_or_404()
	##根据用户对象查找相关的公告，按照时间的逆序，每页5个对象的查出一个页面对象
	posts = Post.query.filter_by(author=user)\
	        .order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
	return render_template('user_posts.html',posts=posts,title='User Posts',user=user)

##注册路径
@users.route("/register/",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		## 算出密码的HASH值
		Hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		## 将固定格式的username,email和hash值密码存入数据库
		user_account = User(username = form.username.data.lower().title(),email=form.email.data.lower(),password=Hashed_password)
		db.session.add(user_account)
		db.session.commit()
		flash('Account created for {} !'.format(form.username.data),'success')
		return redirect(url_for('users.login'))
	return render_template('register.html',title='Register Form',form=form)

##登录路径
@users.route("/login/",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user_account = User.query.filter_by(email=form.email.data.lower()).first()
		## 检查email是否存在数据库，密码是否正确
		if user_account and bcrypt.check_password_hash(user_account.password,form.password.data):
			##认证通过后将用户变成login状态。
			login_user(user_account,remember = form.remember.data)
			##在URI中读取查询字段中的next的值，如果没有返回none.
			next_page = request.args.get('next')
			flash('Welcome {} !'.format(form.email.data),'success')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessfully, please check your password and email !'.format(form.email.data),'danger')			

	return render_template('login.html',title='Login Form',form=form)

##退出路径
@users.route("/logout/")
def logout():
	if current_user.is_authenticated:
		logout_user()
		flash('logout successfully!!!','success')
	return redirect(url_for('main.home'))

##账号路径
@users.route("/account/",methods=['GET','POST'])
@login_required
def account():
	form = AccountUpdateForm()
	if form.submit.data and form.validate():
		if form.picture.data:
			## 返回一个新的图片名称（随机数+后缀），并
			## 将图片保存在操作系统的某个指定目录
			new_pic_string = save_pic(form.picture.data)
			## 更新数据库中的图片名称
			current_user.image_file = new_pic_string
		##更新用户名
		current_user.username = form.username.data
		##更新用户邮件
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated','success')
		return redirect(url_for('users.account'))
	##如果是HTTP GET请求就填充表单
	if request.method == 'GET':	
		form.username.data = current_user.username
		form.email.data = current_user.email
	##获取当前用户图片的操作系统路径
	image_file = url_for('static',filename='profile_pics/{}'.format(current_user.image_file))
	return render_template('account.html',title='Account',form=form,image_file=image_file)

##申请重设密码的路径
@users.route("/reset_password",methods=['GET','POST'])
def request_reset():
	##如果用户已经认证，则转到主页
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = ResetRequestForm()
	if form.validate_on_submit():
		##表格提交后，根据邮件地址查找用户对象
		user = User.query.filter_by(email=form.email.data).first()
		##发邮件
		send_reset_email(user)
		flash('A Email with instruction has been sent to your email','success')
		return redirect(url_for('users.login'))
	return render_template('request_reset.html',title='Password Reset',form=form)


##重设密码的路径
@users.route("/reset_password/<token>",methods=['GET','POST'])
def password_reset(token):
	##如果用户已经认证，则转到主页
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	##使用User Model里的verify_reset_token函数来验证
	##验证通过则返回相应的user对象
	user = User.verify_reset_token(token)
	##如果验证不通过，返回None
	if not user:
		flash('Your token is invalid or expired','warning')
		return redirect(url_for('users.request_reset'))
	form = PasswordResetForm()
	##提交后在数据库中更新密码
	if form.validate_on_submit():
		## 算出密码的HASH值
		Hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		## 将hash值密码存入数据库
		user.password = Hashed_password
		db.session.commit()
		flash('Account password has been reset !','success')
		return redirect(url_for('users.login'))		
	return render_template('password_reset.html',title='Password Reset',form=form,user=user)