from flask import url_for
from werkzeug.utils import redirect


def check_login(func):
    def login_fun(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            red = redirect(url_for('user.login'))
            red.set_cookie('url', request.get_full_path())
            # 保证用户再登陆验证之后仍点击到希望的页面
            return red
    return login_fun