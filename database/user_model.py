from database.mongo import mongo
from flask_bcrypt import Bcrypt
from datetime import datetime

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def create_user(email, password):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return mongo.db.users.insert_one({
        "email": email,
        "password": password_hash,
        "createdAt": datetime.utcnow()
    })

def check_password(user, password):
    return bcrypt.check_password_hash(user['password'], password)