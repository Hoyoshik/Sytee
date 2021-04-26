from flask import Flask, render_template, url_for, request, redirect
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.declarative as dec
import datetime
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import LoginManager, UserMixin, login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine('sqlite:///users.db')
engine2 = create_engine('sqlite:///posts.db')
db = dec.declarative_base(app)
db_posts = dec.declarative_base(app)

class Posts(db_posts):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    intro = sa.Column(sa.String(300), nullable=False)
    text = sa.Column(sa.Text, nullable=False)

    def repr(self):
        return '<Posts %r>' % self.title

class User(db, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), nullable=False, unique=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String(255), nullable=False)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<User {}>'.format(self.username)

def check(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False

db.metadata.create_all(engine)
db_posts.metadata.create_all(engine2)
Session = sessionmaker(bind=engine)
session = Session()

Session2 = sessionmaker(bind=engine2)
session2 = Session2()

@app.route('/')
def showSignUp():
    return render_template('first.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    message = ''
    if request.method == 'POST':
        if len(request.form['name']) > 4 and  len(request.form['email']) > 4 \
                and len(request.form['password']) >= 8:
            email = request.form['email']
            name = request.form['name']
            hash = generate_password_hash(request.form['password'])
            user = User(name=name, password=hash, email=email)
            new_user = session.query(User).filter(User.email == email).first()
            session.commit()
            if new_user:  # если пользователь уже есть
                message = 'пользователь занят'
                return redirect(url_for('register', message=message))
            session.add(user)
            session.commit()
            return redirect(url_for('login'))
        else:
            message = 'неверный формат данных'
            return redirect(url_for('register'))
    return render_template('regist.html', message=message)

@app.route('/main')
def showSignUpi():
    return render_template('index.html')

@app.route('/characters')
def characters():
    return render_template('Hero.html')


@app.route('/grobovshik')
def Grob():
    return render_template('Grob.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST':
        global user
        login = request.form['login']
        password = request.form['password']
        user = session.query(User).filter(User.name == login).first()
        session.commit()
        if user == None:
            message = 'пользователь не найден'
            return redirect(url_for('login', message=message))
        if check_password_hash(user.password, password):
            return redirect(url_for('showSignUpi'))
        message = 'неверный пароль'
        session.commit()
        return redirect(url_for('login', message=message))
    return render_template('login.html', message=message)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    pass

@app.route('/news')
def News():
    return render_template('new.html')

@app.route('/newpost', methods=['post', 'get'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        intro = request.form['intro']
        print(title, text, intro)
        new_post = Posts(title=title, text=text, intro=intro)
        session2.commit()
        session2.add(new_post)
        session2.commit()
    return render_template('newpost.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    global user
    return render_template('profile.html', user=user)


@app.route('/posts', methods=['POST', 'GET'])
def posts():
    session2.commit()
    posts = session2.query(Posts).all()
    return render_template('otziv.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)