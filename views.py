import datetime
import json
import traceback

import jwt
from jwt import exceptions
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models import User, Tab, Customer

views = Blueprint('views', __name__)


# 创建token
def create_token(id, name):
    SALT = 'ydc'
    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload = {
        'user_id': id,
        'username': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 超时时间
    }
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return token


# 校验token
def get_payload(token):
    SALT = 'ydc'
    try:
        # 从token中获取payload【校验合法性】
        jwt.decode(token, SALT, True)
        return True
    # except exceptions.ExpiredSignatureError:
    #     print('token已失效')
    # except jwt.DecodeError:
    #     print('token认证失败')
    # except jwt.InvalidTokenError:
    #     print('非法的token')
    except:
        return False


# 登录接口
@views.route('/flask/api/v1/login', methods=['POST'])
def login():
    params = request.json
    name = params['params']['name']
    pwd = params['params']['pwd']

    user = User.query.filter_by(name=name).first()
    if not user.check_pwd(pwd):
        res = {
            'status': 500,
            'msg': '密码错误'
        }
        return jsonify(res)

    # 创建token
    token = create_token(user.id, user.name)
    res = {
        'id': user.id,
        'username': user.name,
        'mobile': user.mobile,
        'email': user.email,
        'token': token,
        'status': 200,
        'msg': '登录成功'
    }
    return jsonify(res)


# 注册
@views.route('/flask/api/v1/register', methods=['POST'])
def register():
    params = request.json
    name = params['params']['name']
    from werkzeug.security import generate_password_hash
    pwd = generate_password_hash(params['params']['pwd'])  # 加密
    email = params['params']['email']

    user = User.query.filter_by(name=name).first()
    if user is not None:
        res = {
            'msg': '该账号已存在',
            'status': 500
        }
        return jsonify(res)

    user = User(name=name, password=pwd, email=email)
    db.session.add(user)
    db.session.commit()

    res = {
        'msg': '注册成功',
        'status': 201
    }
    return jsonify(res)


# 获取所有标签
@views.route('/flask/api/v1/tabs', methods=['GET'])
def get_all_tabs():
    try:
        tabs = Tab.query.all()
        tabs = [{'name': t.name, 'id': t.id} for t in tabs]
        res = {
            'msg': '获取标签数据成功',
            'tabs': tabs,
            'status': 200
        }
        return jsonify(res)
    except:
        return jsonify({'msg': '获取标签数据失败', 'tabs': [], 'status': 500})


# 获取所有顾客信息
@views.route('/flask/api/v1/customers/', methods=['POST', 'GET', 'DELETE'])
def get_all_customers():

    if request.method == 'GET':

        try:
            query = request.args.get('query')  # 要查询的信息
            page_size = int(request.args.get('pageSize'))  # 页大小
            current_page = int(request.args.get('currentPage'))  # 当前页
            # 查询全部
            if query is '':
                customers = Customer.query.paginate(current_page, page_size).items
                total_customers = Customer.query.count()
                customers = [{'id': c.id, 'name': c.name, 'address': c.address,
                              'orders': [
                                  {'id': o.id, 'name': o.phone, 'from_address': o.from_address, 'to_address': o.to_address,
                                   'goods': o.goods, 'customer_id': o.customer_id} for
                                  o in c.orders if o is not None]} for c in customers]
                res = {
                    'msg': '获取顾客数据成功',
                    'customers': customers,
                    'status': 200,
                    'total': total_customers
                }
                return jsonify(res)
            # 模糊查询
            else:
                # Customer.query.filter(Customer.name.containts(query))
                res = Customer.query.filter(Customer.name.ilike('%' + query + '%'))
                customers = res.all()
                total_customers = res.count()
                customers = [{'id': c.id, 'name': c.name, 'address': c.address,
                              'orders': [
                                  {'id': o.id, 'name': o.phone, 'from_address': o.from_address,
                                   'to_address': o.to_address,
                                   'goods': o.goods, 'customer_id': o.customer_id} for
                                  o in c.orders if o is not None]} for c in customers]
                res = {
                    'msg': '获取顾客数据成功',
                    'customers': customers,
                    'status': 200,
                    'total': total_customers
                }
                return jsonify(res)
        except:
            return jsonify({'msg': '获取顾客数据失败', 'customers': [], 'status': 500, 'total': 0})

    if request.method == 'POST':
        try:
            params = request.json
            customer = Customer(name=params['name'], address=params['address'])
            db.session.add(customer)
            db.session.commit()
            return jsonify({'msg': '添加成功', 'status': 201})

        except:
            return jsonify({'msg': '添加失败', 'status': 500})

    if request.method == 'DELETE':
        try:
            id = request.args.get('id')
            headers = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'DELETE'
            }
            customer = Customer.query.filter_by(id=int(id)).first()
            if customer is not None:
                db.session.delete(customer)
                db.session.commit()
                return make_response((jsonify({'msg': '删除成功'}), 204, headers))
            else:
                db.session().rollback()
                make_response((jsonify({'msg': '删除失败'}), 500, headers))
        except:
            return make_response((jsonify({'msg': '删除失败'}), 500, headers))


# 根据用户id查询
@views.route('/flask/api/v1/customers/search', methods=['GET'])
def search_by_id():
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'DELETE'
    }
    try:
        cid = request.args.get('id')
        customer = Customer.query.filter_by(id=cid).first()
        res = {'id': customer.id, 'name': customer.name, 'address': customer.address}
        return make_response((jsonify({'customer': res, 'msg': '查询成功'}), 200, headers))
    except:
        return make_response((jsonify({'customer': '', 'msg': '查询失败'}), 500, headers))


# 编辑用户信息
@views.route('/flask/api/v1/customers/edit', methods=['PUT'])
def edit_customer():
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'DELETE'
    }
    try:
        params = request.json
        # 因为name 不可修改且是唯一的 所有可以用于查询
        customer = Customer.query.filter_by(name=params['name']).first()
        customer.address = params['address']
        db.session.commit()
        return make_response((jsonify({'msg': '修改成功'}), 200, headers))
    except:
        db.session().rollback()
        return make_response((jsonify({'msg': '修改失败'}), 500, headers))
