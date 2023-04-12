import datetime
import flask
from . import db_session
from .mars_jobs import Jobs
from flask import jsonify, request


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder="templates"
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            "jobs":
                [item.to_dict(only=('id', "job", "team_leader", "collaborators",
                                    "start_date", "work_size", "end_date", "is_finished"))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:id_job>')
def get_one_job(id_job):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    if not jobs:
        return jsonify({"error": "Not found"})
    return jsonify({
        "jobs": jobs.to_dict(only=('id', "job", 'team_leader', 'collaborators',
                                   'start_date', 'work_size', "end_date", 'is_finished'))
    })


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in
                 ("id", "job", 'team_leader', 'collaborators', 'start_date', 'work_size', "end_date", 'is_finished')):
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    if db_sess.query(Jobs).filter(Jobs.id == request.json["id"]).first():
        return jsonify({"error": "Id already exists"})
    jobs = Jobs()
    try:
        date_date, date_time = request.json["start_date"].split(' ')
        year, month, day = map(int, date_date.split('-'))
        hours, minutes, seconds = map(int, map(lambda x: x.split('.')[0], date_time.split(':')))
        start_date = datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)
        end_date = start_date + datetime.timedelta(hours=request.json["work_size"])
    except ValueError:
        return jsonify({"error": "Bad param"})
    except TypeError:
        return jsonify({"error": "Bad param"})
    jobs.set_information(team_leader=request.json["team_leader"], job=request.json["job"],
                         collaborators=request.json["collaborators"], start_date=start_date,
                         work_size=request.json["work_size"], is_finished=request.json["is_finished"],
                         end_date=end_date)
    jobs.id = request.json["id"]
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({"success": "OK"})


@blueprint.route('/api/jobs/<int:id_job>', methods=['DELETE'])
def delete_jobs(id_job):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    if not jobs:
        return jsonify({'error': "Not found"})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({"success": 'OK'})


@blueprint.route('/api/jobs/<int:id_job>', methods=['PUT'])
def edit_jobs(id_job):
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in
                 ("id", "job", 'team_leader', 'collaborators', 'start_date', 'work_size', "end_date", 'is_finished')):
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    if not jobs:
        return jsonify({"error": "Not found"})
    try:
        date_date, date_time = request.json["start_date"].split(' ')
        year, month, day = map(int, date_date.split('-'))
        hours, minutes, seconds = map(int, map(lambda x: x.split('.')[0], date_time.split(':')))
        start_date = datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)
        end_date = start_date + datetime.timedelta(hours=request.json["work_size"])
    except ValueError:
        return jsonify({"error": "Bad param"})
    except TypeError:
        return jsonify({"error": "Bad param"})
    jobs.set_information(team_leader=request.json["team_leader"], job=request.json["job"],
                         collaborators=request.json["collaborators"], start_date=start_date,
                         work_size=request.json["work_size"], is_finished=request.json["is_finished"],
                         end_date=end_date)
    jobs.id = request.json["id"]
    db_sess.commit()
    return jsonify({"success": "OK"})

