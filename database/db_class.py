from database.models import User
from database.create_session import session


class DB:

    @staticmethod
    def find_user_by_user_id(user_id):
        return session.query(User).where(User.user_id == user_id).all()[0]

    @staticmethod
    def get_users():
        """Get list of users that are testing via pytest"""
        return session.query(User).where(User.status).all()

    @staticmethod
    def user_exists(user_id):
        """Check if user exists in db"""
        result = session.query(User).where(User.user_id == user_id).all()
        return bool(len(result))

    @staticmethod
    def add_user(user_id):
        """Check if user exists in db, and if not, then adding it"""
        does_user_exist = session.query(User).filter(User.user_id == user_id).one_or_none()
        if does_user_exist is None:
            session.add(User(user_id=user_id))

    @staticmethod
    def update_user(user_id, **kwargs):
        """Updates user parameters"""
        session.query(User).filter(User.user_id == user_id).update(kwargs)   # extra check!

    @staticmethod
    def get_user_path(user_id):
        user_path_as_array = session.query(User.user_path).where(User.user_id == user_id).all()
        return user_path_as_array[0][0]

    @staticmethod
    def close_session():
        """Close session"""
        session.close()
