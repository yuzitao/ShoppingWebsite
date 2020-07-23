from datetime import datetime

from apps.df_users.models import BaseModel
from config.exts import db


class Category(BaseModel, db.Model):
    """商品类别"""

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 商品类别编号
    cname = db.Column(db.String(255), nullable=False)  # 商品类别名称

    def category_json(self):
        category_json = {}
        category_json["id"] = self.id
        category_json["cname"] = self.cname

        return category_json


class Goods(BaseModel, db.Model):
    """商品"""

    __tablename__ = "goods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 房屋编号
    title = db.Column(db.String(128), nullable=False)  # 商品名称
    price = db.Column(db.Integer, default=0)  # 单价
    counts = db.Column(db.Integer, default=1)  # 商品数目
    is_sell = db.Column(db.Integer, default=1)  # 0销完 1在售
    date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 上架时间
    index_image_url = db.Column(db.String(256), default="")  # 主图片的路径
    # images = db.relationship("GoodsImage")  # 商品图片
    click_counts = db.Column(db.Integer, default=0)  # 被浏览次数
    cid = db.Column(db.Integer, db.ForeignKey("category.id", ondelete='cascade'))
    category = db.relationship("Category", backref=db.backref("goods", order_by=date.desc()))


class Comment(db.Model):
    '''商品评论'''

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    cdate = db.Column(db.DateTime, default=datetime.now)
    uid = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='cascade'))
    user = db.relationship("User", backref=db.backref('commments', order_by=cdate.desc()))
    # comment_parent = db.relationship("Comment", backref=db.backref("comments"), remote_side=[id])
    gid = db.Column(db.Integer, db.ForeignKey('goods.id'))
    goods = db.relationship("Goods", backref=db.backref('commments', order_by=cdate.desc()))
