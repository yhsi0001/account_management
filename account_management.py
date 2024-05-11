from flask import Flask, request, jsonify
import re
import time
app = Flask(__name__)

accounts = {}
login_info = {}

# Define the password regular expression
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,32}$')


# Accounts_api
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
    if username in accounts:
        return jsonify({"success": False, "reason": "Username already exists"}), 400

    # Create account
    accounts[username] = password
    return jsonify({"success": True}), 201

@app.route('/accounts/verify', methods=['POST'])
def verify_account():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Check the account username exsits
    if username not in accounts:
        return jsonify({"success": False, "reason": "Account does not exist"}), 400


    if username not in login_info:
        login_info[username] = {'count': 1, 'last_login_time': 0}

    # get the current time
    current_time = time.time()
    # get the current login username
    login_name = login_info[username]

    # check the count of login attemption 
    if login_name['count'] >= 5 and (current_time - login_name['last_login_time']) < 60:
        return jsonify({"success": False, "reason": "Too many attempts. Please wait one minute before trying again."}), 429

    
    if accounts[username] == password:
        login_name['count'] = 0
        login_name['last_login_time'] = None
        return jsonify({"success": True}), 200
    else :
        login_name['count'] += 1
        login_name['last_login_time'] = current_time
        print(login_name['count'])
        print(login_name['last_login_time'])
        return jsonify({"success": False, "reason": "Incorrect password"}), 400



# 啟動 Flask 應用
if __name__ == '__main__':
    app.run(debug=True)