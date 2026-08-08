from flask_login import UserMixin
from extensions import mysql

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admin_users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return User(user_data[0], user_data[1], user_data[3])  # id, username, role
        return None
