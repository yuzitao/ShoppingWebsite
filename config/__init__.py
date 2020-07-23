from flask import Flask
from flask_admin import Admin

from config.exts import init_ext
from config.urls import init_url
from apps.df_cart.models import ShopCart
from apps.df_goods.models import Goods, Comment, Category
from apps.df_users.models import User
from apps.df_order.models import *


def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config['SECRET_KEY'] = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/shopping_website'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    # init_admin(app)
    init_ext(app)

    init_url(app)

    return app
