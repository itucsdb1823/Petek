
How to use this repository
--------------------------

## Installation

- Download this project into your local computer

### Backend

- run `python -m pip install -r requirements.txt` command to install Python packages to your computer.

- Create database.ini file in the server directory and paste these configurations:
```
[postgresql]
user=postgres
host=localhost
password=secret
database=petek
```

- Change these configurations according to your local computer. Note that, this project uses postgresql database. So, you should install PostgreSQL.
- To install database tables, run these commands:
```
cd server
python dbinit.py
```

You will see some options in here. For example, to import database tables hit '1'.

After creating the tables use the ```cd ..``` command to go back and run ```python server.py``` command to start the Server (Flask App).

### Frontend
- Go to frontend directory with `cd frontend` command.
- Run `npm install` to install npm packages to your computer. This command will create a directory in the frontend path called `node_modules`. Note that, you need to install NPM to run this command.
- Run `npm run dev` command. This command will run frontend side of the project on `localhost:8080` port.
