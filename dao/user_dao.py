from model.user import User


class UserDao(object):

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter(User.username == username, User.status == User.Status.NORMAL).first()


    @staticmethod
    def get_user_by_user_id(user_id):
        return User.query.filter(User.id == user_id, User.status == User.Status.NORMAL).first()


    @staticmethod
    def get_users_by_identity_type(identity_type):
        return User.query.filter(User.identity_type == identity_type, User.status == User.Status.NORMAL).all()

    @staticmethod
    def get_deliver_by_real_name(real_name):
        """
        根据姓名获取快递员
        :return:
        """
        return User.query.filter(User.real_name == real_name, User.identity_type == User.IdentityType.COURIER).first()
