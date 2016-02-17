# catalog_database_data.py -- add sample data to the database for catalaog application
# Created by: Vineeta Gupta
# Date: 14 Feburary 2016

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database_setup import Base, User, Categorie, Item

engine = create_engine('sqlite:///catalogDBVineetaTry.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations.
session = DBSession()

# Create dummy user 1
user1 = User(name="Vineeta Gupta", email="gvineeta@yahoo.com",
             picture='Vineeta.jpg')
session.add(user1)
session.commit()

# Create dummy user 2
user2 = User(name="Riya ", email="riyaabc@yahoo.com",
             picture='Riya.jpg')
session.add(user1)
session.commit()

# Categories of user 1
Categorie1 = Categorie(name="Baseball",picture = "baseball.jpg", user=user1)
session.add(Categorie1)
session.commit()

Categorie2 = Categorie(name="Boxing",picture = "boxing.jpg", user = user1)
session.add(Categorie2)
session.commit()

# Categories of user 2
Categorie3 = Categorie(name="Cycling",picture = "cycling.jpg", user = user2)
session.add(Categorie3)
session.commit()

Categorie4 = Categorie(name="Football",picture = "football.jpg", user = user2)
session.add(Categorie4)
session.commit()

Categorie5 = Categorie(name="Hockey",picture = "hockey.jpg", user = user2)
session.add(Categorie5)
session.commit()

Categorie6 = Categorie(name="Surfing",picture = "surfing.jpg", user = user2)
session.add(Categorie6)
session.commit()

Categorie7 = Categorie(name="Tennis",picture = "tennis.jpg", user = user2)
session.add(Categorie7)
session.commit()


#Items for Category 1  - User 1

Item1 = Item(name="Bat & Ball", description="Baseball is one of America's most beloved and iconic sport. It is played with bat & Ball",picture="baseballbat&ball.jpg",user = user1, categorie = Categorie1)
session.add(Item1)
session.commit()

Item2 = Item(name="Gloves", description="When you get in the field, you need a fielding glove. They have batting, first base, catchers, and regular glove. You just need a regular fielding glove to start out.",picture="baseballgloves.jpg",user = user1, categorie = Categorie1)
session.add(Item2)
session.commit()

#Items for Category 2 - User 1

Item3 = Item(name="Boxing Gloves", description=" If you're serious enough about boxing to buy your own equipment, you should already have a sense of what size glove you need. ",picture="boxinggloves.jpg",user = user1, categorie = Categorie2)
session.add(Item3)
session.commit()

Item4 = Item(name="Boxing Wraps", description="Boxers apply boxing wraps to protect their hands from injury while lending additional support to the wrist and thumbs. Boxing without your hands properly wrapped can result in breaks to the movable bones and joints",picture="boxingwraps.jpg",user = user1, categorie = Categorie2)
session.add(Item4)
session.commit()


#Items for Category 3 - User 2

Item5 = Item(name="Cycle", description="a vehicle consisting of two wheels held in a frame one behind the other, propelled by pedals and steered with handlebars attached to the front wheel.",picture="cycle.jpg",user = user2, categorie = Categorie3)
session.add(Item5)
session.commit()

Item6 = Item(name="Cycle Helmet", description="A bicycle helmet is designed to attenuate impacts to the head of a cyclist in falls while minimizing side effects such as interference with peripheral vision.", picture="cyclehelmet.jpg",user = user2, categorie = Categorie3)
session.add(Item6)
session.commit()


#Items for Category 4 - User 2

Item7 = Item(name="FootBall Ball", description="A football is a ball inflated with air that is used to play one of the various sports known as football.",picture="footballball.jpg",user = user2, categorie = Categorie4)
session.add(Item7)
session.commit()

Item8 = Item(name="Studs", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.",picture="footballstuds.jpg",user = user2, categorie = Categorie4)
session.add(Item8)
session.commit()


#Items for Category 5 - User 2

Item9 = Item(name="Hockey Stick", description="A long, thin implement with a curved end, used to hit or direct the ball or puck in hockey or ice hockey.",picture="hockeystick.jpg",user = user2, categorie = Categorie5)
session.add(Item9)
session.commit()

Item10 = Item(name="Protecting Guards", description="Hockey shin guards are worn to protect your knees, shins and calves. With skates, sticks and pucks constantly moving around on the ice at high speeds, it is imperative that you wear shin guards that fit properly and offer good overall protection for your legs",picture="hockeypads.jpg",user = user2, categorie = Categorie5)
session.add(Item10)
session.commit()

#Items for Category 6 - User 2

Item11 = Item(name="SurfBoards", description="a long, narrow shaped board used in surfing.",picture="surfboard.jpg",user = user2, categorie = Categorie6)
session.add(Item11)
session.commit()

Item12 = Item(name="Surf Leg Rope", description="Although this can happen, most surfers today choose to use a leg rope whilst surfing as it is believed that leg ropes prevent more accidents than they cause",picture="surflegrope.jpg",user = user2, categorie = Categorie6)
session.add(Item12)
session.commit()


#Items for Category 7 - User 2

Item13 = Item(name="Racquets", description="Modern day tennis rackets are made from a high modulus graphite and/or carbon fibre, which is used to keep the frame lightweight and stiff for increased racket head stability and performance.",picture="tennisracquet.jpg",user = user2, categorie = Categorie7)
session.add(Item13)
session.commit()

Item14 = Item(name="Tennis Court", description="A tennis court is the venue where the sport of tennis is played. It is a firm rectangular surface with a low net stretched across the center.",picture="tenniscourt.jpg",user = user2, categorie = Categorie7)
session.add(Item14)
session.commit()


print "Added Data items!"