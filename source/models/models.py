from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from source.models import Base
import datetime


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String)
    phone = Column(String)
    source = Column(String)

    messages = relationship('Message', back_populates='user')
    tasks = relationship('Task', back_populates='user')

    def __repr__(self):
        return (f"<User(user_id='{self.user_id}', name='{self.name}, email='{self.email}', "
                f"phone='{self.phone}', source='{self.source}')>")


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    direction = Column(String)

    user = relationship('User', back_populates='messages')


class Scenario(Base):
    __tablename__ = 'scenarios'

    scenario_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    crm_system = Column(String)

    user = relationship('User', back_populates='tasks')


class Messenger(Base):
    __tablename__ = 'messengers'

    messenger_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    api_key = Column(String)


class Integration(Base):
    __tablename__ = 'integrations'

    integration_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    api_key = Column(String)

    def __repr__(self):
        return f"<Integration(integration_id='{self.integration_id}', name='{self.name}', api_key='{self.api_key}')>"
