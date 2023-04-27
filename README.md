# Music Master

Music Master is a musical training program whose purpose is to assist beginner to intermediate musicians in learning how to play pieces with accurate feedback, without the need for feedback from an actual instructor.

For detailed instructions on using this program, check the [wiki](https://github.com/Infinity323/music-master/wiki/).

## Setup and Installation from Source

Prerequisites:

- Python 3.8 and Pip
- NPM 9.6.0+ and Node v16.14.2+

First, clone the repository.

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

On some operating systems, you may be required to install additional binaries via your OS's package manager. Be sure to do so as needed.

## Running Development Build

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

## Building and Packaging

For convenience, a build shell script, `build.sh`, has been added to the project directory. **Make sure to run it in the project directory!**

```bash
# Inside music-master/
./build.sh
```

This script will generate an executable in `client/dist/`. It can be run through command-line or double-clicking it in your file explorer.
