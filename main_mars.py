from data import db_session
import datetime
from datetime import datetime as dt
from data.mars_user import User
from data.mars_jobs import Jobs


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


def task_add_captain_part1():
    crew = {"user_1": {
             "surname": "Scott", "name": "Ridley", "age": 21, "position": "captain", "speciality": "research_engineer",
             "address": "module_1", "email": "scott_chief@mars.org"
            },
            "user_2": {
                "surname": "Simona", "name": "Barlow", "age": 22, "position": "colonist", "speciality": "engineer",
                "address": "module_1", "email": "simona_colonist@mars.org"
            },
            "user_3": {
                "surname": "Samuel", "name": "Parsons", "age": 25, "position": "colonist", "speciality": "physician",
                "address": "module_1", "email": "samuel_colonist@mars.org"
            },
            "user_4": {
                "surname": "Dominic", "name": "Hansen", "age": 26, "position": "colonist", "speciality": "biologist",
                "address": "module_1", "email": "dominic_colonist@mars.org"
            }
            }
    return crew


def task_first_job_part1():
    dict_jobs = {"job_1": {
        "team_leader": 1, "job": "deployment of residential modules 1 and 2", "work_size": 15,
        "collaborators": "2, 3", "start_date": dt.now(), "is_finished": False
                           }}
    return dict_jobs


def task_add_captain_part2(db_sess):
    crew = task_add_captain_part1()
    for key in crew:
        person = crew[key]
        surname, name, age, position = person["surname"], person["name"], person["age"], person["position"]
        speciality, address, email = person["speciality"], person["address"], person["email"]
        add_person(db_sess, surname, name, age, position, speciality, address, email)


def task_first_job_part2(db_sess):
    dict_jobs = task_first_job_part1()
    for key in dict_jobs:
        el_job = dict_jobs[key]
        team_leader, job, work_size = el_job["team_leader"], el_job["job"], el_job["work_size"]
        collaborators, start_date, is_finished = el_job["collaborators"], el_job["start_date"], el_job["is_finished"]
        add_job(db_sess, team_leader=team_leader, description_job=job,
                work_size=work_size, start_date=start_date, is_finished=is_finished, collaborators=collaborators)


def main():
    db_session.global_init('mars_explorer.db')
    db_sess = db_session.create_session()
    task_add_captain_part2(db_sess)


if __name__ == '__main__':
    main()
