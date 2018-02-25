from app import app
from passlib.apps import custom_app_context as pwd_context

from flask_sqlalchemy import SQLAlchemy

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/geetest'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))
    access_token = db.Column(db.String(122))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=3*24*24):
        # 3天
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        res = s.dumps({'id': self.id})
        self.access_token = res.decode('ascii')
        self.save()
        # return s.dumps({'id': self.id})
        return res

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        if user.access_token is None or user.access_token != token:
            return None
        return user

    def logout(self):
        self.access_token = None
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

