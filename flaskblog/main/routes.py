from flask import render_template,request,Blueprint
from flaskblog.models import Post
import json
##创建一个蓝本实例
main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home/")
def home():
	##定义一个page的变量，默认值为1，类型为整数，从URL的查询参数
	##page中获得
	page = request.args.get('page',1,type=int)
	##按照时间的逆序，每页5个对象的查出一个页面对象
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
	return render_template('home.html',posts=posts)


@main.route("/about/")
def about():
    return render_template('about.html',title='About')

@main.route("/test1/",methods=['GET','POST'])
def test1():
	MESSAGE=None
	_POST=None
	if request.args.get('item'):
		MESSAGE=request.args.get('item')
	if request.form.get('item'):
		_POST=request.form.get('item')
	return render_template('test1.html',title='test1',MESSAGE=MESSAGE,_POST=_POST)

#XSS钓鱼页面
@main.route("/test2/",methods=['GET','POST'])
def test2():
	if request.args.get('sid'):
		MESSAGE=request.args.get('sid')
		return render_template('test2.html',title='test2',MESSAGE=MESSAGE)
	return render_template('test2.html',title='test2')

