import flask_login
from data import db_session
import datetime
from datetime import datetime as dt
from data.mars_user import User
from data.mars_jobs import Jobs
from data.mars_departments import Department
from flask import Flask, render_template
from forms.mars_user import RegisterMarsForm
from flask import request, make_response, session, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.mars_loginform import LoginForm
from forms.mars_job import JobForm
from forms.mars_department import DepartmentForm
from forms.mars_categoriesform import CategoryForm
from data.mars_categories import Categories

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
        return redirect('/')
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
        return render_template('mars_loginform.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('mars_loginform.html', title='Authorisation', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
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
        category = form.category.data
        get_category = db_sess.query(Categories).filter(Categories.hazard_category == category).first()
        if not get_category:
            return render_template("mars_add_job.html", title="Adding job", form=form, message="Category doesn't exist")
        jobs.categories.append(get_category)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('mars_add_job.html', title="Adding Job", form=form)


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = JobForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if jobs and (jobs.user.id == flask_login.current_user.id or flask_login.current_user.id == 1):
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.work_size.data = jobs.work_size
            form.is_finished.data = jobs.is_finished
            categories = [el.hazard_category for el in jobs.categories]
            if categories:
                form.category.data = categories[0]
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if jobs and (jobs.user.id == flask_login.current_user.id or flask_login.current_user.id == 1):
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.start_date = form.start_date.data
            jobs.collaborators = form.collaborators.data
            jobs.work_size = form.work_size.data
            jobs.is_finished = form.is_finished.data
            jobs.end_date = form.start_date.data + datetime.timedelta(hours=form.work_size.data)
            form_category = form.category.data
            get_category = db_sess.query(Categories).filter(Categories.hazard_category == form_category).first()
            if get_category:
                categories = [el for el in jobs.categories]
                if categories:
                    jobs.categories.remove(categories[0])
                jobs.categories.append(get_category)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('mars_add_job.html', title="Edit job", form=form)


@app.route('/delete_job/<int:job_id>', methods=["GET", 'POST'])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if jobs and (jobs.user.id == flask_login.current_user.id or flask_login.current_user.id == 1):
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def show_departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('mars_departments.html', elements=departments, title="List of Departments",
                           current_user=flask_login.current_user)


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = Department()
        departments.title = form.title.data
        departments.chief = form.chief.data
        departments.members = form.members.data
        departments.email = form.email.data
        db_sess.add(departments)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', form=form, title="Adding department")


@app.route('/edit_department/<int:id_department>', methods=['GET', 'POST'])
@login_required
def edit_department(id_department):
    form = DepartmentForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(Department.id == id_department).first()
        if departments and (departments.user.id == flask_login.current_user.id or flask_login.current_user.id == 1):
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(Department.id == id_department).first()
        if departments and (departments.user.id == flask_login.current_user.id or flask_login.current_user.id == 1):
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_department.html', form=form, title="Editing department")


@app.route('/delete_department/<int:id_department>', methods=['GET', 'POST'])
@login_required
def delete_department(id_department):
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).filter(Department.id == id_department).first()
    if departments and (departments.user.id == flask_login.current_user.id or flask_login.current_user.id == 1):
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/categories')
def show_categories():
    db_sess = db_session.create_session()
    categories = db_sess.query(Categories).all()
    return render_template('mars_categories.html', elements=categories, title="List of categories",
                           current_user=flask_login.current_user)


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        category = form.category.data
        search_matches = db_sess.query(Categories).filter(Categories.hazard_category == category).first()
        if search_matches:
            return render_template('mars_add_category.html', form=form, title='Adding category',
                                   message='Category already exists')
        categories = Categories()
        categories.hazard_category = category
        db_sess.add(categories)
        db_sess.commit()
        return redirect('/categories')
    return render_template('mars_add_category.html', form=form, title='Adding category')


@app.route('/edit_category/<int:id_category>', methods=['GET', 'POST'])
@login_required
def edit_category(id_category):
    form = CategoryForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        categories = db_sess.query(Categories).filter(Categories.id == id_category).first()
        if categories and flask_login.current_user.id == 1:
            form.category.data = categories.hazard_category
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        categories = db_sess.query(Categories).filter(Categories.id == id_category).first()
        if categories and flask_login.current_user.id == 1:
            categories.hazard_category = form.category.data
            db_sess.commit()
            return redirect('/categories')
        else:
            abort(404)
    return render_template("mars_add_category.html", form=form, title="Editing category")


@app.route('/delete_category/<int:id_category>', methods=['GET', 'POST'])
@login_required
def delete_category(id_category):
    if flask_login.current_user.id == 1:
        db_sess = db_session.create_session()
        categories = db_sess.query(Categories).filter(Categories.id == id_category).first()
        if categories:
            db_sess.delete(categories)
            db_sess.commit()
        else:
            abort(404)
    else:
        abort(404)
    return redirect('/categories')


def main():
    db_session.global_init('db/mars_explorer.db')
    app.run()


if __name__ == '__main__':
    main()


'''
Added Categories + Interface for categories (add/delete/show)
WARNING: Categories and Jobs ARE NOT CONNECTED!!
WARNING: ADVANCED FIELDS ARE NOT ADDED TO JOB FORM!!
'''
