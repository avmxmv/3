from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, \
    login_required, current_user
from flask_wtf import FlaskForm
from flask_restful import Api
from wtforms import IntegerField
from wtforms import SelectField, StringField, PasswordField, SubmitField, \
    TextAreaField, \
    BooleanField
from wtforms.validators import DataRequired
from data import db_session, items, users
from api_item import ItemListResource, ItemResource
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
db_session.global_init("db/blogs.sqlite")
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
number = 1


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    secondname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    gender = SelectField("Пол", validators=[DataRequired()],
                         choices=[('0', 'М'), ('1', "Ж")])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ItemsForm(FlaskForm):
    title = StringField('Название автомобиля', validators=[DataRequired()])
    content = TextAreaField('Информация')
    price = IntegerField('Цена руб')
    maxspeed = IntegerField('Максимальная скорость км/ч')
    boost = TextAreaField('Разгон до 100км/ч секунды')
    power = IntegerField('Мощность л.c.')
    powerdensity = IntegerField('Удельная мощность л.c./т')
    size = TextAreaField('Объём двигателя см³')
    weight = IntegerField('Вес автомобиля кг')
    submit = SubmitField('Добавить')


class EditItemsForm(FlaskForm):
    title = StringField('Название автомобиля', validators=[DataRequired()])
    content = TextAreaField('Информация')
    price = IntegerField('Цена руб')
    maxspeed = IntegerField('Максимальная скорость км/ч')
    boost = TextAreaField('Разгон до 100км/ч секунды')
    power = IntegerField('Мощность л.c.')
    powerdensity = IntegerField('Удельная мощность л.c./т')
    size = TextAreaField('Объём двигателя см³')
    weight = IntegerField('Вес автомобиля кг')
    submit = SubmitField('Изменить')


class PasswordForm(FlaskForm):
    password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new1_password = PasswordField('Повторите новый пароль',
                                  validators=[DataRequired()])
    submit = SubmitField('Сменить пароль')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/items', methods=['GET', 'POST'])
@login_required
def add_items():
    global number
    form = ItemsForm()
    if request.method == 'POST':
        f = request.files['file']
        f.save('static/images/' + str(number) + '.png')
        if form.validate_on_submit():
            sessions = db_session.create_session()
            item = items.Items()
            item.title = form.title.data
            item.content = form.content.data
            item.price = form.price.data
            item.maxspeed = form.maxspeed.data
            item.boost = form.boost.data
            item.power = form.power.data
            item.powerdensity = form.powerdensity.data
            item.size = form.size.data
            item.weight = form.weight.data
            item.photo = '/static/images/' + str(number) + '.png'
            number += 1
            sessions.add(item)
            sessions.commit()
            return redirect('/cars')
    return render_template('items.html', title='Добавление автомобиля',
                           form=form)


