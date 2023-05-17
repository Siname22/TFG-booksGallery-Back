from project.__init__ import db

class UsersBooks(db.Model):
    id_Users = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    id_Books = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key = True)
    favoritos = db.Column(db.Boolean)
    def to_dict(self):
        return{
            'id_usuario': self.id_Users,
            'id_libros': self.id_Books,
            'favoritos':self.favoritos
        }