#### 面试题目

##### 使用

python3 环境
接口测试使用的是httpie

```bash

$ virtualenv geetest
$ source geetest/bin/activate
(geetest) $ pip install -r requirements.txt

# 先创建数据库
(venv) $ python createdb.py

# 运行
(venv) $ python api.py
* Running on http://127.0.0.1:5000/
```

nginx和Supervisor配置文件都在项目里面。


##### api接口

注册接口

```bash
>>> http POST http://127.0.0.1:5000/users username=liuhuan password=liuhuan
{"username": "liuhuan"}
```

用户密码登录
```bash
>>> http -a liuhuan:liuhuan  http://127.0.0.1:5000/login
{"msg": "Hello, liuhuan!"}
```

token登录
```bash
#获取token
>>> http -a liuhuan:liuhuan  http://127.0.0.1:5000/get_token
{
    "duration": 259200,
    "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxOTUyOTk0OSwiZXhwIjoxNTE5Nzg5MTQ5fQ.eyJpZCI6NX0.VcRL_WGtefmTheU9AM7VZ5KRqrlgKgO1vXqzPswdX-Q"
}
# 用token登录
>>> http -a eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxOTUyOTk0OSwiZXhwIjoxNTE5Nzg5MTQ5fQ.eyJpZCI6NX0.VcRL_WGtefmTheU9AM7VZ5KRqrlgKgO1vXqzPswdX-Q:x  http://127.0.0.1:5000/login
{"msg": "Hello, liuhuan!"}
```

获取登录用户信息接口

```bash
>>> http -a liuhuan:liuhuan http://127.0.0.1:5000/get_user
{"email": "liuhuan@qq.com"}
```

修改用户登录信息接口

```bash
>>> http -a liuhuan:liuhuan POST http://127.0.0.1:5000/change_email email=liuhuan1@qq.com
{
    "email": "111121@q.com",
    "msg": "ok"
}
```

退出登录接口

```bash
>>> http -a liuhuan:liuhuan  http://127.0.0.1:5000/logout
>>> http -a access_token:x http://127.0.0.1:5000/logout
{"msg": "logout"}
```

