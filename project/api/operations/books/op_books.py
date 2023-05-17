from operations.base import *
from operations.author.op_author import getInfoAutor_Id

""" -----------------------------------------------GET----------------------------------------------------------"""

#get todo los libros
@ops_all.route('/books')
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
@ops_all.route('/detail_book/<int:idBook>')
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

