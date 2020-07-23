from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from config.exts import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    """用户"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    _password = db.Column('password', db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    addr = db.Column(db.String(255), nullable=True)  # 用户的收货地址
    real_name = db.Column(db.String(32))  # 真实姓名
    id_card = db.Column(db.String(18))  # 身份证号
    avatar_url = db.Column(db.String(128), default='/static/user/icon/default.jpg')  # 用户头像路径

    # 加入密码散列
    @property
    def password(self):
        # raise AttributeError('The current property is not readable')
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)  # 生成哈希值密码

    def verify_password(self, password):
        return check_password_hash(self._password, password)  # 检验哈希值是否一致
