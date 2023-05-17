from project.__init__ import db

class List(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(125), nullable = False)
    id_User = db.Column(db.Integer, db.ForeignKey('users.id'))
    def to_dict(self):
        return{
            'id': self.id,
            'nombre' : self.name,
            'id_usuario': self.id_User, 
        }
