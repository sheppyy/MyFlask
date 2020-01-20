from app import db
db.metadata.clear()  # 去除缓存


# 用户模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30))
    mobile = db.Column(db.String(11))
    portrait = db.Column(db.String(100))  # 头像
    address = db.Column(db.String(100))
    introduce = db.Column(db.Text())

    # 解密
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, pwd)  # 解密后对比是否一致 返回bool值


# tabs模型
class Tab(db.Model):
    __tablename__ = 'tab'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# 订单模型 多
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    phone = db.Column(db.String(100), nullable=False)
    from_address = db.Column(db.String(100), nullable=False)
    to_address = db.Column(db.String(100), nullable=False)
    goods = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))


# 顾客模型 一
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')


if __name__ == '__main__':
    db.create_all()
