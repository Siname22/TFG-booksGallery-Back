import os
import jwt
import datetime
import uuid
from flask import Blueprint, jsonify, request, make_response
from project.api.models.Author import Author, db
from project.api.models.Books import Books, db
from project.api.models.BooksList import BooksList, db
from project.api.models.List import List, db
from project.api.models.Users import Users, db
from project.api.models.UsersBooks import UsersBooks, db
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from project.config import DevelopmentConfig


ops_all = Blueprint('operaciones', __name__)
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(token)
            data = jwt.decode(token, DevelopmentConfig.SECRET_KEY, algorithms=["HS256"])
            print('data', data)
            current_user = Users.query.filter_by(id=data['id']).first()
            return f(current_user, *args, **kwargs)

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        
    return decorator

@ops_all.route('/')
def informacion_api():
    return 'Api de libros creada por Raul Poblete Illescas'

@ops_all.route('/auth/login', methods=['GET','POST'])  
def login_user(): 
    header = request.headers.get('Content-Type')
    username = request.json['username']
    password = request.json['password']
    
    
    print('Lo cojo desde el formulario------------------------------------------------>',header, username, password)

    if not username or not password:
        return make_response('Algun dato esta vacio',401, {'WWW.Authentication': 'Basic realm: "login required"'})
    

    user = Users.query.filter_by(mail=username).first()
    print('La contraseña es: ', check_password_hash(generate_password_hash(user.passwd), password=password))
   
    if check_password_hash(generate_password_hash(user.passwd), password=password):
        token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                           DevelopmentConfig.SECRET_KEY, algorithm="HS256")  
        print('El token del user: ', token)
        return jsonify({'token' : token }) 

    return make_response('No se ha podido identificar',  401, {'WWW.Authentication': 'Basic realm: "login required"'})




""" ------------------------------------operaciones de la tabla user------------------------------------------ """

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


""" ------------------------------------operaciones de la tabla books---------------------------------------- """

""" -----------------------------------------------GET----------------------------------------------------------"""

#get todo los libros
@ops_all.route('/books', methods=['GET'])
def all_books():
    allBooks = Books.query.all()
    resultado =[]
    
    for i in allBooks:
        infoAutor = getInfoAutor_Id(i.id_Author)
        infoDef = i.to_dict()
        del infoDef['id_autor']
        infoDef['autor'] = infoAutor.to_dict()

        resultado.append(infoDef)
    return jsonify(resultado)

#get de solo un libro
@ops_all.route('/detail_book/<int:idBook>', methods=['GET'])
def book_Id(idBook):
    bookPorId = Books.query.get(idBook)
    if not bookPorId:
        return jsonify({'El libro no existe'}), 404
    
    infoAutor = getInfoAutor_Id(bookPorId.id_Author)
    resultado = []
    infoDef = bookPorId.to_dict()
    del infoDef['id_autor']
    infoDef['autor'] = infoAutor.to_dict()

    resultado.append(infoDef)
    return jsonify(resultado)
    
def get_info_book_gallery_Id(idBook):
    bgId = Books.query.get(idBook)
    if not bgId:
        return jsonify({'El libro no existe'}), 404
    return bgId


#get de busqueda de libros
@ops_all.route('/books/<string:busqueda>', methods=['GET'])
def buscar_libros(busqueda):
    libros = Books.query.filter(Books.name.like(f'%{busqueda}%') | 
                                Books.saga.like(f'%{busqueda}%') | 
                                (Books.id_Author == Author.name.like(f'%{busqueda}%'))
                                ).all()
    if not libros:
        return jsonify({'mensaje': 'No se encontraron libros'}), 404
    resultado = []
    for libro in libros:

        infoDef = libro.to_dict()
        infoAutor = getInfoAutor_Id(libro.id_Author)
        del infoDef['id_autor']
        infoDef['autor'] = infoAutor.to_dict()
        
        resultado.append(infoDef)
    return jsonify(resultado)

""" -----------------------------------------------POST---------------------------------------------------------"""


""" ------------------------------------operaciones de la tabla autores---------------------------------------- """


""" -----------------------------------------------GET----------------------------------------------------------"""
#get todos los autores
@ops_all.route('/authors', methods=['GET'])
@token_required
def all_authors():
    allAuthors = Author.query.all()
    resultado = []
    for i in allAuthors:
        resultado.append(i.to_dict())
    return jsonify(resultado)

