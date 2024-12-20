from flask import Flask, session, redirect, url_for, request
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'test_secret_key'  # 生成 Session ID 的密钥
app.permanent_session_lifetime = timedelta(minutes=10)  # 设置会话有效期

# 页面 1：设置会话并显示 Session ID
@app.route('/')
def page1():
    session.permanent = True  # 设置为永久会话
    if 'sid' not in session:
        session['sid'] = request.cookies.get('session') or 'session_' + str(id(session))
    return f"Page 1 - Your SID is: {session['sid']}<br><a href='/page2'>Go to Page 2</a>"

# 页面 2：跳转后显示 Session ID
@app.route('/page2')
def page2():
    if 'sid' not in session:
        session['sid'] = request.cookies.get('session') or 'session_' + str(id(session))
    return f"Page 2 - Your SID is: {session['sid']}<br><a href='/'>Back to Page 1</a>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
