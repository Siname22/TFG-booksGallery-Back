from project.__init__ import db
from sqlalchemy.orm import relationship

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    photo = db.Column(db.String(4000), nullable = False)
    books = relationship('Books', backref='autor', lazy=True)
    def to_dict(self):
        return{
            'id': self.id,
            'nombre': self.name,
            'foto': self.photo
        }