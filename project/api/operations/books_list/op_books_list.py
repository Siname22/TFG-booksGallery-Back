from operations.base import *
from operations.list.op_list import list_in_user
from operations.user_books.op_user_books import all_books_list, detail_book_list
from models.BooksList import db


""" -----------------------------------------------GET----------------------------------------------------------"""

#get todos los libros de una lista
@ops_all.route('/books_list/<int:idList>/', methods=['GET'])
@token_required
def books_list(idList, idUserConnect):
    list = list_in_user(idUserConnect.id,idList)
    resultado =[]
    for i in list:
        booksList = BooksList.query.filter_by(id_List = i.id)
        for b in booksList:
            infoDef  = all_books_list(b.id_Books, idUserConnect.id)
            resultado.append(infoDef)

    return  jsonify(resultado)

#get detalle de un libro de la lista
@ops_all.route('/detail_book_list/<int:idBooks>/<int:idList>/', methods=['GET'])
@token_required
def detailBookList(idBooks, idList, idUserConnect):
    list = list_in_user(idUserConnect, idList)
    resultado = []
    for i in list:
        booksList = BooksList.query.filter_by(id_List = i .id)
        for b in booksList:
            if b.id_Books == idBooks:
                infoDef = detail_book_list(b.id_Books, idUserConnect)
    
    resultado.append(infoDef)
    return jsonify(resultado)

""" -----------------------------------------------DELETE-------------------------------------------------------"""
#delete del un libro de la lista
@ops_all.route('/delete_book_list/<int:idBook>/<int:idList>/<int:idUserConnect>', methods=['DELETE'])
@token_required
def delete_bookList(idBook, idList, idUserConnect):
    list = list_in_user(idUserConnect, idList)
    resultado = []
    for i in list:
        booksList = BooksList.query.filter_by(id_List = i.id, id_Books = idBook).delete()
        db.session.commit()
        resultado.append(booksList)
    return jsonify(resultado)
