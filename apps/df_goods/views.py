from datetime import datetime

from flask import render_template, Blueprint, request, session, jsonify

from apps.df_goods.models import Goods, Comment
from apps.df_users.models import User

from config.exts import db

goods = Blueprint('goods', __name__)

# 用户首页显示商品


@goods.route('/')
def index():
    cookie = request.cookies.get('token')
    user_id = session.get(cookie)
    goods = Goods.query.all()
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        context = {
            'user': user,
            'goods': goods
        }
        return render_template('goods/index.html', **context)
    else:
        context = {
            'goods': goods
        }
        return render_template('goods/index.html', **context)

# 商品详情


@goods.route('/<good_id>/')
def good_datail(good_id):
    cookie = request.cookies.get('token')
    user_id = session.get(cookie)
    good = Goods.query.filter_by(id=good_id).first()
    comments = Comment.query.filter_by(gid=good_id).all()
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        context = {
            'goods': good,
            'comment_num': len(comments),
            'user': user,
            'comments': comments
        }
        return render_template('goods/good_detail.html', **context)
    else:
        context = {
            'goods': good,
            'comment_num': len(comments),
            'comments': comments,
            'user': None
        }
        return render_template('goods/good_detail.html', **context)

# 商品评论


@goods.route('/goods/comment', methods=['GET', 'POST'])
def goods_comment():
    token = request.cookies.get('token')
    user_id = session.get(token)
    if request.method == 'POST':
        comment_time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        content = request.form.get('content')
        gid = request.form.get('gid')

        comment = Comment()

        comment.content = content
        comment.uid = user_id
        comment.gid = gid
        comment.cdate = comment_time

        db.session.add(comment)
        db.session.commit()

        user_comment = Comment.query.filter_by(content=content).first()
        # user_comment = Comment.query.all()[0]
        data = {
            'status': 200,
            'username': user_comment.user.name,
            'img_url': user_comment.user.avatar_url,
            'content': user_comment.content,
            'comment_time': str(user_comment.cdate)
        }

        return jsonify(data)

# 商品浏览量


@goods.route('/goods/click_counts')
def goods_click_counts():
    goods_id = request.args.get('gid')
    goods = Goods.query.filter_by(id=goods_id).first()

    goods.click_counts += 1  # 商品详情页没刷新一次浏览量+1
    db.session.add(goods)
    db.session.commit()

    return jsonify('200')

# 检索商品-模糊查询


@goods.route('/search', methods=['GET'])
def search_goods():
    if request.method == 'GET':
        kw = request.args.get('kw')

        goods = Goods.query.filter(Goods.title.like("%" + kw + "%")).all()

        # return jsonify('200')
        return render_template('goods/search_show.html', goods=goods)