@app.route('/items_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def items_delete(id):
    sessions = db_session.create_session()
    item = sessions.query(items.Items).filter(items.Items.id == id).first()
    if item:
        sessions.delete(item)
        sessions.commit()
    else:
        abort(404)
    return redirect('/cars')


@app.route('/items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_items(id):
    form = EditItemsForm()
    if request.method == 'GET':
        sessions = db_session.create_session()
        item = sessions.query(items.Items).filter(items.Items.id == id).first()
        if item:
            form.title.data = item.title
            form.content.data = item.content
            form.price.data = item.price
            form.maxspeed.data = item.maxspeed
            form.boost.data = item.boost
            form.power.data = item.power
            form.powerdensity.data = item.powerdensity
            form.size.data = item.size
            form.weight.data = item.weight
        else:
            abort(404)
    if form.validate_on_submit():
        sessions = db_session.create_session()
        item = sessions.query(items.Items).filter(items.Items.id == id).first()
        if item:
            item.title = form.title.data
            item.content = form.content.data
            item.price = form.price.data
            item.maxspeed = form.maxspeed.data
            item.boost = form.boost.data
            item.power = form.power.data
            item.powerdensity = form.powerdensity.data
            item.size = form.size.data
            item.weight = form.weight.data
            sessions.commit()
            return redirect('/cars')
        else:
            abort(404)
    return render_template('edit.html', title='Редактирование автомобиля',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(
            users.User.email == form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/end")
def end():
    return render_template("end.html")


@app.route("/cars")
def index():
    sessions = db_session.create_session()
    item = sessions.query(items.Items)
    search = request.args.get('s', default="", type=str)
    if search:
        return render_template("index.html", items=item, search=search.lower())
    return render_template("index.html", items=item, search="")


@app.route('/info_cars/<int:id>', methods=['GET', 'POST'])
def info_cars(id):
    sessions = db_session.create_session()
    item = sessions.query(items.Items).get(id)
    return render_template("infocars.html", item=item)


@app.route('/buy/<int:id>', methods=['GET', 'POST'])
def buy(id):
    sessions = db_session.create_session()
    item = sessions.query(items.Items).get(id)
    try:
        if request.method == 'POST':
            number_card = request.form.get('card')
            result_card_number = alg_luna(number_card)
            cvv = request.form.get('cvv')
            username = request.form.get('name')
            month = request.form.get('month')
            year = request.form.get('year')
            if not (cvv or username or month or year):
                return render_template("buy.html", error='Некорректные данные',
                                       card_error='OK',
                                       item=item)
            if result_card_number != 'OK':
                return render_template('buy.html',
                                       card_error=result_card_number,
                                       error='OK',
                                       item=item)
            return redirect('/end')
        return render_template("buy.html", error='OK',
                               card_error='OK',
                               item=item)
    except Exception:
        return render_template("buy.html", error='Некорректные данные',
                               card_error='OK',
                               item=item)


def alg_luna(number_card):
    summ, summ2 = 0, 0
    number_card = ''.join(''.join(number_card.split()).split('-'))[::-1]
    if number_card.isdigit():
        for i in range(1, len(number_card) + 1):
            if i % 2 == 0:
                summ2 = int(number_card[i - 1]) * 2
                if summ2 > 9:
                    summ2 = summ2 % 10 + summ2 // 10
                summ += summ2
            else:
                summ += int(number_card[i - 1])
    if summ % 10 or len(number_card) != 16:
        return 'Номер карты введен некорректно'
    return 'OK'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        flag = password(form.password.data)
        if flag != 'OK':
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form, email_error="OK",
                                   nickname_error="OK",
                                   password_again_error="OK",
                                   password_error=flag, age_error='OK')
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, email_error="OK",
                                   nickname_error="OK",
                                   password_error="OK",
                                   password_again_error="Пароли не совпадают",
                                   age_error='OK')
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        if sessions.query(users.User).filter(
                users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, password_error="OK",
                                   nickname_error="OK",
                                   again_password_error="OK",
                                   email_error="Такой пользователь уже есть")
        if sessions.query(users.User).filter(
                users.User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, password_error="OK",
                                   password_again_error="OK",
                                   nickname_error="Данное имя пользователя "
                                                  "уже занято",
                                   email_error="OK", age_error='OK')
        if int(form.age.data) < 18:
            return render_template('register.html', title='Регистрация',
                                   form=form, password_error="OK",
                                   password_again_error="OK",
                                   email_error="OK", nickname_error="OK",
                                   age_error='Этот сайт предназначен для '
                                             'совершеннолетних лиц')
        if form.gender.data == '0':
            gender = "Мужской"
        else:
            gender = "Женский"
        user = users.User(
            nickname=form.nickname.data,
            name=form.name.data,
            secondname=form.secondname.data,
            email=form.email.data,
            password=form.password.data,
            age=form.age.data,
            gender=gender,
        )
        sessions.add(user)
        sessions.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация',
                           email_error="OK",
                           password_error="OK", nickname_error="OK",
                           age_error='OK',
                           password_again_error="OK", form=form)


def password(password):
    try:
        if len(password) < 8:
            raise LenEr
        f1 = 0
        f2 = 0
        for i in password:
            if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                f1 = 1
            if i.lower() in 'qwertyuiopasdfghjklzxcvbnm':
                f2 = 1
        if not f1:
            raise DigitEr
        if not f2:
            raise AlphabetEr
        return 'OK'
    except (LenEr, AlphabetEr, DigitEr) as e:
        return e.error


class LenEr(Exception):
    error = 'Длинна пароля должена быть более 7 символов!'


class AlphabetEr(Exception):
    error = 'В пароле должна быть хотя бы одна латинская буква!'


class DigitEr(Exception):
    error = 'В пароле должна быть хотя бы одна арабская цифра!'


@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    form = RegisterForm()
    return render_template('profil.html', title='Профиль',
                           form=form)


@app.route('/edit_profil', methods=['GET', 'POST'])
@login_required
def edit_profil():
    form = RegisterForm()
    db_session.global_init('db/blogs.sqlite')
    session = db_session.create_session()
    user = session.query(users.User).get(current_user.id)
    if request.method == 'GET':
        form.name.data = user.name
        form.secondname.data = user.secondname
        form.nickname.data = user.nickname
        form.age.data = user.age
        if user.gender == 'Мужской':
            gender = '0'
        else:
            gender = '1'
        form.gender.data = gender
    elif request.method == 'POST':
        user.name = form.name.data
        user.secondname = form.secondname.data
        form.nickname.data = user.nickname
        user.age = form.age.data
        if form.gender.data == '0':
            gender = "Мужской"
        else:
            gender = "Женский"
        user.gender = gender
        session.commit()
        return redirect('/profil')
    return render_template('edit_profil.html', form=form,
                           title='Редактирование')


@app.route('/password', methods=['GET', "POST"])
@login_required
def replace_password():
    form = PasswordForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.sqlite')
        session = db_session.create_session()
        user = session.query(users.User).get(current_user.id)
        if user.password != form.password.data:
            return render_template('password.html', form=form,
                                   password_error="Неверный пароль",
                                   new_password_error="OK",
                                   new1_password_error="OK")
        flag = password(form.new_password.data)
        if user.password == form.new_password.data:
            return render_template('password.html', form=form,
                                   password_error="OK",
                                   new_password_error="Новый пароль должен "
                                                      "отличаться от старого",
                                   new1_password_error="OK")
        if flag != 'OK':
            return render_template('password.html', form=form,
                                   password_error="OK",
                                   new_password_error=flag,
                                   new1_password_error="OK")
        if form.new_password.data != form.new1_password.data:
            return render_template('change_password.html', form=form,
                                   password_error="OK",
                                   new_password_error="OK",
                                   new1_password_error="Пароли не совпадают")
        user.password = form.new_password.data
        session.commit()
        return redirect('/profil')
    return render_template('password.html', form=form, title="Сменить пароль",
                           password_error="OK",
                           new_password_error="OK",
                           new1_password_error="OK")


def main():
    global number
    sessions = db_session.create_session()
    api.add_resource(ItemListResource, '/api/v2/item')
    api.add_resource(ItemResource, '/api/v2/item/<int:item_id>')
    number += len(list(sessions.query(items.Items)))
    app.run()


if __name__ == '__main__':
    main()
