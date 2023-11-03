from flask import Flask, make_response, render_template, redirect, url_for, request, jsonify, session
import logging

app = Flask(__name__)
app.secret_key = "168a90d618a4ff3f7a816eda137517bc"

# creating a logger and configureing it to write to a log file
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger('my_logger')

# store username and passwords inn a dict
user_credentials = {
    "staff": {"password": "password", "role":"staff"},
    "admin": {"password": "password", 'role': 'admin'}
}
# error handler for 404(Not Found) errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# internal server error 
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.route('/') 
def index():
    return render_template('Login.html', error_message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in user_credentials and password == user_credentials[username]['password']:
            role = user_credentials[username]['role']
            if role == "staff":
                logger.info(f'Successful login for {username} (staff)')
                return render_template('staff_dashbord.html', username=username)
            elif role == "admin":
                logger.info(f'Successful login for {username} (admin)')
                return render_template('dashboard.html', username=username)
        else:
            error_message = "Wrong username or password. Please try again."
            logger.warning(f'Login Failed {username}')
            return render_template('Login.html', error_message=error_message)

    # If the request method is GET or the login failed (GET request to show the login page)
    return render_template('Login.html', error_message="")

@app.route('/pos')
def pos():
    return render_template('pos.html')





if __name__ == '__main__':
    app.run(debug=True, host='192.168.106.225', port=5000)
