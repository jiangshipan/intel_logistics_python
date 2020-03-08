from flask import Blueprint, request
from service.logistics_service import LogisticsService
from utils.resp_utils import ResponseUtil


logistics = Blueprint('logistics', __name__)

logistics_service = LogisticsService()


@logistics.route('/get')
def get_logistics():
    """
    根据寄件人电话号/快递编号查询物流信息
    :return: 
    """
    order_number = request.args.get('order_number', '')
    if not order_number:
        return ResponseUtil.error_response(msg='寄件人电话号和订单号必填一项')
    try:
        res = logistics_service.get_logistics_by_phone_and_order_number(order_number)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(data=res, msg='success')

@logistics.route('/all')
def get_all_logistics():
    """
    得到所有物流信息
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        res = logistics_service.get_all_logistics(user_id)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success', data=res)

@logistics.route('/make')
def make_employee_to_deliver():
    """
    指派快递员去派件
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    employee_name = request.args.get('employee_name')
    order_number = request.args.get('order_number')
    if not employee_name or not order_number:
        return ResponseUtil.error_response(msg='相关参数不能为空')
    try:
        logistics_service.make_employee_to_deliver(user_id, employee_name, order_number)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')


