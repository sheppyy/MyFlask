## 项目使用
项目说明：此项目是一个后端的代码，配对的前端代码在[这里](数据库连接模块在app的init文件，修改成自己的用户名，密码即可，.sql文件在项目).此项目使用了多个方法实现相同的功能（其实就是乱！...），包含jwt(JSON Web tokens)认证、跨域、数据库增删改查、构造数据等等常用操作.

### 1.环境（python 3.6下，以下是主要包，要是报包不存在，安装即可）

    pip install flask
    pip install flask-sqlalchemy
    pip install pymysql
    pip install pyjwt
### 2. 数据库连接
数据库连接模块在app的init文件，修改成自己的用户名，密码即可，.sql文件在[这里](https://github.com/sheppyy/vue_flask_face.git)的db文件下，新建一个跟文件名相同的数据库，再执行文件即可

### 3. 启动服务

右键manage.py，运行即可，或终端执行 python manage.py。

哒哒~ 一个后端就跑起来啦！





有啥问题可Issues或邮箱ydcdck@163.com，技术菜，多多谅解~

