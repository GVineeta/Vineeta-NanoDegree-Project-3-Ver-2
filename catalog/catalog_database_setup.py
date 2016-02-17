# catalog_database_setup.py -- create database for catalaog application
# Created by: Vineeta Gupta
# Date: 14 Feburary 2016

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#Create user table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

#Create Categorie table which has id, name & picture path location. And relation to User
class Categorie(Base):
    __tablename__ = 'categorie'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    #Using a cascade, in case categorie gets deleted, all the items of that category will get deleted
    user = relationship(User, cascade="all")
    #Serialize the fields to return as JSON or XML endpoints
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

#Create Item table which has id, name, description & picture path location.
#Each Item is related to its categorie & user
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)    
    description = Column(String(250))
    picture = Column(String(250))
    categorie_id = Column(Integer, ForeignKey('categorie.id'))
    categorie = relationship(Categorie)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    #Serialize the fields to return as JSON or XML endpoints
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id, 
            
        }

#Create database in SQLite
engine = create_engine('sqlite:///catalogDBVineeta.db')


Base.metadata.create_all(engine)