from datetime import datetime

from config.exts import db


class ShopCart(db.Model):
    """购物车"""

    __tablename__ = "shop_cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sdate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    counts = db.Column(db.Integer)  # 添加商品数量，不可大于库存总量
    # subTotal = db.Column(db.Float)  # 结算总金额
    uid = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='cascade'))
    user = db.relationship("User", backref=db.backref("shopcarts", order_by=sdate.desc()))
    gid = db.Column(db.Integer, db.ForeignKey('goods.id'))
    goods = db.relationship("Goods", backref=db.backref("shopcarts"))