#get solo un autor
@ops_all.route('/author/<int:idAuthor>')
@token_required
def one_author(idAuthor):
    author = Author.query.get(idAuthor)
    if not author:
        return jsonify({'mensaje':'El autor no existe o no esta implementado. Si es el segundo caso, por favor agregalo a traves del boton, "Añadir Libro"'}), 404

    authorJSON = author.to_dict()
    resultado = []
    resultado.append(authorJSON)
    

    return jsonify(resultado)

#get del autor de un libro
def getInfoAutor_Id(idAuthor):
    author = Author.query.get(idAuthor)
    if not author:
        return jsonify({'mensaje':'El autor no existe o no esta implementado. Si es el segundo caso, por favor agregalo a traves del boton, "Añadir Libro"'}), 404
    return author



""" ------------------------------------operaciones de la tabla list---------------------------------------- """

""" -----------------------------------------------GET----------------------------------------------------------"""
#get todos las listas del user
@ops_all.route('/lists/', methods=['GET'])
@token_required
def all_list(current_user):
    list = List.query.all()
    resultado =[]
    for i in list:
        if i.id_User == current_user.id:
            listUser = List.query.get(i.id)
            infoDef = listUser.to_dict()   
        resultado.append(infoDef)
    return jsonify(resultado)

""" -----------------------------------------------POST---------------------------------------------------------"""
#post para añadir una lista a un user
@ops_all.route('/addList/', methods=['POST'])
@token_required
def add_list(current_user):
    name = request.json['name']
    id_User = current_user.id
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
@ops_all.route('/list/<int:idList>/', methods=["DELETE"])
@token_required
def delete_list(idList, current_user):
    listToDelete = List.query.filter_by(id = idList).delete()
    db.session.commit()
    if not listToDelete:
        return jsonify({'El libro no esta en tu galeria de libros, elige otro libro para poder quitarlo de tu galeria.'})
    list = List.query.all()
    resultado =[]
    for i in list:
        if i.id_User == current_user.id:
            listUser = List.query.get(i.id)
            infoDef = listUser.to_dict()   
        resultado.append(infoDef)
    return jsonify(resultado)
    


def list_in_user(current_user, idList):
    list = List.query.filter_by(id = idList, id_User = current_user)
    return list

""" ------------------------------------operaciones de la tabla userBooks---------------------------------------- """

""" -----------------------------------------------GET----------------------------------------------------------"""
#get todos los libros de la galeria del user
@ops_all.route('/books_gallery/', methods=['GET'])
@token_required
def obtener_libros_user(current_user):
    booksBg = UsersBooks.query.filter_by(id_Users = current_user.id)
    resultado = []

    for i in booksBg:
        infoBookBg = get_info_book_gallery_Id(i.id_Books)
        infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
        infoDef = infoBookBg.to_dict()
        del infoDef['id_autor']
        infoDef['favoritos'] = i.favoritos
        infoDef['autor'] = infoAutor.to_dict()
        resultado.append(infoDef)

    return jsonify(resultado)

#get todos los libros de una lista
def all_books_list(idBook,current_user):
    booksBg = UsersBooks.query.filter_by(id_Users = current_user)
    for i in booksBg:
        if i.id_Books == idBook:
            infoBookBg = get_info_book_gallery_Id(i.id_Books)
            infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
            infoDef = infoBookBg.to_dict()
            del infoDef['id_autor']
            infoDef['favoritos'] = i.favoritos
            infoDef['autor'] = infoAutor.to_dict()
            if not infoDef:
                return jsonify({'El libro no esta en tu galeria de libros, vuelve a añadirlo'})
    return infoDef

#get todos los libros favoritos
@ops_all.route('/favorites/',methods=['GET'])
@token_required
def obtener_libros_favs(current_user):
    booksBg = UsersBooks.query.filter_by(id_Users = current_user.id, favoritos = True)
    resultado =[]

    for i in booksBg:
        infoBookBg = get_info_book_gallery_Id(i.id_Books)
        infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
        
        infoDef = infoBookBg.to_dict()
        del infoDef['id_autor']
        infoDef['favoritos'] = i.favoritos
        infoDef['autor'] = infoAutor.to_dict()
        
        resultado.append(infoDef)

    return jsonify(resultado)

