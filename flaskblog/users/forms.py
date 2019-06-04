from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from flask_wtf.file import FileField,FileAllowed 
from wtforms.validators import Length,Email,InputRequired,EqualTo,ValidationError
from flaskblog.models import User 
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username = StringField('Username',
							validators=[InputRequired(),Length(min=2)])
	email = StringField('Email Address',
							validators=[InputRequired(),Email()])
	password = PasswordField('New Password',validators=[InputRequired()])
	confirm_password = PasswordField('Confirm Password',
								validators=[InputRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')
	def validate_username(self,username):
		username_input = username.data.lower().title()
		if User.query.filter_by(username=username_input).first():
			raise ValidationError('Username {} has already taken, please try again!'.format(username_input))
	def validate_email(self,email):
		email_input = email.data.lower()
		if User.query.filter_by(email=email_input).first():
			raise ValidationError('Email {} has already registered, please try again!'.format(email_input))



class LoginForm(FlaskForm):
	email = StringField('Email Address',
							validators=[InputRequired(),Email()])
	password = PasswordField('Password',validators=[InputRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class AccountUpdateForm(FlaskForm):
	username = StringField('Username',
							validators=[InputRequired(),Length(min=2)])
	email = StringField('Email Address',
							validators=[InputRequired(),Email()])
	submit = SubmitField('Update')
	picture = FileField('Update Profile Picture',
							validators=[FileAllowed(['jpg','png'])])
	def validate_username(self,username):
		if username.data != current_user.username:
			username_input = username.data.lower().title()
			if User.query.filter_by(username=username_input).first():
				raise ValidationError('Username {} has already taken, please try again!'.format(username_input))
	def validate_email(self,email):
		if email.data != current_user.email:
			email_input = email.data.lower()
			if User.query.filter_by(email=email_input).first():
				raise ValidationError('Email {} has already registered, please try again!'.format(email_input))

##用户往自己的邮箱发邮件的表格
class ResetRequestForm(FlaskForm):
	email = StringField('Email Address',
							validators=[InputRequired(),Email()])
	submit = SubmitField('Request Password Reset')
	def validate_email(self,email):
			email_input = email.data.lower()
			if not User.query.filter_by(email=email_input).first():
				raise ValidationError('Did not find Email address...'.format(email_input))

##用户重设密码的表格
class PasswordResetForm(FlaskForm):
	password = PasswordField('New Password',validators=[InputRequired()])
	confirm_password = PasswordField('Confirm Password',
								validators=[InputRequired(),EqualTo('password')])
	submit = SubmitField('Reset Password')