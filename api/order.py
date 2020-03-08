from flask import Blueprint, request
from wtforms import Form, StringField, validators, IntegerField, FloatField

from service.order_service import OrderService
from utils.resp_utils import ResponseUtil

from utils.common_utils import validate_form

order = Blueprint('order', __name__)

order_service = OrderService()


@order.route('/do', methods=['POST'])
def do_order():
    """
    下单接口
    @:param username, password
    :return:
    {"msg": "34e3f953ee814a66a62b2cc2c02b1968", "code": 0, "data": null}
    """
    form = DoOrderForm.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        order_service.generate_order(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')


@order.route('/cost')
def get_order_cost():
    """
    根据寄件人地址, 收件人地址, 物品重量获得价格
    :return:
    """
    form = GetOrderCost(request.args, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        send_pos, receive_pos, goods_weight = form.data.get('send_pos'), form.data.get('receive_pos'), \
                                              form.data.get('goods_weight')
        res = order_service.get_order_cost_by_pos(send_pos, receive_pos, float(goods_weight))
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success', data=res)


@order.route('/all')
def get_all_orders():
    """
    查询所有订单信息
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        res = order_service.get_all_orders(user_id)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success', data=res)



class DoOrderForm(Form):
    send_name = StringField(u'寄件人姓名', [validators.Length(min=1, max=50), validators.required()])
    send_telephone = StringField(u'寄件人电话', [validators.Length(min=1, max=20), validators.required()])
    send_pos = StringField(u'寄件人地址', [validators.Length(min=1, max=100), validators.required()])
    receive_name = StringField(u'收件人姓名', [validators.Length(min=1, max=50), validators.required()])
    receive_telephone = StringField(u'收件人电话', [validators.Length(min=1, max=20), validators.required()])
    receive_pos = StringField(u'收件人地址', [validators.Length(min=1, max=100), validators.required()])

    appoint_type = StringField(u'寄件类型', [validators.required()])
    appoint_time = IntegerField(u'预约时间')  # 非必填
    goods_weight = FloatField(u'物品重量', [validators.required()])


class GetOrderCost(Form):
    send_pos = StringField(u'寄件人地址', [validators.Length(min=1, max=100), validators.required()])
    receive_pos = StringField(u'收件人地址', [validators.Length(min=1, max=100), validators.required()])
    goods_weight = FloatField(u'物品重量', [validators.required()])