#get informacion de un libro en concreto
@ops_all.route('/detail_book_gallery/<int:idDetailBook>/', methods=['GET'])
@token_required
def detalles_libros(current_user,idDetailBook):
    booksBg = UsersBooks.query.filter_by(id_Users = current_user.id)
    resultado =[] 
    for i in booksBg:
        if i.id_Books == idDetailBook:
            infoBookBg = get_info_book_gallery_Id(i.id_Books)
            infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
            infoDef = infoBookBg.to_dict()
            del infoDef['id_autor']
            infoDef['favoritos'] = i.favoritos
            infoDef['autor'] = infoAutor.to_dict()
    resultado.append(infoDef)
    if not booksBg:
        return jsonify({'El libro no esta en tu galeria de libros, vuelve a añadirlo'})

    return jsonify(resultado)

#get detalle de un libro de una lista
def detail_book_list(idDetailBook,current_user):
    booksBg = UsersBooks.query.filter_by(id_Users = current_user)
    resultado =[] 
    for i in booksBg:
        if i.id_Books == idDetailBook:
            infoBookBg = get_info_book_gallery_Id(i.id_Books)
            infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
            infoDef = infoBookBg.to_dict()
            infoDef['favoritos'] = i.favoritos
            infoDef['autor'] = infoAutor.to_dict()
            
    resultado.append(infoDef)

    return resultado
"""-------------------------------------------------POST--------------------------------------------------------"""






""" -----------------------------------------------DELETE-------------------------------------------------------"""
#delete de un libro de la galeria del user
@ops_all.route('/delete_book_gallery/<int:idDeleteBook>/', methods=['DELETE'])
@token_required
def delete_libro(idDeleteBook, current_user):
    book_deleteBg = UsersBooks.query.filter_by(id_Users = current_user.id, id_Books = idDeleteBook).delete()
    db.session.commit()
    if not book_deleteBg:
        return jsonify({'El libro no esta en tu galeria de libros, elige otro libro para poder quitarlo de tu galeria.'})
    
    booksBg = UsersBooks.query.filter_by(id_Users = current_user.id)
    resultado = []

    for i in booksBg:
        infoBookBg = get_info_book_gallery_Id(i.id_Books)
        infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
        infoDef = infoBookBg.to_dict()

        infoDef['favoritos'] = i.favoritos
        infoDef['autor'] = infoAutor.to_dict()
        resultado.append(infoDef)
    
    return jsonify(resultado)

""" ------------------------------------operaciones de la tabla listBook---------------------------------------- """
""" -----------------------------------------------GET----------------------------------------------------------"""

#get todos los libros de una lista
@ops_all.route('/books_list/<int:idList>/', methods=['GET'])
@token_required
def books_list(current_user, idList):
    list = list_in_user(current_user.id,idList)
    resultado =[]
    for i in list:
        booksList = BooksList.query.filter_by(id_List = i.id)
        for b in booksList:
            infoDef  = all_books_list(b.id_Books, current_user.id)
            resultado.append(infoDef)

    return  jsonify(resultado)

#get detalle de un libro de la lista
@ops_all.route('/detail_book_list/<int:idBooks>/<int:idList>/')
@token_required
def detailBookList(idBooks, idList, current_user):
    list = list_in_user(current_user.id, idList)
    resultado = []
    for i in list:
        booksList = BooksList.query.filter_by(id_List = i .id)
        for b in booksList:
            if b.id_Books == idBooks:
                infoDef = detail_book_list(b.id_Books, current_user.id)
    
    resultado.append(infoDef)
    return jsonify(resultado)

""" -----------------------------------------------DELETE-------------------------------------------------------"""

#delete del un libro de la lista
@ops_all.route('/delete_book_list/<int:idBook>/<int:idList>/', methods=['DELETE'])
@token_required
def delete_bookList(idBook, idList, current_user):
    list = list_in_user(current_user.id, idList)
    resultado = []
    for i in list:
        booksList = BooksList.query.filter_by(id_List = i.id, id_Books = idBook).delete()
        db.session.commit()
        resultado.append(booksList)
    return jsonify(resultado)
