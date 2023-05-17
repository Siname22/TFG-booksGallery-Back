from project.__init__ import db
from sqlalchemy.orm import relationship
from werkzeug.security import  generate_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(255), nullable = False)
    mail = db.Column(db.String(255), nullable = False)
    passwd = db.Column(db.String(255), nullable = False)
    list = relationship('List', backref='Users', lazy=True)
    
    
    def to_dict(self):
        return{
            'id': self.id,
            'nickname': self.nickname,
            'email': self.mail,
            'passwd': generate_password_hash(self.passwd)    
        }
    
    