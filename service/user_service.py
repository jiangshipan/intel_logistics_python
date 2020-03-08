import uuid

from client.redis_client import redis_client
from dao.user_dao import UserDao
from model.user import User
from config.db import db
from utils.common_utils import Singleton


class UserService(object):
    """
    用户服务
    """
    __metaclass__ = Singleton

    def user_login(self, username, password):
        """
        用户登陆
        :param username:
        :param password:
        :return:
        """
        if not username or not password:
            raise Exception('username or password is empty')
        user = UserDao.get_user_by_username(username)
        if not user:
            raise Exception('user is not exist')
        if user.password != password:
            raise Exception('password is not available')
        # 验证通过，分配token
        token = self.assign_token(user.id)
        return token

    def user_register(self, user_info):
        """
        用户注册
        :param user_info:
        :return:
        """
        username = user_info.get('username')
        user = UserDao.get_user_by_username(username)
        if user:
            raise Exception('user has existed')
        try:
            user = User()
            user.username = username
            user.password = user_info.get('password')
            user.real_name = user_info.get('real_name')
            user.telephone = user_info.get('telephone')
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def assign_token(self, user_id):
        """
        分配token. 1天过期
        :param username:
        :return:
        """
        token = redis_client.get(user_id)
        if not token:
            token = str(user_id) + '-' + ''.join(str(uuid.uuid4()).split('-'))
            redis_client.set(user_id, token, ex=1 * 3600 * 24)
        return token

    def logout(self, user_id):
        redis_client.delete(user_id)

    def get_user_info(self, user_id):
        user = UserDao.get_user_by_user_id(user_id)
        if not user:
            raise Exception("不存在该用户或被禁用")
        user_info = {
            'id': user.id,
            'real_name': user.real_name,
            'identity_type': user.identity_type
        }
        return user_info

    def get_all_user_infos(self, user_id, identity_type):
        """
        管理员查询所有用户信息
        :param user_id:
        :return:
        """
        manager_user = UserDao.get_user_by_user_id(user_id)
        if manager_user.identity_type != User.IdentityType.MANAGER:
            raise Exception('你没有权限查看')
        user_infos = UserDao.get_users_by_identity_type(identity_type)
        res = []
        if int(identity_type) == User.IdentityType.CUSTOMER:
            identity_type = '普通客户'
        elif int(identity_type) == User.IdentityType.COURIER:
            identity_type = '快递员'
        else:
            identity_type = ''
        for user_info in user_infos:
            res.append({
                'username': user_info.username,
                'real_name': user_info.real_name,
                'identity_type': identity_type
            })
        return res

    def delete_user(self, user_id, username):
        """
        删除用户
        """
        try:
            manager_user = UserDao.get_user_by_user_id(user_id)
            if manager_user.identity_type != User.IdentityType.MANAGER:
                raise Exception('你没有权限操作')
            user = UserDao.get_user_by_username(username)
            if not user:
                raise Exception('用户不存在')
            user.status = User.Status.ABANDON
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def user_increase(self, user_id, username):
        """
        用户变为快递员
        """
        try:
            manager_user = UserDao.get_user_by_user_id(user_id)
            if manager_user.identity_type != User.IdentityType.MANAGER:
                raise Exception('你没有权限操作')
            user = UserDao.get_user_by_username(username)
            if not user:
                raise Exception('用户不存在')
            user.identity_type = User.IdentityType.COURIER
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
