from flask import Flask, render_template, url_for, request, redirect
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.declarative as dec
import datetime
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import LoginManager

app = Flask(__name__)
engine = create_engine('sqlite:///users.db')
db = dec.declarative_base(app)


class User(db):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False, unique=False)
    email = sa.Column(sa.String, nullable=False, unique=False)
    password = sa.Column(sa.String, nullable=False, unique=False)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Users %r>' % self.id

def check(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False

db.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and  len(request.form['email']) > 4 \
                and len(request.form['password']) >= 8:
            email = request.form['email']
            name = request.form['name']
            hash = generate_password_hash(request.form['password'])
            user = User(name=name, password=hash, email=email)
            session.add(user)
            session.commit()
    else:
        return render_template('register.html')
    if request.method == 'GET':
        pass

if __name__ == '__main__':
    app.run(debug=True)