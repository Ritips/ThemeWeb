import flask_login
import data.users_resource
from data import db_session, jobs_api, users_api
import datetime
from data.mars_user import User
from data.mars_jobs import Jobs
from data.mars_departments import Department
from flask import Flask, render_template
from forms.mars_user import RegisterMarsForm
from flask import request, make_response, session, redirect, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.mars_loginform import LoginForm
from forms.mars_job import JobForm
from forms.mars_department import DepartmentForm
from forms.mars_categoriesform import CategoryForm
from data.mars_categories import Categories
from flask_restful import Api
import requests
import os


app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = 'yandex_lyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


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
        params = {
            "name": form.name.data, "surname": form.surname.data, "age": form.age.data,
            "position": form.position.data, "speciality": form.speciality.data, "address": form.address.data,
            "email": form.email.data, "city_from": form.city_from.data, "password": form.password.data
        }
        response = requests.post('http://127.0.0.1:5000/api/v2/users', params=params)
        if not response:
            return render_template('mars_register.html', form=form,
                                   title="Registration", message=response.json()["message"])
        return redirect('/')
    return render_template("mars_register.html", form=form, title="Registration")


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


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.route('/users_show/<int:user_id>')
@login_required
def show_city_from(user_id):
    user_info = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}').json()
    try:
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": user_info["users"]["city_from"],
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            return response, response.url
        json_object = response.json()
        toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        point = toponym["Point"]["pos"].split()
        envelope = toponym["boundedBy"]["Envelope"]
        lower_corner = tuple(map(float, envelope["lowerCorner"].split()))
        upper_corner = tuple(map(float, envelope["upperCorner"].split()))
        spn = (abs(lower_corner[0] - upper_corner[0]), abs(lower_corner[1] - upper_corner[1]))
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll": f"{point[0]},{point[1]}",
            "spn": f"{spn[0]},{spn[1]}",
            "l": 'sat',
        }
        map_response = requests.get(map_api_server, params=map_params)
        if not map_response:
            return map_response, map_response.url
        path = os.path.join('static/img', 'map_file.png')
        with open(path, 'wb') as f:
            f.write(map_response.content)
        return render_template("show_native_city.html", title="Hometown", info_user=user_info["users"])
    except KeyError:
        return user_info


def main():
    db_session.global_init('db/mars_explorer.sqlite')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(data.users_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(data.users_resource.UserListResource, '/api/v2/users')
    app.run()


if __name__ == '__main__':
    main()
