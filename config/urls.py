from apps.df_cart.views import cart
from apps.df_goods.views import goods
from apps.df_order.views import order
from apps.df_users.views import user


def init_url(app):
    # 蓝图注册
    app.register_blueprint(goods)
    app.register_blueprint(user)
    app.register_blueprint(cart)
    app.register_blueprint(order)