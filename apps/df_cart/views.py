from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from sqlalchemy import and_

from apps.df_cart.models import ShopCart
from apps.df_goods.models import Goods
from config.exts import db

cart = Blueprint('cart', __name__)

# 添加购物车


@cart.route('/add_cart', methods=["GET", "POST"])
def add_cart():
    token = request.cookies.get('token')
    user_id = session.get(token)
    if user_id:
        if request.method == 'GET':
            carts = ShopCart.query.filter_by(uid=user_id).all()
            context = {
                'carts': carts
            }
            return render_template('cart/cart.html', **context)

        else:
            goods_id = request.form.get('goods_id')
            goods_num = request.form.get('goods_num')
            shopcart = ShopCart.query.filter(and_(ShopCart.uid==user_id, ShopCart.gid==goods_id)).first()
            if shopcart:
                goods = Goods.query.filter_by(id=goods_id).first()
                goods_count = goods.counts
                shopcart_goods_count = shopcart.counts
                all_count = int(goods_num) + int(shopcart_goods_count)
                if goods_count < all_count:  # 判断加入购物车的商品数量是否超过商品总量
                    data = {
                        'msg': '添加的商品超过当前库存数量'
                    }
                    return jsonify(data)
                # 不超过就向购物晨添加一条数据
                else:
                    shopcart.counts += int(goods_num)
                    db.session.add(shopcart)
                    db.session.commit()

                    data = {
                        'msg': '添加成功'
                    }

                    return jsonify(data)
            else:

                shopcart = ShopCart()
                shopcart.uid = user_id
                shopcart.gid = goods_id
                shopcart.counts = goods_num
                db.session.add(shopcart)

                db.session.commit()
                data = {
                    'msg': '添加购物车成功'
                }
                return jsonify(data)
    else:
        next_url = request.path
        return redirect('/user/login?next_url=' + next_url)

# 购物车删除商品


@cart.route('/delete/<cart_id>')
def delete_cart(cart_id):

    cart = ShopCart.query.filter_by(id=cart_id).first()

    db.session.delete(cart)

    db.session.commit()

    return redirect(url_for('cart.add_cart'))

# 购物车添加商品


@cart.route('/cart/add_goods')
def cart_add_goods():
    goods_id = request.args.get('goods_id')
    cart_id = request.args.get('cart_id')
    goods = Goods.query.filter_by(id=goods_id).first()
    cart = ShopCart.query.filter_by(id=cart_id).first()
    if goods.counts <= cart.counts:  # 判断每次添加的商品是否大于商品的总量
        data = {
            'status': 201,
            'msg': '添加的商品超过当前库存数量'
        }
        return jsonify(data)
    else:
        cart.counts += 1
        db.session.add(cart)
        db.session.commit()

        data = {
            'status': 200,
            'msg': '添加成功'
        }

        return jsonify(data)

# 购物车减少商品


@cart.route('/cart/reduce_goods')
def cart_reduce_goods():
    goods_id = request.args.get('goods_id')
    cart_id = request.args.get('cart_id')
    goods = Goods.query.filter_by(id=goods_id).first()
    cart = ShopCart.query.filter_by(id=cart_id).first()

    cart.counts -= 1

    db.session.add(cart)
    db.session.commit()

    data = {
        'status': 200,
        'msg': '修改成功'
    }

    return jsonify(data)