from flask import Flask
from flask_cors import CORS
import pymysql

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import mysqlconnector

app = Flask(__name__)

# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:xiaoliliya77@127.0.0.1:3306/vue_flask_mysql'
app.config['SQLALCHEMY_MODIFICATIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 创建数据库对象
db = SQLAlchemy(app)
# 解决 vue + flask 跨越问题
cors = CORS(app, resources={r"/flask/api/v1/*": {"origins": "*"}})
# 注册视图蓝图
from views import views
app.register_blueprint(views)
