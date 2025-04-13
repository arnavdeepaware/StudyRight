from database.mongo import mongo
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_user(email, password):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return mongo.db.users.insert_one({
        "email": email,
        "password": password_hash,
        "createdAt": datetime.utcnow()
    })