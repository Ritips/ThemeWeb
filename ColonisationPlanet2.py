from flask import url_for, Flask, render_template

app = Flask(__name__)


@app.route('/index/<title>/<prof>')
def first_sample(title, prof):
    param = dict()
    param["title"] = title
    param["prof"] = prof
    if prof == "physician":
        param["photo"] = url_for('static', filename=f'img/Mars.jpg')
    elif prof == "engineer":
        param["photo"] = url_for('static', filename=f'img/saved_image.jpg')
    return render_template('base.html', **param)




@app.route('/list_prof/<list_param>')
def list_prof(list_param):
    param = dict()
    param["profs"] = ["engineer", "physician"]
    param["title"] = ["Professions"]
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
