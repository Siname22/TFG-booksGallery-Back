from operations.base import *
from models.UsersBooks import db
from operations.books.op_books import get_info_book_gallery_Id
from operations.author.op_author import getInfoAutor_Id





""" -----------------------------------------------GET----------------------------------------------------------"""
#get todos los libros de la galeria del user
@ops_all.route('/books_gallery/<int:IdUser>', methods=['GET'])
@token_required
def obtener_libros_user(UserConnect):
    booksBg = UsersBooks.query.filter_by(id_Users = UserConnect.id)
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
def all_books_list(idBook,idUserConnect):
    booksBg = UsersBooks.query.filter_by(id_Users = idUserConnect)
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
@ops_all.route('/favorites/<int:idUserConnect>',methods=['GET'])
@token_required
def obtener_libros_favs(idUserConnect):
    booksBg = UsersBooks.query.filter_by(id_Users = idUserConnect, favoritos = True)
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
@ops_all.route('/detail_book_gallery/<int:idDetailBook>/<int:idUserConnect>', methods=['GET'])
@token_required
def detalles_libros(idDetailBook, UserConnect):
    booksBg = UsersBooks.query.filter_by(id_Users = UserConnect.id)
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
def detail_book_list(idDetailBook,idUserConnect):
    booksBg = UsersBooks.query.filter_by(id_Users = idUserConnect)
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
@ops_all.route('/delete_book_gallery/<int:idDeleteBook>/<int:idUserConnect>', methods=['DELETE'])
@token_required
def delete_libro(idDeleteBook, idUserConnect):
    book_deleteBg = UsersBooks.query.filter_by(id_Users = idUserConnect, id_Books = idDeleteBook).delete()
    db.session.commit()
    if not book_deleteBg:
        return jsonify({'El libro no esta en tu galeria de libros, elige otro libro para poder quitarlo de tu galeria.'})
    
    booksBg = UsersBooks.query.filter_by(id_Users = idUserConnect)
    resultado = []

    for i in booksBg:
        infoBookBg = get_info_book_gallery_Id(i.id_Books)
        infoAutor = getInfoAutor_Id(infoBookBg.id_Author)
        infoDef = infoBookBg.to_dict()

        infoDef['favoritos'] = i.favoritos
        infoDef['autor'] = infoAutor.to_dict()
        resultado.append(infoDef)
    
    return jsonify(resultado)
