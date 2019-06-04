from flask import Blueprint,render_template

##创建一个蓝本实例
errors = Blueprint('errors',__name__)

##网页错误的路径,app_errorhandler中app_的目的是使这些handler可以在所有其他的蓝本中还能使用
@errors.app_errorhandler(404)
def error_404(error):
	return render_template('/errors/404.html'),404

@errors.app_errorhandler(403)
def error_403(error):
	return render_template('/errors/403.html'),403

@errors.app_errorhandler(500)
def error_500(error):
	return render_template('/errors/500.html'),500

