import uuid
import requests
import json

from config.config import DISTANCE_COST
from dao.order_dao import OrderDao
from dao.user_dao import UserDao
from model.logistics import Logistics
from model.order import Order
from model.user import User
from utils.common_utils import Singleton
from datetime import datetime, timedelta
from geopy.distance import geodesic
from config.db import db


class OrderService(object):
    """
    快递单服务
    """

    __metaclass__ = Singleton

    def generate_order(self, order_info):
        """
        生成订单
        :return:
        """
        try:
            send_name = order_info.get('send_name')
            send_telephone = order_info.get('send_telephone')
            send_pos = order_info.get('send_pos')
            receive_name = order_info.get('receive_name')
            receive_telephone = order_info.get('receive_telephone')
            receive_pos = order_info.get('receive_pos')
            appoint_type = order_info.get('appoint_type', 0)
            appoint_time = order_info.get('appoint_time') if order_info.get('appoint_time') else (datetime.now() + timedelta(hours=1)) # 未填写, 默认一小时后
            goods_weight = order_info.get('goods_weight')
            if not isinstance(appoint_time, datetime):
                appoint_time = datetime.fromtimestamp(appoint_time / 1000) # 毫秒时间戳转换
            # 生成订单号
            order_number = ''.join(str(uuid.uuid4()).split('-'))
            order_cost = self.get_order_cost_by_pos(send_pos, receive_pos, goods_weight) * 100000  # 乘以10w 返回的时候除以10w
            order = Order()
            order.send_name = send_name
            order.send_telephone = send_telephone
            order.send_pos = send_pos
            order.receive_name = receive_name
            order.receive_telephone = receive_telephone
            order.receive_pos = receive_pos
            order.appoint_type = Order.AppointType.APPOINT if appoint_type else Order.AppointType.SELF_SEND
            order.appoint_time = appoint_time
            order.goods_weight = goods_weight
            order.order_number = order_number
            order.order_cost = order_cost
            db.session.add(order)
            db.session.flush()
            # 新增一条物流信息
            logistics = Logistics()
            logistics.order_id = order.id
            # 出库信息
            info = [{
                'content': '%s 包裹正在等待揽收' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }]
            logistics.contents = json.dumps({'data': info})
            db.session.add(logistics)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_order_cost_by_pos(self, send_pos, receive_pos, weight):
        """
        根据寄件方, 收件方地址 和 物品重量计算价格
        :param send_pos:
        :param receive_pos:
        :param weight:
        :return:
        """
        try:
            # 获取地区经纬度url
            url = 'https://apis.map.qq.com/jsapi?qt=poi&wd=%s&pn=0&rn=10&rich_source=qipao&rich=web&nj=0&c=1&key=FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS&output=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb2.search_service_0'
            send_pos_url = url % send_pos
            receive_pos_url = url % receive_pos
            send_res = self.send_get_request(send_pos_url)
            receive_res = self.send_get_request(receive_pos_url)
            send_posx, send_posy = self.parse_response(send_res)  # 经度, 纬度
            receive_posx, receive_posy = self.parse_response(receive_res)
            # 计算距离, 经度0-180 纬度0-90
            distance = str(geodesic((send_posy, send_posx), (receive_posy, receive_posx)))
            # 取小数点前的数字
            pos = distance.find('.')
            aver_distance = int(distance[0: pos])  # 平均距离 km

            total_cost = 0  # 总运费 元
            # 计算距离价格
            distance_region = [k for k, _ in DISTANCE_COST.items()]  # 价格区间
            for i in range(len(distance_region) - 1):
                if aver_distance > distance_region[i] and aver_distance <= distance_region[i + 1]:
                    total_cost = DISTANCE_COST[distance_region[i]]
                    break
                if i == len(distance_region) - 2:
                    total_cost = DISTANCE_COST[distance_region[i + 1]]
            # 计算重量价格, 超过10kg, 每kg +5元
            if weight < 10:
                total_cost += 10
            else:
                total_cost += (weight - 10) * 5
            return total_cost
        except Exception:
            raise Exception('寄收件地址不合规, 无法获取金额信息, 请重新输入')

    def send_get_request(self, url):
        """
        发送get请求
        :param url:
        :return:
        """
        response = requests.get(url)
        if response and response.status_code != 200:
            raise Exception('调经纬度查询接口失败, 错误信息:%s' % response.reason)
        return response.text

    def parse_response(self, text):
        """
        获取response返回的经纬度结果
        :return:
        """
        try:
            start_pos = text.find('(')
            body = text[start_pos + 1: -1].strip()
            pos_info = json.loads(body)
            pos_detail = pos_info['detail'].get('pois')[0]
            return pos_detail['pointx'], pos_detail['pointy']
        except Exception as e:
            raise e

    def get_all_orders(self, user_id):
        manager_user = UserDao.get_user_by_user_id(user_id)
        if manager_user.identity_type != User.IdentityType.MANAGER:
            raise Exception('你没有权限操作')
        order_infos = OrderDao.get_all_orders()
        res = []
        for order_info in order_infos:
            res.append({
                'send_name': order_info.send_name,
                'send_telephone': order_info.send_telephone,
                'send_pos': order_info.send_pos,
                'order_cost': order_info.order_cost,
                'create_time': order_info.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': '完成' if order_info.status == Order.Status.COMPLETE else '未完成'
            })
        res.sort(key=lambda x: x['create_time'], reverse=True)
        return res


if __name__ == '__main__':
    OrderService().get_order_cost_by_pos('陕西省西安市三桥枫桥名邸', '陕西省西安市西安邮电大学长安校区东区', 25.5)
