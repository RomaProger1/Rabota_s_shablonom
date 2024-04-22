from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

@app.route('/user/sign_up/', methods=['GET', 'POST'])
def user_sign_up():
    if request.method == 'POST':
        # Обработка POST-запроса на регистрацию пользователя
        data = request.json
        new_user = User(login=data['login'], password=data['password'], name=data['name'], age=data['age'], height=data['height'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id}), 201
    else:
        # Отображение формы регистрации пользователя
        return render_template('sign_up.html')

@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'login': user.login, 'name': user.name, 'age': user.age, 'height': user.height} for user in users])

@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(login=data['login'], password=data['password']).first()
        if user:
            return redirect(url_for('user_info', user_id=user.id))
        else:
            return 'User not found', 404
    return render_template('sign_in.html')

@app.route('/user/<int:user_id>/', methods=['GET'])
def user_info(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('user_info.html', user=user)
    else:
        return 'User not found', 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)