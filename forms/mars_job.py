from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField, StringField, DateTimeField
from wtforms.validators import DataRequired
from datetime import datetime as dt


class JobForm(FlaskForm):
    job = StringField("Job Title", validators=[DataRequired()])
    team_leader = IntegerField("Team leader's id", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    start_date = DateTimeField("Start date(format: %Y-%m-%d %H:%M:%S)", default=dt.now(), validators=[DataRequired()])
    work_size = IntegerField("Work size", validators=[DataRequired()])
    is_finished = BooleanField("Is finished")
    submit = SubmitField("Confirm")

