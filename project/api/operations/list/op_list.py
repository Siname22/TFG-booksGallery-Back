from operations.base import *
from models.List import db
""" -----------------------------------------------GET----------------------------------------------------------"""
#get todos las listas del user
@ops_all.route('/lists/', methods=['GET'])
@token_required
def all_list(idUserConnect):
    list = List.query.all()
    resultado =[]
    for i in list:
        if i.id_User == idUserConnect.id:
            listUser = List.query.get(i.id)
            infoDef = listUser.to_dict()   
        resultado.append(infoDef)
    return jsonify(resultado)

""" -----------------------------------------------POST---------------------------------------------------------"""
#post para añadir una lista a un user
@ops_all.route('/addList/<int:idUserConnect>', methods=['POST'])
@token_required
def add_list(idUserConnect):
    name = request.json['name']
    id_User = idUserConnect
    if name is None:
        return jsonify({'Escribe un nombre para añadir a la lista'},401)
    list = List(
        name = name,
        id_User = id_User
    )
    db.session.add(list)
    db.session.commi()
    return jsonify(list.to_dict()), 201

""" -----------------------------------------------DELETE-------------------------------------------------------"""
@ops_all.route('/list/<int:idList>/<int:idUserConnect>', methods=["DELETE"])
@token_required
def delete_list(idList, idUserConnect):
    listToDelete = List.query.filter_by(id = idList).delete()
    db.session.commit()
    if not listToDelete:
        return jsonify({'El libro no esta en tu galeria de libros, elige otro libro para poder quitarlo de tu galeria.'})
    list = List.query.all()
    resultado =[]
    for i in list:
        if i.id_User == idUserConnect:
            listUser = List.query.get(i.id)
            infoDef = listUser.to_dict()   
        resultado.append(infoDef)
    return jsonify(resultado)
    


def list_in_user(idUserConnect, idList):
    list = List.query.filter_by(id = idList, id_User = idUserConnect)
    return list