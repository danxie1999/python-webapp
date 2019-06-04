from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flask_login import current_user,login_required
from flaskblog.posts.utils import save_post_pic

##创建一个蓝本实例
posts = Blueprint('posts',__name__)

##公告创建路径
@posts.route("/post/new",methods=['GET','POST'])
@login_required
def post_form():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data,content=form.content.data,author=current_user)
		if form.picture.data:
			picture_name = save_post_pic(form.picture.data)
			post.image_file = picture_name
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created','success')
		return redirect(url_for('main.home'))
	return render_template('create_update_post.html',title='New Post',form=form,legend="New Post")


##公告查看路径
##在Flask的路由环境中可以利用<varible>在路由路径中提取变量
@posts.route("/post/<int:post_id>",methods=['GET','POST'])
def post_detail(post_id):
	##get_or_404表示如果数据库中没有则返回HTTP 404
	post = Post.query.get_or_404(post_id)
	return render_template('post_detail.html',title=post.title,post=post,legend='New Post')


##公告的更新路径
@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def post_update(post_id):
	##get_or_404表示如果数据库中没有则返回HTTP 404
	post = Post.query.get_or_404(post_id)
	##如果当前用户不是公告作者则返回HTTP 403
	if post.author != current_user:
		##返回 HTTP 403
		abort(403)	

	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		##如果存在图片更新存储新图片，删除老图片，更新数据库的图片信息
		if form.picture.data:
			new_pic_string = save_post_pic(form.picture.data,post.image_file)
			post.image_file = new_pic_string
		db.session.commit()
		flash('Your post has been updated','success')
		return redirect(url_for('posts.post_detail',post_id=post.id))
	if request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_update_post.html',title='Update Post',form=form,legend='Update Post')

##公告的删除路径
@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def post_delete(post_id):
	post = Post.query.get_or_404(post_id)
	##如果当前用户不是公告作者则返回HTTP 403
	if post.author != current_user:
		##返回 HTTP 403
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted','success')
	return redirect(url_for('main.home'))

