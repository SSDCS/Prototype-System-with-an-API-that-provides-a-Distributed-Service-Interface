# application/user_api/routes.py
from . import bp
from .. import db, login_manager
from ..models import User
from flask import make_response, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from argon2 import PasswordHasher as ph


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None


@bp.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)
    return response

@bp.route('/api/user/create', methods=['POST'])
def post_register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']

    plain_password = str(request.form['password'])

    password = ph.hash(plain_password)

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.username = username
    user.authenticated = True

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User added', 'result': user.to_json()})

    return response


@bp.route('/api/user/login', methods=['POST'])
def post_login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        if ph.verify(str(request.form['password']), user.password):
            user.encode_api_key()
            db.session.commit()
            login_user(user)

            return make_response(jsonify({'message': 'Logged in', 'api_key': user.api_key}))

    return make_response(jsonify({'message': 'Not logged in'}), 401)


@bp.route('/api/user/logout', methods=['POST'])
def post_logout():
    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({'message': 'You are logged out'}))
    return make_response(jsonify({'message': 'You are not logged in'}))


@bp.route('/api/user/<username>/exists', methods=['GET'])
def get_username(username):
    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find username'}), 404
    return response


@login_required
@bp.route('/api/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        return make_response(jsonify({'result': current_user.to_json()}))

    return make_response(jsonify({'message': 'Not logged in'})), 401