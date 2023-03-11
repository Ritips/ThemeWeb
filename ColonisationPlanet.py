from flask import Flask, url_for, request
import os

app = Flask(__name__)


@app.route('/')
def show_mission_name():
    return 'Миссия Колонизация Марса'


@app.route('/index')
def show_message():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion')
def promotion():
    phrases = [
        "Человечество вырастает из детства.",
        "Человечеству мала одна планета.",
        "Мы сделаем обитаемыми безжизненные пока планеты.",
        "И начнем с Марса!",
        "Присоединяйся!"
    ]
    return "<br>".join(phrases)


@app.route('/image_mars')
def show_image_mars():
    return f'''<!doctype html>
                <html lang='en'>
                    <head>
                        <meta charset="utf-8">
                        <title>Colonisation of Mars</title>
                    </head>
                    <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/Mars.jpg')}" 
                        alt="здесь должна была быть картинка, но не нашлась">
                        <div>Вот она какая, красная планета</div>
                    </body>
                </html>
            '''


@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <title>Promotion image</title>
                        <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    </head>
                    <body>
                        <h2>Жди нас, Марс!</h2>
                        <img src="{url_for('static', filename='img/Mars.jpg')}" 
                        alt="здесь должна была быть картинка, но не нашлась">
                        <div class="alert alert-dark" role="alert">
                            Человечество вырастает из детства.
                        </div>
                        <div class="alert alert-success" role="alert">
                            Человеству мала одна планета.
                        </div>
                        <div class="alert alert-secondary" role="alert">
                            Мы сделаем обитаемыми безжизненные пока планеты
                        </div>
                        <div class="alert alert-warning" role="alert">
                            И начнем с Марса!
                        </div>
                        <div class="alert alert-danger" role="alert">
                            Присоединяйся!
                        </div>
                    </body>
                </html>
            '''


@app.route('/astronaut_selection', methods=["POST", 'GET'])
def astronaut_selection():
    engineer = "инженер"
    pilot = "пилот"
    constructor = "строитель"
    exobiologist = "экзобиолог"
    physician = "врач"
    meteorologist = "метеоролог"
    climatologist = "Климатолог"
    profs = [engineer, pilot, constructor, exobiologist, physician, meteorologist, climatologist]
    if request.method == "GET":
        return f'''<!doctype html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <meta name="viewpoint" content="width=device-width, initial-scale=1.0">
                            <title>Astronaut selection</title>
                            <link rel="stylesheet"
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        </head>
                        <body>
                            <h3>Анкета претендента</h3>
                            <h3>на участие в миссии</h3>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                    <input type="text" class="form-control" name="surname" id="surname" placeholder="Введите фамилию">
                                    <input type="text" class="form-control" name="name" id="name" placeholder="Введите имя">
                                    <br><input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="classSelect">Какое у Вас образование?</label>
                                        <select class="form-control" id="education" name="education">
                                            <option>Начальное</option>
                                            <option>Среднее</option>
                                            <option>Высшее</option>
                                            <option>Послевузовское</option>
                                        </select>                                        
                                    </div>
                                    <br><p>Какие у вас есть профессии?</p>
                                    <input type="checkbox" name="{engineer}" id="{engineer}" checked> {engineer}
                                    <br><input type="checkbox" name="{pilot}" id="{pilot}" checked> {pilot}
                                    <br><input type="checkbox" name="{physician}" id="{physician}" checked> {physician}
                                    <br><input type="checkbox" name="{meteorologist}" id="{meteorologist}" checked> {meteorologist} 
                                    <br><input type="checkbox" name="{climatologist}" id="{climatologist}" checked> {climatologist}
                                    <br><input type="checkbox" name="{constructor}" id="{constructor}" checked> {constructor}
                                    <br><input type="checkbox" name="{exobiologist}" id="{exobiologist}" checked> {exobiologist}
                                    <br><p>Укажите пол</p>
                                    <input type="radio" name="sex" id="male" value="male"> Мужской
                                    <br><input type="radio" name="sex" id="female" value="female"> Женский
                                    <div class="form-group">
                                        <label for="about">Почему Вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label><br>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <br><input type="checkbox" name="acceptRules"> Готовы отправиться на Марс?<br>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                        </body>
                    </html>'''
    elif request.method == 'POST':
        keys1 = ["surname", "name", "education", "email"]
        keys2 = ["about", "sex", "acceptRules"]
        for key in keys1 + profs + keys2:
            print(f"{key}: {request.form[key]}")
        file = request.files["file"]
        print(file.read())
        return "Форма отправлена"


@app.route('/choice/<planet_name>')
def choice_planet(planet_name):
    planets = ["Меркурий", "Венера", "Земля", "Марс", "Юпитер", "Сатурн", "Уран", "Нептун", "Уран", "Нептун", "Плутон"]
    text = 'Неизвестный для меня объект'
    if planet_name in planets:
        if planet_name == "Земля":
            text = "Моя любимая планета!"
        elif planet_name == 'Плутон':
            text = "Крупнейшая карликовая планета Солнечной системы"
        else:
            text = "Эта планета находится в Солнечной Системе"
    return f'''<!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <meta name="viewpoint" content="width=device-width, initial-scale=1.0">
                        <title>Варианты выбора</title>
                        <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    </head>
                    <body>
                        <h1><b>Мое предложение: {planet_name}</b></h1>
                        <h2>{text}<h2>
                        <div class="alert alert-success" role="alert">{planet_name * 1}</div>
                        <div class="alert alert-dark" role="alert">{planet_name * 2}</div>
                        <div class="alert alert-warning" role="alert">{planet_name * 3}</div>
                        <div class="alert alert-danger" role="alert">{planet_name * 4}</div>
                    </body>
                </html>'''


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def selection_results(nickname, level, rating):
    return f'''<!doctype html>
                    <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <meta name="viewpoint" content="width=device-width, initial-scale=1.0">
                        <title>Варианты выбора</title>
                        <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    </head>
                    <body>
                        <h1><b>Результаты отбора</b></h1>
                        <p>Претендента на участие в миссии {nickname}</p>
                        <div class="alert alert-success">Поздравляем! Ваш рейтинг после {level} этапа отбора</div>
                        <p>составляет {rating}</p>
                        <div class="alert alert-warning">Желаем удачи!</div>
                    </body>
                </html>'''


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    image_show = 'saved_image.jpg'
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h3>Загрузка фотографии</h3>
                            <h3>для участия в миссии</h3>
                            <form method="post" class="login_form" enctype="multipart/form-data">
                                <div class="form-group">
                                     <label for="photo">Выберите файл</label>
                                     <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <br><img src="{url_for('static', filename=f'img/{image_show}')}"><br>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return 'Файл не был загружен'
        if f and ('.' in f.filename and f.filename.split('.')[-1] in ['txt', 'jpg', 'png', 'jpeg']):
            path = os.path.join("static/img", image_show)
            f.save(path)
            return 'Success'


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
