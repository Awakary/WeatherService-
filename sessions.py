import os
from abc import ABC
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from config import settings
from exceptions import UsernameExistsException, SameLocationException
from models import User, engine, Location
from pd_models import *
from pd_models import LocationCheckUser


class BaseDao:

    def __init__(self):
        self.engine = engine
        self.session_factory = sessionmaker(
            bind=self.engine, autoflush=False
        )

    # def get_engine(self):
    #     return create_engine("sqlite:///./test_db.db") if os.environ.get("PYTEST_VERSION") else create_engine(settings.DB_URL)

    def get_one(self, *args, **kwargs):
        pass

    def save_one(self, *args, **kwargs):
        pass

    def delete_one(self, *args, **kwargs):
        pass


class UserDao(BaseDao):

    def get_one(self, login):
        with self.session_factory() as session:
            user = session.query(User).filter(User.login == login).first()
        return user

    def save_one(self, login, hashed_password):
        with self.session_factory() as session:
            print(session.bind, 55555)
            new_user = User(login=login, password=hashed_password)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise UsernameExistsException
            session.refresh(new_user)
        return new_user


class LocationDao(BaseDao):

    def save_one(self, location_for_db: LocationCheckUser):
        with self.session_factory() as session:
            new_location_dict = location_for_db.model_dump()
            new_location = Location(**new_location_dict)
            session.add(new_location)
            try:
                session.commit()
            except IntegrityError:
                raise SameLocationException
            session.refresh(new_location)
        return new_location

    def get_one(self, user: UserInDB):
        with self.session_factory() as session:
            user_locations = session.query(Location).filter(Location.user_id == user.id).all()
            return user_locations

    def delete_one(self, location_id: int):
        with self.session_factory() as session:
            session.query(Location).filter(Location.id == location_id).delete()
            session.commit()
            return "Удалено"
