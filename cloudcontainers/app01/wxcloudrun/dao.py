import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.model import *

# 初始化日志
logger = logging.getLogger('log')


# Count

def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


# 用户信息

def insert_new_user(openid, session_key=None, user_name=None, nick_name=None, profile_picture=None):
    """
    插入新的用户信息到数据库。
    
    :param openid: 用户的openid，必须提供
    :param session_key: 会话密钥，可选
    :param user_name: 用户名，可选
    :param nick_name: 昵称，可选
    :param profile_picture: 头像链接，可选
    """
    try:
        # 创建一个新的 UserInfo 实例
        new_user = UserInfo(
            openid=openid,
            session_key=session_key,
            user_name=user_name,
            nick_name=nick_name,
            profile_picture=profile_picture
        )
        
        # 添加新用户到数据库会话
        db.session.add(new_user)
        # 提交更改以保存到数据库
        db.session.commit()
        # 返回新用户的 uid
        return new_user.uid
    except OperationalError as e:
        logger.info("新增新用户 errorMsg= {} ".format(e))


def query_user_info(openid=None, uid=None, user_name=None):
    """
    根据 openid, uid 或 user_name 查询用户信息。
    
    :param openid: 用户的openid，可选
    :param uid: 用户的uid，可选
    :param user_name: 用户名，可选
    :return: 包含查询结果的列表
    """
    try:
        # 构建查询条件
        query = UserInfo.query
        
        if openid is not None:
            query = query.filter_by(openid=openid)
        if uid is not None:
            query = query.filter_by(uid=uid)
        if user_name is not None:
            query = query.filter_by(user_name=user_name)
        
        # 执行查询并获取结果
        results = query.all()
        
        # 返回结果列表
        return results
    except Exception as e:
        logger.info("查询用户信息时发生错误: {}".format(e))
        return []
    

