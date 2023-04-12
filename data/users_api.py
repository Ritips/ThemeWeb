import datetime
import flask
from . import db_session
from .mars_user import User
from flask import jsonify, request


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder="templates"
)


@blueprint.route('/api/users', methods=['GET'])
def get_all_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email', 'city_from'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:id_user>', methods=['GET'])
def get_user(id_user):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id_user).first()
    if not users:
        return jsonify({"Error": "Not found"})
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'surname', 'name', 'age',
                                         'position', 'speciality', 'address', 'email', 'city_from'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({"Error": "No params"})
    elif not all(key in request.json for key in ('id', 'surname', 'name', 'age',
                                                 'position', 'speciality', 'address', 'email',
                                                 'password', 'city_from')):
        return jsonify({"Error": "Bad request"})
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == request.json["id"]).first()
    if users:
        return jsonify({"Error": "User already exists"})
    users = db_sess.query(User).filter(User.email == request.json["email"]).first()
    if users:
        return jsonify({"Error": "Email is already used"})
    users = User()
    users.id = request.json["id"]
    users.set_information(name=request.json["name"], surname=request.json["surname"], age=request.json["age"],
                          position=request.json["position"], speciality=request.json["speciality"],
                          address=request.json["address"], email=request.json["email"],
                          modified_date=datetime.datetime.now())
    users.city_from = request.json["city_from"]
    users.set_password(request.json["password"])
    db_sess.add(users)
    db_sess.commit()
    return jsonify({"success": "OK"})


@blueprint.route('/api/users/<int:id_user>', methods=["PUT"])
def edit_user(id_user):
    if not request.json:
        return jsonify({"Error": "No params"})
    elif not all(key in request.json for key in ('id', 'surname', 'name', 'age', 'position', 'speciality',
                                                 'address', 'email', 'password', 'city_from')):
        return jsonify({"Error": "Bad request"})
    db_sess = db_session.create_session()
    user_to_edit = db_sess.query(User).filter(User.id == id_user).first()
    if not user_to_edit:
        return jsonify({"Error": "Not found"})
    if db_sess.query(User).filter(User.email == request.json["email"], User.id != request.json["id"]).first():
        return jsonify({"Error": "Email is already used"})
    user_to_edit.id = request.json["id"]
    user_to_edit.name = request.json["name"]
    user_to_edit.surname = request.json["surname"]
    user_to_edit.age = request.json["age"]
    user_to_edit.position = request.json["position"]
    user_to_edit.speciality = request.json["speciality"]
    user_to_edit.address = request.json["address"]
    user_to_edit.email = request.json["email"]
    user_to_edit.set_password(request.json["password"])
    user_to_edit.city_from = request.json["city_from"]
    db_sess.commit()
    return jsonify({"success": "OK"})


@blueprint.route('/api/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    db_sess = db_session.create_session()
    user_to_delete = db_sess.query(User).filter(User.id == id_user).first()
    if not user_to_delete:
        return jsonify({"Error": "Not Found"})
    db_sess.delete(user_to_delete)
    db_sess.commit()
    return jsonify({"success": "OK"})
