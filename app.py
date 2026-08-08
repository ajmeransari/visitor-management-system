from flask import Flask, redirect, url_for  
from config import Config 
from extensions import mysql
from flask_login import LoginManager, current_user
from models import User

app = Flask(__name__)

app.config.from_object(Config)

mysql.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


from auth.routes import auth_bp
from visitors.routes import visitor_bp
from users.routes import user_bp


app.register_blueprint(auth_bp)
app.register_blueprint(visitor_bp)
app.register_blueprint(user_bp)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('visitor.dashboard'))
    else:
        return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')