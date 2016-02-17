
PROJECT:

Vineeta Catalog project - Project 3 - Full Stack Web Developer - Nanodegree - Udacity

---------------------------------

PROJECT DESCRIPTION:

The Catalog is a web application that provides a list of items within a variety of
categories. Users can view all the categories & items but can not edit & delete the ones created by other users.

Application integrates third party user registration and authentication through Google & Facebook. Uers can leverage their google or facebook a/c to login to Catalaog application. Authenticated users have the ability to post, edit, and delete their own items.

New users can create there own categories as well.

Application also supports image processing. The categories and items can have their own images.

application also supports JSON & XML endpoints.

---------------------------------

COPYRIGHT INFO:

Author: Vineeta Gupta
Version: 1.0
Available At: https://github.com/GVineeta/Vineeta-NanoDegree-Project-3-Ver-2
Copyright: Feburary 2016 All rights reserved

---------------------------------

SYSTEM REQUIREMENTS:

1. OS - Windows 2000/XP/7 or above, Also runs on Ubuntu
2. Python 2.7 or higher. Can be downloaded from https://www.python.org/downloads/
3. pyscopg2. Can be installed from  http://initd.org/psycopg/docs/install.html
4. If you face any issue, that might be because of these additional pacakage requirements mentioned in requirements.txt. You can install the same by doing 'pip install <package name>' of the specific ones or by doing 'pip install -r requirements.txt'


---------------------------------

INSTALLATION INSTRUCTIONS:

1. Download all the files from GitHub and copy them in any folder.
2. Go to command prompt, execute 'python catalog_database_setup.py'. The default database is created by name 'catalogDBVineeta.db', if you wish to change it, you can do so by updating the 'catalog_database_setup.py'. Also, do the same update in 'catalog_project.py'
3. If you wish to add sample data into 'catalogDBVineeta.db', Go to command prompt, execute 'python catalog_database_data.py' OR 'catalog_database_data_json.py'. You can also add the same sample data in your database. Just update the 'catalog_database_data.py' file with the database name you have opted in 'catalog_database_setup.py'
4. Go to command prompt, execute 'python catalog_project.py'. This will run the webserver at 8000 port by default. 

---------------------------------

USAGE NOTES:

1. Access the application at URL http://localhost:8000/catalog. Application will show up all the categories already created.
2. If not looed in earlier, Login via Google or Facebook a/c
3. Create new Category by clicking 'Add Category' link. Category needs Name & Image.
4. Create new Items in Category by clicking 'Add Item' against individual Category
5. You can Edit & Delete the items created by you. Categories once created, can not be edited or deleted.
6. Access the JSON at URL http://localhost:8000/catalog/JSON
7. Access the XML at URL http://localhost:8000/catalog/XML

-----------------------------------

CONTACT:

Support/Bug Reporting/Feedback:
vineeta.g@ge.com

---------------------------------

KNOWN BUGS:

1. Server side & client side validations are not implemented. 
2. Site Formatting has more scope of improvement. Thus please bear with me :)

Thanks,
Vineeta Gupta - Catalog Project Owner


