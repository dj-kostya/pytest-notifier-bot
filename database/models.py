from database.base import Base
from sqlalchemy import Column, Integer, Text, Boolean


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(Boolean, default=False)
    user_path = Column(Text)
    notifications_period = Column(Integer, default=300)
    checks_since_last = Column(Integer, default=1)
    failures_period = Column(Integer, default=30)
    failures_since_last = Column(Integer, default=1)
    detect_failures = Column(Boolean, default=True)
    failure_mute = Column(Boolean, default=False)

    def __repr__(self):
        return f'<User(id="{self.id}", user_id="{self.user_id}", status={self.status}, user_path={self.user_path}, ' \
               f'notifications_period = {self.notifications_period}, checks_since_last = {self.checks_since_last}, ' \
               f'failures_period = {self.failures_period}, failures_since_last = {self.failures_since_last}, ' \
               f'detect_failures = {self.detect_failures}, failure_mute = {self.failure_mute})>'
