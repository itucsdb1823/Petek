Backend Guide for Developer
==============================

On the root directory run::

   python server.py

command to start the server. **server.py** file runs the commands in the **server/__init__.py** file.

*******
Routes
*******

Routing of the backend is done in the *routes.py* file inside the *server* folder.
The Api class in the flask_restful module is used for adding resources.

Example route for **register** resource: ::

    from flask_restful import Api

    api = Api(server)
    api.add_resource(r.Register, '/api/register')

The *routes.py* script contains every route for CRUD operations of each table. Additionally,
it contains the admin routes and the function to check if the user is admin. The admin check is
done by checking if the request contains "/admin/" in it's second part and if the role
of the user is admin.

***********
Resources
***********

The resources folder contains the necessary web resources for each route. To create a custom
resource, we use the *flask_restful* module and it's *Resource* class::

    from flask_restful import Resource

    class CreateEvent(Resource):
        # your code here...

In order to add an argument, we again use the flask_restful module. The reqparse class is used
to parse arguments::

    from flask_restful import Resource, reqparse

    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Title must be a string')

    class CreateEvent(Resource):
        # your code here...

We added an argument named title. Now we can parse and get the argument that was sent through
the request. For an example, let's create a POST request::

    from flask_restful import Resource, reqparse
    from flask_jwt_simple import jwt_required, get_jwt_identity

    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Title must be a string')

    class CreateEvent(Resource):
        @jwt_required
        def post(self):
        args = parser.parse_args()
        title = args['title']

The user sent a post request and sent an argument with name(key) title.
We parsed that argument using the reqparse class and assigned the value with
the key "title" to our variable named title. Now, we can use this variable when
we are creating or updating an event.

In this part, we also added the jwt_required pragma. The jwt is a token used for handling
authentication and sessions. We don't want any user to create an event without signing up.
So, we import the *flask_jwt_simple* module and the *jwt_required* class to prevent this.
You can insert this pragma to any resource that
you want to make available for only logged in users.

----------BURASI SİLİNEBİLİR----------

Now let's create an event. To do that, we use the Event model under
the models folder. The models folder contains the classes used in our application
and a base class. The base class contains functions for the CRUD operations.
It runs the SQL commands written in these functions.
All the other models inherit from it and use these
functions in their custom functions.

Continuing with our event, we create an instance of the Event class and call the
necessary functions::

    from flask_restful import Resource, reqparse
    from flask_jwt_simple import jwt_required, get_jwt_identity
    from server.models.Event import Event
    from server.helpers import response

    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Title must be a string')
    parser.add_argument('description', type=str, help='Description must be a string')
    parser.add_argument('max_participant', type=int, help='Max participant must be a number')
    parser.add_argument('started_at', type=str, help='Start date must be a string')

    class CreateEvent(Resource):
        @jwt_required
        def post(self):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        max_participant = args['max_participant']
        started_at = args['started_at']
        user_id = get_jwt_identity()['id']

        event = Event()
        event.create({
            'title': title,
            'description': description,
            'max_participant': max_participant,
            'started_at': started_at,
            'user_id': user_id
        })

        if event.validate() is False:
            return response({
                'errors': event.getErrors()
            }, 401)

        user = User().where('id', user_id).first()
        event.save()
        return response({
            'event': event.plus('user', user.data()).data()
        }, 200)

We have created our event :)

We used the response function in the helpers.py script. This function takes a
dictionary and an HTTP status code and creates an HTTP response from them.

Details about the HTTP codes can be found `here <https://www.restapitutorial.com/httpstatuscodes.html>`_


*********
Seeders
*********

The **migrations** folder contained the table creation commands for each table. Similarly,
the **seeders** folder contains the scripts to seed each table with a custom amount
of random data. This makes things very practical while testing the database operations.

The functions are called by running::

    cd server
    python dbinit.py

From the options, choose 3 first and then choose the tables you want to seed random data
by separating the table numbers with a space. The default insert value is 10 elements
but it can be modified from the source code by
adding parameters to the functions in dbinit.py

An example of a seeder is below::

    import random

    def lecturers_table_seeder(cur, fake, num=10):
        cur.execute("SELECT id FROM users")
        users = [x for xs in cur.fetchall() for x in xs]

        for i in range(0, num):
            cur.execute("""INSERT INTO lecturers(name, email, slug, created_at, user_id)
                        VALUES(%s, %s, %s, %s, %s) returning id""",
                        (str(fake.name()), str(fake.email()), str(fake.slug()),
                         str(fake.date_time_this_month()), int(random.choice(users))))

The cur parameter is the cursor of the psycopg2 module which is used for
connecting with the database.

The fake parameter is an instance of the Faker class of the
faker module. The faker module is a popular python module which is used for
creating random data in different types (name, email, text, ...) and languages
('tr_TR', 'en_US', ...).

If there are references in the table we are seeding, we first fetch all the IDs
using cursor.fetchall() and put them to an array. Then we use the random module
and select a random element from that array while inserting.