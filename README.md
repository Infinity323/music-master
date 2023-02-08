# Music Master

## Setup and Installation

Prerequisites:

* Raspberry Pi 4 with Debian Bullseye OS
* Python 3
* Pip
* [PostgreSQL](https://www.postgresql.org/download/linux/debian/)
* NPM

Clone repository:

```bash
git clone https://github.com/Infinity323/music-master.git
```

### React

Install npm dependencies:

```bash
cd client
npm install
cd ..
```

### Flask

Setup Python environment and install dependencies:

```bash
cd server
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

### TODO: PostgreSQL

Create a user `postgres` with password `password` and a database named `music_master`:

## Running

To start the frontend, in one terminal:

```bash
cd client
npm start
```

To start the backend, in another terminal:

```bash
cd server
source env/bin/activate
flask run
```

The frontend will run on `localhost:3000`, while the backend will run on `localhost:5000`.

Ensure Postgres is running on `localhost:5432`.

## Notes

This project's organization is vaguely based on [React Flask Boilerplate](https://github.com/jeremyletran/react-flask-boilerplate): MIT © [Jeremy Le-Tran](https://github.com/jeremyletran).
