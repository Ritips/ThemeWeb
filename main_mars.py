from data import db_session
import datetime
from datetime import datetime as dt
from data.mars_user import User
from data.mars_jobs import Jobs
from data.mars_departments import Department
from flask import Flask, render_template
from forms.mars_user import RegisterMarsForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandex_lyceum_secret_key'


def add_person(db_sess, surname, name, age, position, speciality, address, email):
    user = User()
    user.surname, user.name, user.age, user.position = surname, name, age, position
    user.speciality, user.address, user.email = speciality, address, email
    db_sess.add(user)
    db_sess.commit()


def add_job(db_sess, team_leader, description_job, work_size, collaborators, start_date=dt.now(), is_finished=False):
    job = Jobs()
    job.team_leader, job.job, job.work_size = team_leader, description_job, work_size
    job.collaborators, job.start_date, is_finished = collaborators, start_date, is_finished
    job.end_date = start_date + datetime.timedelta(hours=work_size)
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
    return render_template('magazine_jobs.html', title="MAGAZINE JOBS", elements=jobs)


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
        user = User(name=form.name.data, surname=form.surname.data,
                    age=form.age.data, position=form.position.data,
                    speciality=form.speciality.data, address=form.address.data,
                    email=form.email.data, modified_date=datetime.datetime.now())
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return "Success"
    return render_template("mars_register.html", form=form, title="Registration")


def main():
    db_session.global_init('db/mars_explorer.db')
    app.run()


if __name__ == '__main__':
    main()
