from config.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, doc='用户唯一标识')
    username = db.Column(db.String(32), nullable=False, doc='用户名')
    password = db.Column(db.String(32), nullable=False, doc='密码')
    real_name = db.Column(db.String(32), nullable=False, default=u'', doc='真实姓名')
    telephone = db.Column(db.String(32), nullable=False, doc='联系电话')
    identity_type = db.Column(db.Integer, nullable=False, default=2, doc='0管理者 1快递员 2普通用户')
    status = db.Column(db.Integer, nullable=False, default=0, doc='状态 0 启用 1 禁用')

    class IdentityType(object):
        """
        用户身份
        """
        MANAGER = 0  # 管理员
        COURIER = 1  # 快递员
        CUSTOMER = 2  # 普通客户

    class Status(object):
        """
        用户状态
        """
        NORMAL = 0  # 正常
        ABANDON = 1  # 废弃


