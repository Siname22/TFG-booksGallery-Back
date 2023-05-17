from project.__init__ import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    portrait = db.Column(db.String(4000), nullable = False)
    publishing = db.Column(db.String(255), nullable = True)
    saga = db.Column(db.String(255), nullable = False)
    synopsis = db.Column(db.String(4000), nullable = False)
    id_Author = db.Column(db.Integer, db.ForeignKey('author.id'))
    def to_dict(self):
        return{
            'id': self.id,
            'nombre': self.name,
            'portada': self.portrait,
            'editorial': self.publishing,
            'saga': self.saga,
            'sinopsis': self.synopsis,
            'id_autor': self.id_Author
        }
