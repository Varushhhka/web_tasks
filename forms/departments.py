from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')