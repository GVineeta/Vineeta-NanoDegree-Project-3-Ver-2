# catalog_project.py -- implementation of a Catalog Application
# Created by: Vineeta Gupta
# Date: 14 Feburary 2016

#import all the required modules

from flask import g, Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, User, Categorie, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
from flask import send_from_directory
from werkzeug import secure_filename
import requests
import os
import xml.etree.ElementTree as ET
from functools import wraps

#Flask app handle
app = Flask(__name__)

#google client secreat jason load
CLIENT_ID = json.loads(
    open('google_client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogDBVineeta.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('catalogLogin.html', STATE=state)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Show all Categories & their items in Catalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Categorie).order_by(asc(Categorie.name))
    listOfitems=[]
    if 'username' not in login_session:
        user = ""
    else:
        user = session.query(User).filter_by(email = login_session['email'])
    for categorie in categories:
        items = session.query(Item).filter_by(categorie_id = categorie.id).all()
        listOfitems.append(items)

    return render_template('catalog.html', user = user,login_session = login_session, categories = categories, session = session, items = listOfitems)

# add the new categorie for the logged in user
@app.route('/addCategorie/', methods=['GET', 'POST'])
@login_required
def addCategorie():
    if request.method == 'POST':
        # If the request is for action & not cancel
        if request.form['submit'] == 'Add Category':
            # There is no need for this as we are doing @login_required, Which will redirect the user to login page if not already logged in.
            if 'username' in login_session:
                filename = ""
                file = request.files['uploadimage']
                if file:
                    filename = secure_filename(file.filename)
                    # save the uploaded image of categorie on disk
                    file.save(os.path.join(".\static\images", filename))
                categorie = Categorie(name = request.form['categorie_name'], picture = filename, user = getUserInfo(login_session['user_id']))
                session.add(categorie)
                flash(' %s categorie Successfully Added' % categorie.name)
                session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addcategorie.html', login_session = login_session)

# add the new item against a particular categorie for the logged in user
@app.route('/addItem/<int:categorie_id>', methods=['GET', 'POST'])
@login_required
def addItem(categorie_id):
    if request.method == 'POST':
        # If the request is for action & not cancel
        if request.form['submit'] == 'Add Item':
            # There is no need for this as we are doing @login_required, Which will redirect the user to login page if not already logged in.
            if 'username' in login_session:
                file = request.files['uploadimage']
                filename = ""
                if file:
                    filename = secure_filename(file.filename)
                    # save the uploaded image of item on disk
                    file.save(os.path.join(".\static\images", filename))            
                categorie =  session.query(Categorie).filter_by(id = categorie_id).one()
                item = Item(name = request.form['item_name'], picture = filename, description = request.form['description'], user = getUserInfo(login_session['user_id']), categorie = categorie)
                session.add(item)
                flash(' %s item successfully added' % item.name)
                session.commit()
        return redirect(url_for('showCatalog'))        
    else:
        return render_template('additem.html', login_session = login_session, categorie_id = categorie_id)
    
# edit the item against a particular categorie for the logged in user
@app.route('/editItem/<int:item_id>', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    item =  session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        # If the request is for action & not cancel
        if request.form['submit'] == 'Edit Item':
            # There is no need for this as we are doing @login_required, Which will redirect the user to login page if not already logged in.
            if 'username' in login_session:
                # If logged in user is the owner of the item, then only allow to edit
                if login_session['user_id'] == item.user_id:
                    file = request.files['uploadimage']
                    item.name = request.form['item_name']        
                    item.description=request.form['description']
                    oldfile= '.\static\images\%s' %item.picture
                    if file:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(".\static\images", filename))            
                        item.picture=filename 
                        if os.path.exists(oldfile):
                            os.remove(oldfile)
                        session.add(item)
                    flash(' %s Successfully Edited' % item.name)
                    session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('edititem.html',login_session = login_session, item=item)


# delete the specific item against a particular categorie for the logged in user
@app.route('/deleteItem/<int:item_id>', methods=['GET', 'POST'])
@login_required
def deleteItem(item_id):
    item =  session.query(Item).filter_by(id=item_id).one()
    categorie_id = item.categorie.id
    if request.method == 'POST':
        if request.form['submit'] == 'Delete Item':
            # There is no need for this as we are doing @login_required, Which will redirect the user to login page if not already logged in.
            if 'username' in login_session:
                # If logged in user is the owner of the item, then only allow to delete
                if login_session['user_id'] == item.user_id:
                    oldfile= '.\static\images\%s' %item.picture
                    if os.path.exists(oldfile):
                        os.remove(oldfile)
                    session.delete(item)
                    flash(' %s Successfully Deleted' % item.name)
                    session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html',login_session = login_session, item=item)



# for login via Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('google_client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#login via facebook account
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
        
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

# User Helper Functions - Create new user 
def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

# User Helper Functions - get user from database
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# User Helper Functions - get the user id against e-mail from database
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT FROM GOOGLE - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# DISCONNECT FROM FACEBOOK - Revoke a current user's token and reset their login_session
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Common disconnect method which will call disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


# JSON APIs to view catalog Information
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Categorie).all()
    categoriesWithItemsToJasonify=[]
    count=0
    #create dictionory and put categorie information
    for categorie in categories:
        tmpCategory = {
                'category_id' : categorie.id,
                'category_name' : categorie.name
        }
        tmpCategory['items'] = []                
        items = session.query(Item).filter_by(categorie_id=categorie.id).all()
        for item in items:
            #create dictionory and put item information
            items_dict = {
                'item_id' : item.id,
                'item_name' : item.name,
                'item_desc' : item.description
            }
            tmpCategory['items'].append(items_dict)

        categoriesWithItemsToJasonify.append( tmpCategory )
        value = {
            'status' : 'OK',
            'Categories' : categoriesWithItemsToJasonify
        }
    return jsonify(value)

# XML APIs to view catalog Information
@app.route('/catalog/XML')
def catalogXML():
    # Create root XML element Categories
    root = ET.Element("Categories")
    categories = session.query(Categorie).all()
    for categorie in categories:
        # Create sub XML element Categorie and add id & name as sub elements
        doc = ET.SubElement(root, "Catgorie")
        idtowrite = ET.SubElement(doc, "category_id")
        idtowrite.text = str(categorie.id)
        nametowrite = ET.SubElement(doc, "category_name")
        nametowrite.text = str(categorie.name)

        items = session.query(Item).filter_by(categorie_id=categorie.id).all()
        for item in items:
            # Create sub XML element Item under Categorie elemnt & add item id, name & description
            itemXML = ET.SubElement(doc, "Item")
            idtowrite = ET.SubElement(itemXML, "item_id")
            idtowrite.text = str(item.id)
            nametowrite = ET.SubElement(itemXML, "item_name")
            nametowrite.text = str(item.name)
            desctowrite = ET.SubElement(itemXML, "item_desc")
            desctowrite.text = str(item.description)
                
    return app.response_class(ET.tostring(root), mimetype='application/xml')
    
# main webserver runs on 8000 port
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)