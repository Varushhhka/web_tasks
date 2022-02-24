from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname')
    name = StringField('Name')
    age = IntegerField('Age')
    position = StringField
    speciality = StringField('Speciality')
    address = TextAreaField("Address")
    submit = SubmitField('Submit')