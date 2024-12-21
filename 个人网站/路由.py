from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime
from flask_cors import CORS
from flask_socketio import SocketIO, Namespace, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import os
import hashlib

app路由 = Flask(__name__)
socketio = SocketIO(app路由, cors_allowed_origins="*")  # 允许所有来源访问
app路由.secret_key = 'your_secret_key'  # 安全的字符串

# MySQL 配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': '个人网站',
}

# 连接数据库
def get_db_connection():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return connection

# 配置 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app路由)
login_manager.login_view = 'login'  # 未登录时重定向到登录页面

class User(UserMixin):
    def __init__(self, id, username, register_date, avatar=None):
        self.id = id
        self.username = username
        self.register_date = register_date
        self.avatar = avatar

# 加载用户的函数
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT 账号,用户名,注册时间,头像 FROM 用户信息 WHERE 账号 = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    return None

#首页
@app路由.route('/', methods=['GET', 'POST'])
@login_required  # 需要登录
def index():
    return render_template('首页.html')

# 注册
@app路由.route('/注册', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        账号 = request.form['账号']
        密码 = hashlib.sha256(request.form['密码'].encode()).hexdigest()
        用户名 = request.form['用户名']
        
        # 数据库插入
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # 先检查是否有相同的账号
            query_check_account = """SELECT 1 FROM 用户信息 WHERE 账号 = %s"""
            cursor.execute(query_check_account, (账号,))
            result = cursor.fetchone()

            if result:
                # 如果查询到账号已存在
                return render_template('注册.html', error="账号已存在，请选择其他账号！")
            
            # 如果账号不存在，则插入新数据
            query_insert = """INSERT INTO 用户信息 (账号, 密码, 用户名) VALUES (%s, %s, %s)"""
            cursor.execute(query_insert, (账号, 密码, 用户名))
            connection.commit()

            # 关闭连接
            cursor.close()
            connection.close()

            return redirect(url_for('login'))   # 注册成功后跳转到登录页面
        except Exception as e:
            return f"An error occurred: {e}"
    
    return render_template('注册.html')

# 登录
@app路由.route('/登录', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取前端提交的数据
        账号 = request.form['账号']
        密码 = hashlib.sha256(request.form['密码'].encode()).hexdigest()

        # 连接数据库并查询
        try:
            #连接数据库
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # 查询账号对应的密码
            query = """SELECT 密码, 用户名, 注册时间, 头像 FROM 用户信息 WHERE 账号 = %s"""
            cursor.execute(query, (账号,))
            result = cursor.fetchone()

            #关闭连接
            cursor.close()
            connection.close()

            if result:
                # 获取数据库中的密码和用户名
                db_password, db_username, db_register_date, db_avatar_url = result
                
                # 检查密码是否匹配
                if 密码 == db_password:
                    # 用户登录成功
                    user = User(账号, db_username, db_register_date, db_avatar_url)
                    login_user(user)  # 登录用户
                    return redirect(url_for('index'))  # 登录后跳转到首页
                else:
                    return render_template('登录.html', error="账号或密码错误！")
            else:
                return render_template('登录.html', error="账号不存在！")
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('登录.html')

#用户信息
@app路由.route('/用户信息')
@login_required  # 需要登录
def user_info():
    return render_template('用户信息.html')  # 渲染用户信息页面

# 配置文件上传的保存路径为项目根目录下的 '头像' 文件夹
app路由.config['UPLOAD_FOLDER'] = 'static/头像/'
app路由.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# 检查文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app路由.config['ALLOWED_EXTENSIONS']

#修改头像
# 头像上传路由
@app路由.route('/头像修改', methods=['POST'])
@login_required
def update_avatar():
    # 确保用户选择了文件
    if 'avatar' not in request.files:
        return redirect(url_for('user_info'))  # 如果没有选择文件，则返回用户信息页面
    
    avatar = request.files['avatar']
    
    # 如果没有选择文件，返回
    if avatar.filename == '':
        return redirect(url_for('user_info'))
    
    if avatar and allowed_file(avatar.filename):
        # 确保文件名安全
        filename = secure_filename(avatar.filename)
        
        # 保存文件到指定的文件夹
        avatar.save(os.path.join(app路由.config['UPLOAD_FOLDER'], filename))
        
        # 更新数据库中的头像字段（仅存储文件名）
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 更新用户头像（假设使用账号作为唯一标识）
        query = """UPDATE 用户信息 SET 头像 = %s WHERE 账号 = %s"""
        cursor.execute(query, (filename, current_user.id))
        connection.commit()
        
        # 关闭数据库连接
        cursor.close()
        connection.close()
        
        # 更新当前用户对象的头像字段
        current_user.avatar = filename
        
        # 跳转回用户信息页面
        return redirect(url_for('user_info'))
    
    return '无效的文件类型', 400

@app路由.route('/修改信息', methods=['POST'])
@login_required
def update_user_info():
    用户名 = request.form.get('用户名')
    密码 = hashlib.sha256(request.form['密码'].encode()).hexdigest()

    # 连接数据库
    connection = get_db_connection()
    cursor = connection.cursor()

    # 更新用户名和密码（如果有更新）
    if 用户名:
        query_update_username = """UPDATE 用户信息 SET 用户名 = %s WHERE 账号 = %s"""
        cursor.execute(query_update_username, (用户名, current_user.id))
    
    if 密码:
        query_update_password = """UPDATE 用户信息 SET 密码 = %s WHERE 账号 = %s"""
        cursor.execute(query_update_password, (密码, current_user.id))
    
    connection.commit()
    cursor.close()
    connection.close()

    # 更新当前用户的属性
    current_user.username = 用户名

    return redirect(url_for('user_info'))  # 返回到用户信息页面


# 注销
@app路由.route('/注销')
def logout():
    logout_user()  # 注销用户
    return redirect(url_for('index'))  # 注销后返回首页

#小游戏
@app路由.route('/小游戏')
@login_required
def games():
    return render_template('小游戏.html')

@app路由.route('/小游戏/匹配')
@login_required
def minesweeper_matching():
    return render_template('小游戏/扫雷/匹配.html')

@app路由.route('/小游戏/扫雷')
@login_required
def minesweeper_game():
    return render_template('小游戏/扫雷/扫雷.html')

if __name__ == '__main__':
    socketio.run(app路由,host='0.0.0.0', port=5000, debug=True, use_reloader=False)
