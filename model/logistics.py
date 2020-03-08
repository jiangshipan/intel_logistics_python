from config.db import db


class Logistics(db.Model):
    __tablename__ = 'logistics'

    id = db.Column(db.Integer, primary_key=True, doc='快递单唯一标识')
    order_id = db.Column(db.Integer, nullable=False, default=0, doc='订单id')
    user_id = db.Column(db.Integer, nullable=False, default=0, doc='快递员id')
    contents = db.Column(db.Text, default=0, doc='物流信息')
    status = db.Column(db.Integer, nullable=False, default=0, doc='状态 0 出库 1 运输中 2等待配送 3配送中 4配送完成')

    class Status(object):
        """
        物流状态
        """
        OUT_OF_STOCK = 0  # 出库
        TRANSPORTING = 1  # 运输中
        ARRAY_SITE = 2  # 等待配送
        DELIVERING = 3  # 配送中
        DELIVERED = 4  # 配送完成

        __label__ = {
            OUT_OF_STOCK: '出库',
            TRANSPORTING: '运输中',
            ARRAY_SITE: '等待配送',
            DELIVERING: '配送中',
            DELIVERED: '配送完成'
        }


