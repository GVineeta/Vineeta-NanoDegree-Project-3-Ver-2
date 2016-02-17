# catalog_database_data.py -- add sample data to the database for catalaog application
# Created by: Vineeta Gupta
# Date: 14 Feburary 2016

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from catalog_database_setup import Base, User, Categorie, Item

engine = create_engine('sqlite:///catalogDBVineeta.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations.
session = DBSession()

users_json = json.loads("""{
  "all_users": [
    {
      "id": 1,
      "name": "Vineeta Gupta",
      "email": "gvineeta@yahoo.com",
      "picture": "Vineeta.jpg"
    },
    {
      "id": 2,
      "name": "Riya",
      "email": "riyaabc@yahoo.com",
      "picture": "Riya.jpg"
    }
  ]
  }""")

for u in users_json['all_users']:
  users_input = User(
    id=(u['id']),
    name=str(u['name']), 
    email=str(u['email'])
  )
  session.add(users_input)
  session.commit()

category_json = json.loads("""{
  "all_categories": [
    {
      "id": 1,
      "name": "Baseball",
      "picture":"baseball.jpg",
      "user_id": 1
    },
    {
      "id": 2,
      "name": "Boxing",
      "picture":"boxing.jpg",
      "user_id": 1
    },
    {
      "id": 3,
      "name": "Cycling",
      "picture":"cycling.jpg",
      "user_id": 1
    },
    {
      "id": 4,
      "name": "Football",
      "picture":"football.jpg",
      "user_id": 1
    }
  ]
}""")

for c in category_json['all_categories']:
  category_input = Categorie(
    id=c['id'],
    name=str(c['name']),
    picture=str(c['picture']),
    user_id=c['user_id']
  )
  session.add(category_input)
  session.commit()

item_json = json.loads("""{
  "all_items": [
    {
      "id": 1,
      "name": "Bat & Ball",
      "description":"Baseball is one of America's most beloved and iconic sport. It is played with bat & Ball",
      "picture":"baseballbat&ball.jpg",
      "categorie_id": 1,
      "user_id": 1
    },
    {
      "id": 2,
      "name": "Gloves",
      "description":"When you get in the field, you need a fielding glove. They have batting, first base, catchers, and regular glove. You just need a regular fielding glove to start out.",
      "picture":"baseballgloves.jpg",
      "categorie_id": 1,
      "user_id": 1
    },
    {
      "id": 3,
      "name": "Boxing Gloves",
      "description":"If you're serious enough about boxing to buy your own equipment, you should already have a sense of what size glove you need. ",
      "picture":"boxinggloves.jpg",
      "categorie_id": 2,
      "user_id": 1
    },
    {
      "id": 4,
      "name": "Boxing Wraps",
      "description":"Boxers apply boxing wraps to protect their hands from injury while lending additional support to the wrist and thumbs. Boxing without your hands properly wrapped can result in breaks to the movable bones and joints",
      "picture":"boxingwraps.jpg",
      "categorie_id": 2,
      "user_id": 1
    },
    {
      "id": 5,
      "name": "Cycle",
      "description":"a vehicle consisting of two wheels held in a frame one behind the other, propelled by pedals and steered with handlebars attached to the front wheel.",
      "picture":"cycle.jpg",
      "categorie_id": 3,
      "user_id": 1
    },
    {
      "id": 6,
      "name": "Cycle Helmet",
      "description":"A bicycle helmet is designed to attenuate impacts to the head of a cyclist in falls while minimizing side effects such as interference with peripheral vision.",
      "picture":"cyclehelmet.jpg",
      "categorie_id": 3,
      "user_id": 1
    },
    {
      "id": 7,
      "name": "FootBall Ball",
      "description":"A football is a ball inflated with air that is used to play one of the various sports known as football.",
      "picture":"footballball.jpg",
      "categorie_id": 4,
      "user_id": 1
    },
    {
      "id": 8,
      "name": "Studs",
      "description":"Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.",
      "picture":"footballstuds.jpg",
      "categorie_id": 4,
      "user_id": 1
    }
  ]
}""")

for i in item_json['all_items']:
  item_input = Item(
    id=i['id'], 
    name=str(i['name']), 
    description=str(i['description']), 
    picture=str(i['picture']),
    categorie_id=i['categorie_id'], 
    user_id=i['user_id']
  )
  session.add(item_input)
  session.commit()