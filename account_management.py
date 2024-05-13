from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import re
import time
app = Flask(__name__)

### db
# 配置MySQL數據庫連接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db:3306/some_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定義Account模型
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

# 定義LoginInfo模型
class LoginInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), db.ForeignKey('account.username'), nullable=False)
    count = db.Column(db.Integer, default=0)
    last_attempt_time = db.Column(db.BigInteger, default=0)

#db.create_all()
with app.app_context():
    db.create_all()
###


accounts = {}
login_info = {}

# Define the password regular expression
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,32}$')


# accounts api
@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verfiy the length of account username & password
    if len(username) < 3 or len(username) > 32:
        return jsonify({"success": False, "reason": "Username length must be between 3 and 32 characters"}), 400
    if len(password) < 3 or len(password) > 32:
        return jsonify({"success": False, "reason": "Password length must be between 8 and 32 characters"}), 400
    
    # Verfiy the condition of account passowrd
    if not password_regex.match(password):
        return jsonify({"success": False, "reason": "Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"}), 400

    # Check the account username exsits
    #if username in accounts:
    if Account.query.filter_by(username=username).first():
        return jsonify({"success": False, "reason": "Username already exists"}), 400

    # Create account
    #accounts[username] = password
    new_account = Account(username=username, password=password)
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"success": True}), 201

# accounts/verify api
@app.route('/accounts/verify', methods=['POST'])
def verify_account():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    # Query the account table
    account = Account.query.filter_by(username=username).first()

    # Check the account username exsits
    if account is None:
        return jsonify({"success": False, "reason": "Account does not exist"}), 400

    # Query the login_info Table
    login_info = LoginInfo.query.filter_by(username=username).first()
    if login_info is None:
        # If there is no data give them defult
        login_info = LoginInfo(username=username, count=1, last_attempt_time=0)
    else:
        if login_info.count is None:
            login_info.count = 0
        if login_info.last_attempt_time is None:
            login_info.last_attempt_time = 0

    # get the current time
    current_time = int(time.time())

    # check the count of login attemption 
    if login_info.count >= 5 and (current_time - login_info.last_attempt_time) < 60:
        return jsonify({"success": False, "reason": "Too many attempts. Please wait one minute before trying again."}), 429

    if account.password == password:
        login_info.count = 0
        login_info.last_attempt_time = 0
        db.session.add(login_info)
        db.session.commit()
        return jsonify({"success": True}), 200
    else:
        login_info.count += 1
        login_info.last_attempt_time = current_time
        db.session.add(login_info)
        db.session.commit()
        return jsonify({"success": False, "reason": "Incorrect password"}), 400
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)