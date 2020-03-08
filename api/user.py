from flask import Blueprint, request, make_response
from wtforms import Form, StringField, validators

from service.user_service import UserService
from utils.common_utils import validate_form
from utils.resp_utils import ResponseUtil

user = Blueprint('user', __name__)

user_service = UserService()


@user.route('/login', methods=['GET'])
def login():
    """
    登陆接口
    @:param username, password
    :return:
    """
    username = request.args.get('username')
    password = request.args.get('password')
    try:
        msg = user_service.user_login(username, password)
        resp = make_response('{"msg": "success", "code": 0, "data": null}')
        resp.set_cookie("login_token", msg, max_age=1 * 3600 * 24)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return resp


@user.route("/reg", methods=['POST'])
def register():
    """
    注册接口
    @:param
    {"username":"jiangsshipan","password":"19"}
    :return:
    """
    form = RegisterForm.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        user_service.user_register(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')


@user.route("/logout")
def logout():
    """
    用户注销
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        user_service.logout(user_id)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')


@user.route("/get")
def get_user_info():
    """
    获取当前登陆用户的信息
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        user_info = user_service.get_user_info(user_id)
    except Exception as e:
        return ResponseUtil.error_response(data={}, msg=str(e))
    return ResponseUtil.success_response(data=user_info, msg='success')

@user.route("/all")
def get_all_user_info():
    """
    得到所有用户信息
    status：查询普通用户/快递员
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    identity_type = request.args.get('identity_type')
    if not identity_type:
        return ResponseUtil.error_response('请填写查询类型')
    try:
        user_infos = user_service.get_all_user_infos(user_id, identity_type)
    except Exception as e:
        return ResponseUtil.error_response(data={}, msg=str(e))
    return ResponseUtil.success_response(data=user_infos, msg='success')

@user.route('/del')
def update_status():
    """
    删除用户
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    username = request.args.get('username')
    if not username:
        raise Exception('相关参数不能为空')
    try:
        user_service.delete_user(user_id, username)
    except Exception as e:
        return ResponseUtil.error_response(data={}, msg=str(e))
    return ResponseUtil.success_response(msg='success')

@user.route('/incr')
def user_incr():
    """
    用户身份变为快递员
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    username = request.args.get('username')
    if not username:
        raise Exception('相关参数不能为空')
    try:
        user_service.user_increase(user_id, username)
    except Exception as e:
        return ResponseUtil.error_response(data={}, msg=str(e))
    return ResponseUtil.success_response(msg='success')



class RegisterForm(Form):
    """
    自定义注册Form
    """
    username = StringField(u'用户名', [validators.Length(min=4, max=32), validators.required()])
    password = StringField(u'密码', [validators.Length(min=4, max=32), validators.required()])
    real_name = StringField(u'真实姓名', [validators.Length(min=1, max=5), validators.required()])
    telephone = StringField(u'联系电话', [validators.Length(min=4, max=32), validators.required()])

