NOTE: the requirement freeze is populated with quite a bit of unneeded dependencies. Will have to clean this up, as it was a snapshot of our dev environment (we have experimented quite a bit with different kind of potential implementations)

This is the API for pyth.app. The pip requirements are in requirements.txt.
You will need to pass environment variables in terminal (or command-line, depending on your OS).
In Linux this will look like this:

export db_engine='postgresql://login:password@ip:5432/postgres' 
export FLASK_APP=api.py


If you plan on using Firebase, you may also want to pass the JSON variables as they are listed in settings.py (depending if and on what JSON you use, you may need to change a few Firebase specific things in methods.py). 
The configuration is currently in DEBUG mode, which can be changed in api.py __main__.
To run, either run api.py with python3 or by running:

flask run --host=0.0.0.0 --cert=/etc/letsencrypt/live/api.pyth.app/fullchain.pem --key=/etc/letsencrypt/live/api.pyth.app/privkey.pem

