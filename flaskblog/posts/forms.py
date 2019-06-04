from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from flask_wtf.file import FileField,FileAllowed 
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
	title = StringField('Title',validators=[InputRequired()])
	content = TextAreaField('Content',validators=[InputRequired()])
	picture = FileField('Upload Image', 
							validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Post')