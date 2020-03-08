import json
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from dao.logistics_dao import LogisticsDao
from dao.order_dao import OrderDao
from model.logistics import Logistics
from model.order import Order
from config.db import db

"""
修改物流状态脚本
"""


def update_logistic_status():
    """
    修改物流状态
    :return:
    """
    logistics_list = LogisticsDao.get_all_doing_logistics()
    try:
        for logistics in logistics_list:
            print('当前正在执行的物流id是:%s' % logistics.id)
            contents = json.loads(logistics.contents).get('data')
            if logistics.status == Logistics.Status.OUT_OF_STOCK:
                # 出库
                contents.append({
                    'content': datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '包裹正在运输中'
                })
                logistics.contents = json.dumps({
                    'data': contents
                })
                logistics.status = Logistics.Status.TRANSPORTING
            elif logistics.status == Logistics.Status.TRANSPORTING:
                # 运输中
                contents.append({
                    'content': datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '包裹正在等待配送'
                })
                logistics.contents = json.dumps({
                    'data': contents
                })
                logistics.status = Logistics.Status.ARRAY_SITE
            elif logistics.status == Logistics.Status.DELIVERING:
                # 配送中
                contents.append({
                    'content': datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '包裹配送完成, 感谢您的信任。'
                })
                logistics.contents = json.dumps({
                    'data': contents
                })
                logistics.status = Logistics.Status.DELIVERED
                # 订单状态修改为完成
                order = OrderDao.get_order_by_order_number(logistics.order_id)
                if not order:
                    continue
                order.status = Order.Status.COMPLETE
            print('执行完成')
        db.session.commit()
    except Exception:
        db.session.rollback()


if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()
    # 每天每小时整点执行该方法
    scheduler.add_job(update_logistic_status, CronTrigger.from_crontab('0 * * * *'))
    scheduler.start()
