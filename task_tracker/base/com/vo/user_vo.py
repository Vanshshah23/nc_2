from base import db
from base.com.vo.login_vo import LoginVO

class UserVO(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    user_firstname = db.Column('user_firstname', db.String(100), nullable=False)
    user_lastname = db.Column('user_lastname', db.String(100), nullable=False)
    user_contact = db.Column('user_contact', db.Numeric, nullable=False)
    user_login_id = db.Column('user_login_id', db.Integer, db.ForeignKey(LoginVO.login_id))

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_firstname': self.user_firstname,
            'user_lastname': self.user_lastname,
            'user_contact': self.user_contact,
            'user_login_id': self.user_login_id
        }
db.create_all()
