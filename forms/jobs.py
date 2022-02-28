from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Job', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    start_date = StringField('Start date')
    end_date = StringField('End date')
    is_finished = BooleanField("Is finished")
    submit = SubmitField('Submit')