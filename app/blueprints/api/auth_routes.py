from flask import request, jsonify

from . import bp
from app.models import User

# checks if user info valid on login and stores hashkey if valid
@bp.post('/verifyuser')
def verify_user():
  content = request.json
  print(content)
  username= content['username']
  password= content['password']
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return jsonify([{'user token': user.token}])
  return jsonify([{'message':'Invalid User Info'}]) 

# Register User
@bp.post('/register-user')
def register_user():
  content = request.json
  username= content['username']
  email= content['email']
  password= content['password']
  user = User.query.filter_by(username=username).first()
  # verify user credentials are unique and fit paremeters
  if user:
    return jsonify([{'message':'Username Taken, Try again'}])
  user = User.query.filter_by(email=email).first()
  if user:
    return jsonify([{'message':'Email Taken, Try again'}])
  user = User(email=email, username=username )
  # user.password = user.hash_password(password)
  setattr(user,'password', user.hash_password(password))
  # Send new user data to Elephant SQL
  user.add_token()
  user.commit()
  print(user)
  return jsonify([{'message': f"{user.username} Registered"}])