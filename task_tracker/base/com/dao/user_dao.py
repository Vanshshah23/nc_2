from base import db
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO


class UserDAO():
    def add_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()


