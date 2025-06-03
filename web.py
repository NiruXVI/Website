from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.Date, nullable=False) 
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(120), nullable=False)  
    image = db.Column(db.String(200), nullable=True)     


with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            return 'Username already exists!'
        image = request.files.get('image')
        image_path = ''
        if image and image.filename:
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)
            image_path = image_path.replace('\\', '/')

        birthday_str = request.form['birthday']
        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            return 'Invalid birthday format! Please use YYYY-MM-DD.'
        user = User(
            username=username,
            name=request.form['name'],
            birthday=birthday,
            address=request.form['address'],
            password=request.form['password'],
            image=image_path
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('profile'))
        return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('login'))

    user_dict = {
        'name': user.name,
        'birthday': user.birthday.strftime('%Y-%m-%d') if user.birthday else '',
        'address': user.address,
        'image': user.image
    }
    return render_template('profile.html', user=user_dict)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)