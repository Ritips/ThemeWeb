from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    category = IntegerField("Hazard Level", validators=[DataRequired()], default=1)
    submit = SubmitField("Submit")
