from config.db import db
from sqlalchemy import func


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, doc='快递单唯一标识')
    order_number = db.Column(db.String(50), nullable=False, doc='快递编号')
    send_name = db.Column(db.String(50), nullable=False, doc='寄件人姓名')
    send_telephone = db.Column(db.String(20), nullable=False, doc='寄件人电话号')
    send_pos = db.Column(db.String(100), nullable=False, doc='寄件人地址')
    receive_name = db.Column(db.String(50), nullable=False, doc='收件人姓名')
    receive_telephone = db.Column(db.String(20), nullable=False, doc='收件人电话号')
    receive_pos = db.Column(db.String(100), nullable=False, doc='收件人地址')
    appoint_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'预约时间')
    appoint_type = db.Column(db.Integer, nullable=False, default=0, doc='寄件方式 0 预约上门 1 自送')
    goods_weight = db.Column(db.Float, nullable=False, default=0, doc='物品重量, kg')
    order_cost = db.Column(db.BigInteger, nullable=False, default=0, doc='运费')
    create_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'订单生成时间')
    status = db.Column(db.Integer, nullable=False, default=0, doc='状态 0 未完成 1 已完成')

    class AppointType(object):
        """
        寄件方式
        """
        APPOINT = 0  # 预约上门
        SELF_SEND = 1  # 自送

    class Status(object):
        """
        快递单状态
        """
        IN_COMPLETE = 0  # 未完成
        COMPLETE = 1  # 已完成


