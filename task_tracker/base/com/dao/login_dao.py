from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:
    def save_user(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def authenticate_user(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_username=login_vo.login_username,
                                                login_password=login_vo.login_password)
        return login_vo_list

    def search_user_exist(self,login_vo):
        return  LoginVO.query.filter_by(login_username = login_vo.login_username)

    def find_login_username(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_id=login_vo.login_id).all()
        login_username = login_vo_list[0].login_username
        return login_username

    def change_password(self, login_vo):
        db.session.merge(login_vo)
        db.session.commit()



