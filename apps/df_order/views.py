import json
import time
import random
from io import StringIO
from datetime import datetime

import qrcode
from flask import Blueprint, render_template, jsonify, request, g, session, redirect, url_for
from sqlalchemy import and_, text

from apps.df_cart.models import ShopCart
from apps.df_goods.models import Goods
from apps.df_order.models import Order
from apps.df_users.models import User
from config.exts import db

order = Blueprint('order', __name__)


# 获取订单的信心


@order.route('/order/getOrderInfo', methods=['GET', 'POST'])
def get_order_info():
    if request.method == 'POST':
        data = request.form.get('aaa')
        cart_list = data.split(',')
        session['cart'] = cart_list
        return jsonify('200')


# 购物车立即付款获取购物车的内容


@order.route('/order/orderInfo', methods=['GET', 'POST'])
def order_info():
    token = request.cookies.get('token')
    user_id = session.get(token)
    user = User.query.filter_by(id=user_id).first()
    carts = []
    try:
        for cart_id in session.get('cart'):
            cart = ShopCart.query.filter_by(id=cart_id).first()
            carts.append(cart)
        context = {
            'carts': carts,
            'user': user
        }
        return render_template('order/order_info.html', **context)
    except:
        return redirect(url_for('cart.add_cart'))


# 支付订单


@order.route('/order/pay_order')
def pay_order():
    # 判断支付的订单数量1 or 多
    order_id = request.args.get('order_id', None)
    if order_id is None:
        url_path = request.full_path
        res = url_path.split('?')[1].split('&')[0:-1]
        num = 0
        for i in range(1, len(res) + 1):
            id = 'oid_' + str(i)
            print(id)
            oid = request.args.get(id)
            print(oid)
            order = Order.query.filter_by(id=oid).first()
            num += order.total_money
        context = {
            'num': num,
            'kw': url_path.split('?')[1],
            'status': 1
        }

        return render_template('order/pay_order.html', **context)
    else:
        order = Order.query.filter_by(id=order_id).first()
        context = {
            'num': order.total_money,
            'order_id': order_id,
            'status': 0
        }

        return render_template('order/pay_order.html', **context)


# 支付成功跳转的页面


@order.route('/order/pay_success')
def pay_success():
    order_id = request.args.get('order_id', None)
    if order_id is None:
        url_path = request.full_path
        res = url_path.split('?')[1].split('&')[0:-1]
        for i in range(1, len(res) + 1):
            id = 'oid_' + str(i)
            oid = request.args.get(id)

            order = Order.query.filter_by(id=oid).first()
            order.state = 1

            db.session.add(order)
            db.session.commit()
        return render_template('order/pay_success.html')
    else:
        order = Order.query.filter_by(id=order_id).first()

        order.state = 1

        db.session.add(order)
        db.session.commit()
        order_id_list = []
        return render_template('order/pay_success.html', order_id_list=order_id_list)


# 提交订单


@order.route('/order/submit_order', methods=['GET', 'POST'])
def submit_order():
    host = request.host
    order_id = request.args.get('order_id')
    print(order_id)
    # 从订单中心支付
    if order_id:
        order = Order.query.filter_by(id=order_id).first()
        # 生成二维码保存，返回到页面中
        url = 'http://' + host + '/order/pay_order?order_id=' + order_id
        print(url)
        img = qrcode.make(url)
        img.save('./static/pay_qrcode/pay.png')
        order_id_list = []
        context = {
            'num': order.total_money,
            'img_src': '/static/pay_qrcode/pay.png' + '?t=' + str(time.time()),
            'order_id': order_id,
            'order_id_list_len': len(order_id_list)
        }
        return render_template('order/pay_page.html', **context)
    else:
        # 从提交订单页面支付
        num = 0
        token = request.cookies.get('token')
        user_id = session.get(token)
        order_id_list = []
        print(session.get('cart'))
        for cart_id in session.get('cart'):
            cart = ShopCart.query.filter_by(id=cart_id).first()
            order_time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
            order = Order()

            order.count = cart.counts
            order.gid = cart.gid
            order.uid = user_id
            order.state = 0
            order.total_money = cart.counts * cart.goods.price
            order.ordertime = order_time

            db.session.add(order)
            db.session.commit()

            order_id = Order.query.filter(and_(Order.count == cart.counts, Order.gid == cart.gid, Order.uid == user_id,
                                               Order.ordertime == order_time)).first()

            order_id_list.append(order_id.id)
            goods = Goods.query.filter_by(id=cart.gid).first()
            goods.counts -= cart.counts

            db.session.add(goods)

            db.session.commit()

            db.session.delete(cart)

            db.session.commit()
        url = 'http://' + host + '/order/pay_order?'
        for i in range(1, len(order_id_list) + 1):
            url += 'oid_' + str(i) + '=' + str(order_id_list[i - 1]) + '&'

        img = qrcode.make(url)
        img.save('./static/pay_qrcode/pay.png')

        # session.pop('cart')
        context = {
            'num': order.total_money,
            'img_src': '/static/pay_qrcode/pay.png' + '?t=' + str(time.time()),
            'order_id': order_id,
            'order_id_list_len': len(order_id_list),
            'order_id_list': order_id_list
        }

        return render_template('order/pay_page.html', **context)


# 我的订单-全部订单


@order.route('/order/my_order/', methods=['GET', 'POST'])
def order_list():
    print(session.get('cart'))
    if request.method == 'GET':
        url_path = 'all'
        page = int(request.args.get('page', 1))
        token = request.cookies.get('token')
        user_id = session.get(token)
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            # 实现分页
            paginate = Order.query.filter_by(uid=user_id).order_by(text('-ordertime')).paginate(page, 4)
            orders = paginate.items

            context = {
                'user': user,
                'paginate': paginate,
                'orders': orders,
                'url_path': url_path
            }
            return render_template('user/order_list.html', **context)


# 待支付订单


@order.route('/order/wait_pay/')
def wait_pay():
    if request.method == 'GET':
        url_path = 'pay'
        page = int(request.args.get('page', 1))
        token = request.cookies.get('token')
        user_id = session.get(token)
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            paginate = Order.query.filter(and_(Order.uid == user_id, Order.state == 0)).order_by(
                text('-ordertime')).paginate(page, 4)
            orders = paginate.items

            context = {
                'user': user,
                'paginate': paginate,
                'orders': orders,
                'url_path': url_path
            }
            return render_template('user/order_list.html', **context)


# 待收货订单


@order.route('/order/wait_recevi/')
def wait_recevi():
    if request.method == 'GET':
        url_path = 'recevi'
        page = int(request.args.get('page', 1))
        token = request.cookies.get('token')
        user_id = session.get(token)
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            paginate = Order.query.filter(and_(Order.uid == user_id, Order.state == 1)).order_by(
                text('-ordertime')).paginate(page, 4)
            orders = paginate.items
            context = {
                'user': user,
                'paginate': paginate,
                'orders': orders,
                'url_path': url_path
            }
            return render_template('user/order_list.html', **context)


# 确认收货


@order.route('/order/sure', methods=['GET', 'POST'])
def sure_order():
    order_id = request.args.get('order_id')

    order = Order.query.filter_by(id=order_id).first()

    order.state = 2

    db.session.add(order)
    db.session.commit()

    return redirect(url_for('order.order_list'))


# 判断订单是否支付


@order.route('/order/judge_status')
def judge_status():
    order_id = request.args.get('order_id')

    order = Order.query.filter_by(id=order_id).first()
    print(order)
    if order.state == 1:
        return jsonify('200')
    else:
        return jsonify('201')
