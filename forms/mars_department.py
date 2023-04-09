from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField("Title of department", validators=[DataRequired()])
    chief = IntegerField("id Chief", validators=[DataRequired()])
    members = StringField("Department members", validators=[DataRequired()])
    email = EmailField("Department email", validators=[DataRequired()])
    submit = SubmitField("Submit")
