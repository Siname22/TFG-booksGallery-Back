from project.__init__ import db

class BooksList(db.Model):
    id_Books = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key = True)
    id_List = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key = True)
    def to_dict(self):
        return{
            'id_libros': self.id_Books,
            'id_listas': self.id_List
        }