from model.logistics import Logistics
from model.order import Order


class LogisticsDao(object):

    @staticmethod
    def query_logistic_by_order_number(order_number):
        return Logistics.query.join(Order, Order.id == Logistics.order_id).filter(Order.order_number == order_number).\
            with_entities(Order.order_number, Logistics.contents, Logistics.status).first()

    @staticmethod
    def query_logistic_by_send_telephone(send_telephone):
        return Logistics.query.join(Order, Order.id == Logistics.order_id). \
            filter(Order.send_telephone == send_telephone).with_entities(Order.order_number, Logistics.contents).all()

    @staticmethod
    def query_all_logistics():
        return Logistics.query.join(Order, Order.id == Logistics.order_id). \
            filter(Order.status == Order.Status.IN_COMPLETE).with_entities(Order.order_number, Order.send_name,
                                                                           Logistics.contents, Logistics.status).all()

    @staticmethod
    def query_logistic_by_logistic_order_number(order_number):
        return Logistics.query.join(Order, Order.id == Logistics.order_id).filter(Order.order_number == order_number)\
            .first()

    @staticmethod
    def get_all_doing_logistics():
        """
        获取所有非完成状态的物流信息
        :return:
        """
        return Logistics.query.filter(Logistics.status != Logistics.Status.DELIVERED).all()