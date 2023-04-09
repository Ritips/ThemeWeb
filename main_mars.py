import flask_login
from data import db_session
import datetime
from datetime import datetime as dt
from data.mars_user import User
from data.mars_jobs import Jobs
from data.mars_departments import Department
from flask import Flask, render_template
from forms.mars_user import RegisterMarsForm
from flask import request, make_response, session, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.mars_loginform import LoginForm
from forms.mars_job import JobForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandex_lyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


def add_person(db_sess, surname, name, age, position, speciality, address, email):
    user = User()
    user.set_information(surname=surname, name=name, age=age, position=position,
                         speciality=speciality, address=address, email=email, modified_date=datetime.datetime.now())
    db_sess.add(user)
    db_sess.commit()


def add_job(db_sess, team_leader, description_job, work_size, collaborators, start_date=dt.now(), is_finished=False):
    job = Jobs(team_leader=team_leader, job=description_job, work_size=work_size, collaborators=collaborators,
               start_date=dt.now(), is_finished=is_finished, end_date=start_date + datetime.timedelta(hours=work_size))
    db_sess.add(job)
    db_sess.commit()


def add_department(db_sess, title, chief, members, email):
    department = Department(title=title, chief=chief, members=members, email=email)
    db_sess.add(department)
    db_sess.commit()


@app.route('/')
def magazine_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template('magazine_jobs.html', title="MAGAZINE JOBS", elements=jobs,
                           current_user=flask_login.current_user)


@app.route('/register', methods=["GET", "POST"])
def registration_user():
    form = RegisterMarsForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template("mars_register.html", form=form,
                                   title="Registration", message="Password mismatch")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("mars_register.html", form=form,
                                   title="Registration", message="User already exists")
        user = User()
        user.set_information(name=form.name.data, surname=form.surname.data, age=form.age.data,
                             position=form.position.data, speciality=form.speciality.data, address=form.address.data,
                             email=form.email.data, modified_date=datetime.datetime.now())
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return "Success"
    return render_template("mars_register.html", form=form, title="Registration")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('example_loginform.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('example_loginform.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def adding_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        start_date = form.start_date.data
        work_size = form.work_size.data
        end_date = start_date + datetime.timedelta(hours=work_size)
        jobs.set_information(job=form.job.data, team_leader=form.team_leader.data, start_date=start_date,
                             work_size=work_size, end_date=end_date,
                             is_finished=form.is_finished.data, collaborators=form.collaborators.data)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('mars_add_job.html', title="Adding Job", form=form)


def main():
    db_session.global_init('db/mars_explorer.db')
    app.run()


if __name__ == '__main__':
    main()
