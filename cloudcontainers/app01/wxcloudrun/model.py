from datetime import datetime

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())

# 用户信息表
class UserInfo(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'UserInfo'

    # 设定结构体对应表格的字段
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增长的主键
    openid = db.Column(db.String(100), unique=True, nullable=False)  # OpenID，唯一
    session_key = db.Column(db.String(100), nullable=True)  # Session key
    user_name = db.Column(db.String(50), nullable=True)  # 用户名
    nick_name = db.Column(db.String(50), nullable=True)  # 昵称
    profile_picture = db.Column(db.String(200), nullable=True)  # 头像链接
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f'<UserInfo {self.uid}>'