from datetime import datetime

from config.exts import db


class Order(db.Model):
    """订单"""

    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_money = db.Column(db.Float)
    count = db.Column(db.Integer)  # 订单商品数量
    gid = db.Column(db.Integer, db.ForeignKey('goods.id'))  # 商品外键
    goods = db.relationship('Goods', backref=db.backref('orders'))
    ordertime = db.Column(db.DateTime, default=datetime.now)  # 订单创建时间
    state = db.Column(db.Integer, default=0)  # 0未支付，1送达中 2送达完毕
    uid = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='cascade'))
    user = db.relationship("User", backref=db.backref("orders", order_by=ordertime.desc()))
    order_last_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 订单支付时间
