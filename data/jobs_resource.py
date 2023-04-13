from flask_restful import reqparse, Resource, abort
from flask import jsonify
from data import db_session
from data.mars_jobs import Jobs
import datetime


job_parser = reqparse.RequestParser()
job_parser.add_argument('team_leader', type=int, location="args", required=True)
job_parser.add_argument('job', location="args", required=True)
job_parser.add_argument('work_size', type=int, location="args", required=True)
job_parser.add_argument('collaborators', location="args", required=True)
job_parser.add_argument('start_date', location="args", required=True)
job_parser.add_argument('is_finished', type=bool, location="args", required=True)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Job {job_id} Not Found")


def abort_if_wrong_date(date_str):
    try:
        date_date, time_date = date_str.split()
        year, mon, day = map(int, date_date.split('-'))
        h, m, s = map(int, time_date.split(':'))
        normal_date = datetime.datetime(year=year, month=mon, day=day, hour=h, minute=m, second=s)
        return normal_date
    except ValueError:
        abort(400, message=f'Wrong date format. Format is "%Y-%m-%d %H:%M:%S"')
        return None


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        return jsonify({"jobs": jobs.to_dict(
            only=("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))
        })

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({"success": "OK"})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            "jobs": [item.to_dict(
                only=("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished")
            ) for item in jobs]
        })

    def post(self):
        args = job_parser.parse_args()
        abort_if_wrong_date(args["start_date"])
        date_date, time_date = args["start_date"].split()
        year, mon, day = map(int, date_date.split('-'))
        h, m, s = map(int, time_date.split(':'))
        start_date = datetime.datetime(year=year, month=mon, day=day, hour=h, minute=m, second=s)
        end_date = start_date + datetime.timedelta(hours=args["work_size"])
        jobs = Jobs()
        jobs.set_information(team_leader=args["team_leader"], job=args["job"], work_size=args["work_size"],
                             collaborators=args["collaborators"], start_date=start_date, end_date=end_date,
                             is_finished=args["is_finished"])
        session = db_session.create_session()
        session.add(jobs)
        session.commit()
        return jsonify({"success": "OK"})
