from model.order import Order


class OrderDao(object):

    @staticmethod
    def get_all_orders():
        return Order.query.filter().all()

    @staticmethod
    def get_order_by_order_number(order_id):
        return Order.query.filter(Order.id == order_id).first()