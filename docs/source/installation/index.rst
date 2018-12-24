Installation
==============

*This project runs separately as frontend and backend. For that reason, you need install some requirements separately*

Install this project from github_ repository into your computer.

*********
Backend
*********

There are some requirements to run the backend side of the project. All of these requirements given in the requirements_ file. To install these packages, simply run::

  python -m pip install -r requirements.txt


After running this command, create a file in the **server** directory called **database.ini**. In the **database.ini** file, paste these codes::

   [postgresql]
   user=postgres
   host=localhost
   password=secret
   database=petek

Change the configurations according to your computer settings.

After creating the database, run these commands to create tables::

    cd server
    python dbinit.py

After running the second command, program will ask for some options. Hit 1 to create tables. Of course, you can also run the seeders to add dummy data.


You are all set. You can run the server by simply::

    cd ..
    python server.py

*********
Frontend
*********

Running frontend is quite simple. Go to frontend directory from root path and install the packages with::

    cd frontend
    npm install

This will create *node_modules* folder in the frontend directory holding the required packages for user interface.


You are all set. Simply run::

    npm run dev

to open frontend side of the project in the browser.

.. toctree::

   member1
   member2

.. _github: https://github.com/itucsdb1823/itucsdb1823
.. _requirements: https://github.com/itucsdb1823/itucsdb1823/blob/master/requirements.txt