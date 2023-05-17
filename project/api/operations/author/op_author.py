from operations.base import *


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

