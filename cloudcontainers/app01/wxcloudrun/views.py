from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import *
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            # print('自增')
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


# 用户


@app.route('/api/insert_new_user', methods=['POST'])
def insert_new_user():
    """
    插入新的用户信息到数据库。
    """
    try:
        # 获取请求体参数
        params = request.get_json()

        # 检查必需的参数
        if 'openid' not in params:
            return make_err_response('缺少openid参数')

        # 从请求体中提取参数
        openid = params['openid']
        session_key = params.get('session_key')
        user_name = params.get('user_name')
        nick_name = params.get('nick_name')
        profile_picture = params.get('profile_picture')

        uid = insert_new_user(openid=openid, session_key=session_key, user_name=user_name,
                        nick_name=nick_name, profile_picture=profile_picture)

        # 返回新用户的 uid
        return make_succ_response({'uid': uid})
    except Exception as e:
        return make_err_response('插入新用户时发生错误: {}'.format(str(e)))
    

@app.route('/api/query_user_info', methods=['POST'])
def api_query_user_info():
    """
    根据 openid, uid 或 user_name 查询用户信息的 API 接口。
    """
    try:
        # 获取请求体参数
        params = request.get_json()

        # 提取查询参数
        openid = params.get('openid')
        uid = params.get('uid')
        user_name = params.get('user_name')

        # 调用 query_user_info 函数查询用户信息
        results = query_user_info(openid=openid, uid=uid, user_name=user_name)

        # 将查询结果转换为字典列表
        result_list = [{'uid': r.uid, 'openid': r.openid, 'session_key': r.session_key,
                        'user_name': r.user_name, 'nick_name': r.nick_name,
                        'profile_picture': r.profile_picture} for r in results]

        # 返回结果列表
        return make_succ_response(result_list)
    except Exception as e:
        return make_err_response('查询用户信息时发生错误: {}'.format(str(e)))