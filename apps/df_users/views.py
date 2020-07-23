import random
import uuid

from flask import Blueprint, render_template, request, jsonify, json, Response, redirect, url_for, session

from apps.df_users.models import User
from common.aliyun_yzm import sendsms
from common.check_login import check_login
from common.img_code import return_img_code
from config.exts import db

user = Blueprint('user', __name__)

# 用户注册


@user.route('/user/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    else:
        # 获取用户填写的表单信息
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        mobile = request.form.get('mobile')
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        print(username, password, re_password, mobile, real_name, id_card)
        # 判断用户输入的密码
        if password == re_password:
            user1 = User.query.filter_by(name=username).first()
            if user1:
                data = {
                    "msg": '用户名已存在'
                }
                return jsonify(data)
            else:
                user = User()
                user.name = username
                # 传递的用户密码加密
                user.password = password
                user.mobile = mobile
                user.real_name = real_name
                user.id_card = id_card

                # 数据库实现添加
                db.session.add(user)
                db.session.commit()

                return jsonify(200)

# 用户登录


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    # 实现判读用户是否登录以及跳转
    next_url = ''
    try:
        next_url = request.full_path.split('?next_url=')[1]
    except Exception as e:
        print(e)
    if request.method == 'GET':
        return render_template('user/login.html', next_url=next_url)
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(name=username).first()
        if user:
            # 验证用户密码
            if user.verify_password(password):
                # 生成token存到cookie中
                token = str(uuid.uuid4())
                # 将user.id 添加到session中
                session[token] = user.id
                if len(next_url) == 0:
                    response = redirect(url_for('goods.index'))
                    # 向页面添加cookie
                    response.set_cookie('token', token)
                    return response
                else:
                    print(next_url)
                    response = redirect(next_url)
                    response.set_cookie('token', token)
                    return response
            else:
                return render_template('user/login.html', msg='用户名或密码错误')

#用户退出


@user.route('/user/logout', methods=["GET"])
def lg():
    cookie = request.cookies.get('token')

    session.pop(cookie)

    return redirect(url_for('goods.index'))

#获取图片验证码


@user.route('/user/get_img_code', methods=['GET'])
def get_img_code():
    img_path, num = return_img_code()
    data = {
        'img_path': img_path.split('.')[1] + '.png',
        'num': num
    }
    return jsonify(data)

# 获取手机验证码


@user.route('/user/get_phone_code', methods=['GET'])
def get_phone_code():
    username = request.args.get('username')
    phone = request.args.get('phone')
    user = User.query.filter_by(name=username).first()
    if user:
        if user.mobile == phone:
            code = dict()
            code['code'] = str(random.randint(100000, 999999))
            if phone:
                # sendsms(phone, code)

                data = {
                    'status': 200,
                    'code': code['code']
                }
                return jsonify(data)
        else:
            data = {
                'status': 402,
                'msg': '请使用注册的手机号获取验证码'
            }
            return jsonify(data)

# 用户的个人信息


@user.route('/user/user_info/', methods=['GET'])
def user_info():
    token = request.cookies.get('token')
    user_id = session.get(token)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        return render_template('user/user_info.html', user=user)
    else:
        next_url = request.path
        return redirect('/user/login?next_url=' + next_url)

# 用户地址


@user.route('/user/user_addr/', methods=["GET"])
def user_addr():
    if request.method == "GET":
        token = request.cookies.get('token')
        user_id = session.get(token)
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return render_template('user/user_addr.html', user=user)


@user.route('/user/add_addr', methods=['GET', 'POST'])
def add_addr():
    if request.method == 'POST':
        token = request.cookies.get('token')
        user_id = session.get(token)

        user = User.query.filter_by(id=user_id).first()

        addr = request.form.get('addr')

        user.addr = addr

        db.session.add(user)

        db.session.commit()

        return redirect(url_for('user.user_addr'))