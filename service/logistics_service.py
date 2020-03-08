import json

from dao.logistics_dao import LogisticsDao
from dao.user_dao import UserDao
from model.logistics import Logistics
from model.user import User
from datetime import datetime
from config.db import db


class LogisticsService(object):
    """
    物流服务
    """

    def get_logistics_by_phone_and_order_number(self, order_number):
        """
        根据寄件人电话号或订单号查询物流信息，优先根据订单号查询
        :param send_telephone:
        :param order_number:
        :return:
        """
        if len(order_number) > 11:  # 电话号一般是11位, 大于11是订单编号
            logistics = LogisticsDao.query_logistic_by_order_number(order_number)
            logistics = [logistics]
        else:
            logistics = LogisticsDao.query_logistic_by_send_telephone(order_number)
        res = []
        for item in logistics:
            res.append({
                'order_number': item.order_number,
                'contents': json.loads(item.contents).get('data') if json.loads(item.contents).get('data') else []
            })
        return res

    def get_all_logistics(self, user_id):
        manager_user = UserDao.get_user_by_user_id(user_id)
        if manager_user.identity_type != User.IdentityType.MANAGER:
            raise Exception('你没有权限操作')
        logistics_infos = LogisticsDao.query_all_logistics()
        res = []
        for logistics_info in logistics_infos:
            res.append({
                'order_number': logistics_info.order_number,
                'send_name': logistics_info.send_name,
                'contents': json.loads(logistics_info.contents).get('data') if json.loads(logistics_info.contents).get('data') else [],
                'status': Logistics.Status.__label__.get(logistics_info.status)
            })
        return res

    def make_employee_to_deliver(self, user_id, employee_name, order_number):
        manager_user = UserDao.get_user_by_user_id(user_id)
        if manager_user.identity_type != User.IdentityType.MANAGER:
            raise Exception('你没有权限操作')
        employee = UserDao.get_deliver_by_real_name(employee_name)
        if not employee:
            raise Exception('不存在该姓名的快递员')
        # 进行指派
        logistics = LogisticsDao.query_logistic_by_logistic_order_number(order_number)
        if not logistics:
            raise Exception('不存在该物流信息')
        if logistics.status != Logistics.Status.ARRAY_SITE:
            raise Exception('该订单不满足配送条件')
        try:
            # 修改状态
            logistics.status = Logistics.Status.DELIVERING
            contents = json.loads(logistics.contents).get('data')
            contents.append({
                'content': datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '包裹正在配送中, 配送员:%s, 联系电话:%s' %
                           (employee.real_name, employee.telephone)
                })
            logistics.contents = json.dumps({
                'data': contents
            })
            logistics.user_id = employee.id
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception('指派过程出现异常, 错误信息:%s' % str(e))




