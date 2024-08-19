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

def insert_or_update_user(openid, session_key=None, user_name=None, nick_name=None, profile_picture=None):
    """
    插入或更新用户信息到数据库。
    
    :param openid: 用户的openid，必须提供
    :param session_key: 会话密钥，可选
    :param user_name: 用户名，可选
    :param nick_name: 昵称，可选
    :param profile_picture: 头像链接，可选
    """
    try:
        # 查询数据库中是否已存在该 openid 的用户
        existing_user = UserInfo.query.filter_by(openid=openid).first()

        if existing_user:
            # 如果用户已存在，则更新其信息
            existing_user.session_key = session_key
            existing_user.user_name = user_name
            existing_user.nick_name = nick_name
            existing_user.profile_picture = profile_picture
            
            # 提交更改以保存到数据库
            db.session.commit()
            
            return existing_user.uid
        else:
            # 如果用户不存在，则创建一个新用户
            new_user = UserInfo(
                openid=openid,
                session_key=session_key,
                user_name=user_name,
                nick_name=nick_name,
                profile_picture=profile_picture
            )
            db.session.add(new_user)
            db.session.commit()
            
            return new_user.uid
    except IntegrityError as e:
        db.session.rollback()  # 回滚事务
        logger.error("Database integrity error when inserting/updating user: {}".format(e))
    except Exception as e:
        db.session.rollback()  # 回滚事务
        logger.error("Error when inserting/updating user: {}".format(e))


def query_user_info(openid=None, uid=None, user_name=None):
    """
    根据 openid, uid 或 user_name 查询用户信息。
    
    :param openid: 用户的openid，可选
    :param uid: 用户的uid，可选
    :param user_name: 用户名，可选
    :return: 包含查询结果的列表
    """
    print(openid, uid, user_name)
    try:
        res = []
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
        res.extend(results)
        print(res)
        # 返回结果列表
        return res
    except Exception as e:
        logger.info("查询用户信息时发生错误: {}".format(e))
        return []
    

