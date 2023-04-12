from flask_restful import Resource, abort, reqparse
from flask import jsonify
from data import db_session
from data.mars_user import User
import datetime


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, location="args")
parser.add_argument('name', required=True, location="args")
parser.add_argument('age', required=True, type=int, location="args")
parser.add_argument('position', required=True, location="args")
parser.add_argument('speciality', required=True, location="args")
parser.add_argument('address', required=True, location="args")
parser.add_argument('email', required=True, location="args")
parser.add_argument('password', required=True, location="args")
parser.add_argument('city_from', required=True, location="args")


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


def abort_if_email_is_already_used(email):
    session = db_session.create_session()
    users = session.query(User).filter(User.email == email).first()
    if users:
        abort(409, message=f"Email: {email} is already used")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({"users": users.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality',
                                                     'address', 'email', 'city_from'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({"success": "OK"})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({"users": [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'city_from')) for item in users]})

    def post(self):
        args = parser.parse_args()
        abort_if_email_is_already_used(args["email"])
        session = db_session.create_session()
        users = User()
        users.set_information(name=args["name"], surname=args["name"], age=args["age"], position=args["position"],
                              speciality=args["speciality"], address=args["address"], email=args["email"],
                              modified_date=datetime.datetime.now())
        users.set_password(args["password"])
        users.city_from = args["city_from"]
        session.add(users)
        session.commit()
        return jsonify({"success": 'OK'})
