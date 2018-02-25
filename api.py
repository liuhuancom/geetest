# from flask import Flask
from app import app,cache
from app.models import db,User

from flask import abort, request, jsonify, g, url_for
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
api = Api(app)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/')
def home():
    return 'hello'

@app.route('/users', methods=['POST'])
def new_user():
    """
    注册用户
    >>> http POST http://127.0.0.1:5000/users username=liuhuan password=liuhuan
    {"username": "liuhuan"}
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # todo 参数
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # todo 用户已经存在
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/login')
@auth.login_required
def pass_or_token_login():
    """
    用户登录
    >>> http -a liuhuan:liuhuan  http://127.0.0.1:5000/login
    {"msg": "Hello, liuhuan!"}
    """
    return jsonify({'msg': 'Hello, %s!' % g.user.username})


@app.route('/get_token')
@auth.login_required
def get_auth_token():
    """
    api获取token 缓存
    >>> http -a liuhuan:liuhuan  http://127.0.0.1:5000/get_token
    {
    "duration": 259200,
    "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxOTUyOTk0OSwiZXhwIjoxNTE5Nzg5MTQ5fQ.eyJpZCI6NX0.VcRL_WGtefmTheU9AM7VZ5KRqrlgKgO1vXqzPswdX-Q"
    }

    """
    username = request.authorization.get('username',None)
    cache_user_key = 'user_token_%s' % username
    cache_token = cache.get(cache_user_key)
    if cache_token is None:
        token = g.user.generate_auth_token(app.config['cache_time'])
        cache_token = token.decode('ascii')
        cache.set(cache_user_key,cache_token,timeout=app.config['cache_time'])
    return jsonify({'token': cache_token, 'duration': app.config['cache_time']})


@app.route('/get_user')
@auth.login_required
def get_user():
    """
    获取用户信息接口
    >>> http -a liuhuan:liuhuan http://127.0.0.1:5000/get_user
    {"email": "liuhuan@qq.com"}
    """
    return jsonify({'email': g.user.email})


@app.route('/change_email', methods=['POST'])
@auth.login_required
def change_email():
    """
    修改用户登录信息接口
    >>> http -a liuhuan:liuhuan POST http://127.0.0.1:5000/change_email email=liuhuan1@qq.com
    {
    "email": "111121@q.com",
    "msg": "ok"
    }
    """
    email = request.json.get('email',None)
    g.user.email = email
    g.user.save()
    return jsonify({'msg':'ok','email':email})


@app.route('/logout')
@auth.login_required
def logout():
    """
    退出登录接口
    >>> http -a liuhuan:liuhuan  http://127.0.0.1:5000/logout
    >>> http -a access_token:x http://127.0.0.1:5000/logout
    {"msg": "logout"}
    """
    g.user.logout()
    return jsonify({'msg':'logout'})


if __name__ == '__main__':
    app.debug = True
    app.run()
