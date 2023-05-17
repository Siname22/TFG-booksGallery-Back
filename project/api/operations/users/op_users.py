from operations.base import *
from models.Users import db
from werkzeug.security import  generate_password_hash
import uuid


""" -----------------------------------------------GET----------------------------------------------------------"""
#get all users
@ops_all.route('/users', methods=['GET'])
@token_required
def all_users():
    allUsers = Users.query.all()
    resultado =[]

    for i in allUsers:
        infoDef = i.to_dict()
        resultado.append(infoDef)

    return jsonify(resultado)

#get usersId
@ops_all.route('/user')
@token_required
def userId(current_user):
    user = Users.query.get(current_user.id)
    if not user:
        return jsonify({'mensaje': 'No se encontro el user'}), 404
    
    resultado =[]
    infoDef = user.to_dict()
    resultado.append(infoDef)
    
    return jsonify(resultado)

def getUserList(idUser):
    user = Users.query.get(idUser)
    return user


@ops_all.route('/register', methods=['GET', 'POST'])
def signup_user():  
 data = request.get_json()  

 hashed_password = generate_password_hash(data['password'], method='sha256')
 
 new_user = Users(
    public_id=str(uuid.uuid4()),
    name=data['nickname'], 
    password=hashed_password
    ) 
 db.session.add(new_user)  
 db.session.commit()    

 return jsonify({'message': 'registered successfully'})
