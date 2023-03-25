from flask import url_for, Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'


@app.route('/training/<prof>')
def first_sample(prof):
    param = dict()
    param["prof"] = prof
    if prof == "physician":
        param["photo"] = url_for('static', filename=f'img/Mars.jpg')
    elif prof == "engineer":
        param["photo"] = url_for('static', filename=f'img/engineer_sim.jpg')
    return render_template('base.html', **param)


@app.route('/index/<title>')
def first_task(title):
    param = dict()
    param["title"] = title
    return render_template('main.html', **param)


@app.route('/list_prof/<list_param>')
def list_prof(list_param):
    param = dict()
    param["profs"] = ["engineer", "physician"]
    param["par"] = list_param
    return render_template("task3.html", **param)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer(dictionary=None):
    param = dict()
    unk = 'unknown'
    param["title"], param["surname"], param["name"], param["education"] = "Questionnaire", unk, unk, unk
    param["education"], param["profession"], param["sex"], param["motivation"], param["ready"] = unk, unk, unk, unk, unk
    if dictionary:
        for key in param:
            try:
                param[key] = dictionary[key]
            except KeyError:
                pass
    return render_template("auto_answer.html", **param)


class LoginForm(FlaskForm):
    id_astronaut = IntegerField("id astronaut", validators=[DataRequired()])
    password_astronaut = PasswordField("Astronaut's password", validators=[DataRequired()])
    id_captain = IntegerField('id captain', validators=[DataRequired()])
    password_captain = PasswordField("Captain's password", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('double_defence.html', title='Authorisation', form=form)


@app.route('/success')
def show_success():
    return 'Success'


@app.route('/distribution')
def distribution():
    list_astronauts = ['Garry', "Peter", "Jack", "Mark", "Teddy"]
    return render_template('distribution.html', list_astronauts=list_astronauts)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
