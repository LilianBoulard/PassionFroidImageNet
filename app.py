"""

For this app to work, two environment variables need to be set:
`PFIN_SERVER`: The endpoint leading to the MongoDB server.
`PFIN_SECRET`: A secret key used by Flask.

"""

import os

import pfin

from flask import Flask, render_template


app = Flask(__name__)

# Get Flask secret
PFIN_SERVER = pfin.config.PFIN_SERVER
PFIN_SECRET = pfin.config.PFIN_SECRET

if PFIN_SECRET == "" or PFIN_SERVER == "":
    raise ValueError('Please set your configuration variables. '
                     'They are needed to run the server.')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
